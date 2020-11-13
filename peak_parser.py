'''
this is a work in progress script - still trying to work out some of the metrics and a few of them parsed here would need further calculation steps once in CSV
will update when I get a change
'''

import binascii
from bitstring import ConstBitStream, BitArray
import os
import sys
import jsons
import json
import statistics
import csv

class data:  
    def __init__(self, timestamp, hr, gsr, accel, temperature_b, temperature_c, temperature_d):  
        self.timestamp = timestamp  
        self.accel = accel
        self.gsr = gsr
        self.hr = hr
        self.temperature_b = temperature_b
        self.temperature_c = temperature_c
        self.temperature_d = temperature_d

dirname = os.path.dirname(__file__)

z = 0
samples = []

with open(os.path.join(dirname, 'pulsedata'), 'rb') as f:
    a = BitArray(f)
    for s in a.split('0x2988'):
        if len(s) >= 1912:
            samples.append(s)

print(str(len(samples)) + " samples")

i=0
valid_samples = []

while i < len(samples):
    selected_sample = samples[i]
    x = ConstBitStream(selected_sample)

    x.pos += 32
    time = 0
    try:
        time = x.read('uintle:32')
    except Exception:
        pass
    
    if time > 1600000000 and time < 1700000000:
        valid_samples.append(selected_sample)

    i += 1

print(str(len(valid_samples)) + " minutes of data")

i = 0
bio_data = []

while i < len(valid_samples):
    hr_array = []
    accel_array = []
    
    selected_sample = valid_samples[i]
    x = ConstBitStream(selected_sample)
    x.pos += 32
    time = x.read('uintle:32')
    #print(time)

    x.pos += 32
    unknown_a = x.read('uintle:16')
    #print(unknown_a)

    x.pos += 80

    z = 0
    while z < 60:
        hr = x.read('uintle:8')
        hr_array.append(hr)
        z += 1
    average_hr = statistics.mean(hr_array)
    #print(hr_array)

    x.pos += 64
    z = 0
    while z < 60:
        accel_x = x.read('uintle:8')
        if accel_x == 49:
            accel_x = 0
        accel_y = x.read('uintle:8')
        if accel_y == 49:
            accel_y = 0
        accel = (accel_x,accel_y)
        accel_array.append(accel)
        z += 1
    accel_sum = sum(e[0] for e in accel_array) + sum(e[1] for e in accel_array)
    #print(accel_sum)
    #print(accel_array)

    x.pos += 64
    temperature_b = x.read('uintle:16')
    if temperature_b > 5000 or temperature_b < 1800:
        temperature_b = ""
    #print(temperature_b)
    gsr = x.read('uintle:24')
    #print(gsr)

    x.pos += 8
    temperature_c = x.read('uintle:16')
    if temperature_c > 5000 or temperature_c < 1800:
        temperature_c = ""
    #print(temperature_c)
    temperature_d = x.read('uintle:16')
    if temperature_d > 5000 or temperature_d < 1800:
        temperature_d = ""
    #print(temperature_d)
        
    bio_data.append(data(time,average_hr,gsr,accel_sum,temperature_b,temperature_c, temperature_d))
    i += 1

with open('peak_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'HR','GSR','Accel','temp_b','temp_c','temp_d'])
    for row in bio_data:
        writer.writerow([row.timestamp, row.hr, row.gsr, row.accel,row.temperature_b
                         ,row.temperature_c,row.temperature_d])




