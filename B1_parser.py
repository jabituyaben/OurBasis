#example parser - work in progress

import binascii
from bitstring import ConstBitStream, BitArray
import os
import sys
import jsons
import json
import statistics
import csv
from datetime import datetime

class data:  
    def __init__(self, timestamp, accell, galvanic, skintemp, heart_rate, unknown_val
                 ,average_accell,average_galvanic,average_skintemp,average_heart_rate,average_unknown_val,
                 HR_stdv,Galvanic_stdv,unknown_stdv):  
        self.time = time  
        self.accel = accell
        self.galvanic = galvanic
        self.heart_rate = heart_rate
        self.unknown = unknown_val
        self.skintemp = skintemp
        self.average_accell = average_accell
        self.average_galvanic = average_galvanic
        self.average_skintemp = average_skintemp
        self.average_heart_rate = average_heart_rate
        self.average_unknown_val = average_unknown_val
        self.HR_stdv = HR_stdv
        self.Galvanic_stdv = Galvanic_stdv
        self.unkown_stdv = unkown_stdv

dirname = os.path.dirname(__file__)

z = 0
valid_samples = []

#this is quite a brutal approach to parsing as it will drop partial chunks but it has proven fine in my case
with open(os.path.join(dirname, 'pulsedata'), 'rb') as f:
    a = BitArray(f)
    for s in a.split('0x2900'):
        if len(s) == 3680:
            valid_samples.append(s)

print(str(len(valid_samples)) + " minutes of data")

list = []

i=0
while i < len(valid_samples):
    accel_array = []
    skin_temp_array = []
    galvanic_array = []
    heartrate_array = []
    unknown_array = []

    selected_sample = valid_samples[i]
    x = ConstBitStream(selected_sample)

    x.pos += 16
    #time = x.read('hex:32')
    time = x.read('uintle:32')
    time += 1293840000
    time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    #print(time)

    x.pos += 16
    steps = x.read('uintle:8')
    #print(steps)

    z = 0
    x.pos += 56
    
    while z < 90:
        accel_x = x.read('uintle:8')
        accel_y = x.read('uintle:8')
        accel_z = x.read('uintle:8')
        accel = (accel_x,accel_y,accel_z)
        accel_array.append(accel)
        z+=1
    #print(accel_array[z-1])
    if len(accel_array) > 0:
        average_acel = sum(accel_array[0])+sum(accel_array[1])+sum(accel_array[2])
    else:
        average_acel = ""
    
    z=0
    while z < 30:
        skin = x.read('uintle:24')
        galvanic_array.append(1/skin) #seems to work for charting but probably doesn't convert to siemens/cm so will need to review
        z+=1
    #print(galvanic_array[z-1])
    if len(galvanic_array) > 0:
            average_galvanic = statistics.mean(galvanic_array)
            Galvanic_stdv = statistics.pstdev(galvanic_array)
    else:
            average_galvanic = ""
            Galvanic_stdv = ""

    z=0
    while z < 12:
        skin_temp = x.read('uintle:8')
        if skin_temp > 30 and skin_temp < 120:
            skin_temp_array.append(skin_temp)
        z+=1
    #print(skin_temp_array[z-1])
    if len(skin_temp_array) > 0:
            average_skintemp = statistics.mean(skin_temp_array)
    else:
            average_skintemp = ""

    z=0
    while z < 4:
        unkown = x.read('uintle:24')
        unknown_array.append(unkown)
        z+=1
    #print(uknown_array[z-1])
    if len(unknown_array) > 0:
            average_unknown = statistics.mean(unknown_array)
            unkown_stdv = statistics.pstdev(unknown_array)
    else:
            average_unknown = ""
            unkown_stdv = ""
    
    z=0
    while z < 60:
        heartrate = x.read('uintle:8')
        if heartrate > 50 and heartrate < 150: #temporary filter until I deal with noise better
            heartrate_array.append(heartrate)
        z+=1
    #print(heartrate_array[z-1])
    if len(heartrate_array) > 0:
            average_heartrate = statistics.mean(heartrate_array)
            HR_stdv = statistics.pstdev(heartrate_array)
    else:
            average_heartrate = ""
            HR_stdv = ""
    
    list.append(data(time,accel_array,galvanic_array,skin_temp_array,heartrate_array,unknown_array,average_acel,
                     average_galvanic,average_skintemp,average_heartrate,average_unknown,HR_stdv,Galvanic_stdv,unkown_stdv))
    i += 1


y = jsons.dumps(list)

with open('parsed.txt', 'w') as outfile:
    json.dump(y, outfile)


with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'HR','Skin_Temp','GSR','Unknown','Movement','HR_stdv','GSR_stdv','unkown_stdv'])
    for row in list:
        writer.writerow([row.time, row.average_heart_rate, row.average_skintemp, row.average_galvanic, row.average_unknown_val,
                         row.average_accell,row.HR_stdv,row.Galvanic_stdv,row.unkown_stdv])

