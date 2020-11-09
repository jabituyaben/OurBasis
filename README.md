# OurBasis: resurrecting Basis watches
See blog post and youtube video for more info.

All the server files should be placed in your webserver and whatever server you use you’ll need to remap the original URLs requested from the basis app to these files. The URLs are listed in each file as comments and I’d advise also reviewing the source android APK’s for both the B1 & Peak in Jadx to get familiar with the requests and for any troubleshooting you might come across.

Aside from debugging using server logs or a packet sniffer, you can also review the android app logs, both the Peak and B1 have verbose logging:

B1 log location:
/storage/emulated/0/Android/data/com.mybasis.android.basis/files/logs
Peak log location:
/data/data/com.mybasis.android.basis.peak/files/log

You will also need a rooted android phone, it’s probably possible without one for the B1 but you’d be making life hard – older cheap handsets are easy to root. Because of the variety of methods in rooting phones, you’re best off searching for guides specific to your handset – I wouldn’t use my usual personal phone for this and I’d advise backing everything up on your phone before you attempt rooting if you’re not familiar with doing it. Bare in mind also that Basis watches had limited support for certain handsets so the app may not function on some devices. I used an old Samsung Galaxy S4 without issue. 

You’ll also need ADB (Android Data Bridge) to side-load the apps, access folders, ammend files and read logs.

The Basis B1 had a Developer Options menu in the production app where you can change the domain of the API, for the Peak you will have to ammend the shared preferences file for that unless you find a version with the dev options, the shared prefs file is in:

/data/data/com.mybasis.android.basis.peak/shared_prefs/com.mybasis.android.basis.peak_preferences.xml/

It’s a straightfoward process and once you make any updates to shared_prefs, you should close and restart the app for changes to get picked up.

If you’d like to have the app resolve to an IP address in the above rather than to a hostname, you will have to ammend the android APK’s. This can be done by decompiling the apps in apktool and ammending the smali files where relevant. I cross referenced against Jadx to find references to “https://api-“ and replaced that string with just “http://” I think for the B1 there might also be a couple of additional files where you have to replace “https://”  with “http://” if you go this route. You’ll see from the Basis app log files where you’ll need to do this because it will log the error appropriately. The other option to modifying the app is to setup a local DNS and route requests that way (untested). Be very sure about the changes you’re making to smali files – you can easily break the app or whatever specific thing you’re trying to do if you make mistakes.
The Python parser scripts are fairly short and self-explanatory but if you’re not familiar working with binary files, just do some searches on the segments of code you don’t understand. It’s worth looking into how data is stored in memory and representation of binary (just numbers in this case) in hexidecimal. The Peak parser is more work in progress – still figuring out where GSR data is and some of the temperature parsing might be wrong at the moment.

Other things you'll need:
- a Hex Editor
- APKtool
- ADB (Android Data Bridge) I'd actually advise just having the whole Android Studio because it's useful using the emulator to test any changes with the app - note bluetooth doesn't work with emulators in Android Studio.
- Jadx - Dex to Java decompiler
