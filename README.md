# Investigating the Correlation between Perfume.js PerformanceMetrics and Energy Efficiency of Web Applications

This repository is a companion page for the paper "Investigating the Correlation between Perfume.js PerformanceMetrics and Energy Efficiency of Web Applications". The paper can be downloaded [here]().

It contains all the material required to replicate our analysis, including an updated version of the [android-runner](https://github.com/S2-group/android-runner/blob/master/documentation/A_Mobile_2020.pdf) framework used for automating the execution of the experiments; [scripts](./scripts) for setting up the environment for the experiments; [data-analysis](./data-analysis) results and scripts written in R required to execute the data analysis and an [experiment-data](./experiment-data) folder containing roughly 26 hours of experiment data that we've obtained, together with data aggregation scripts.

# Prerequisites for running the experiments

### 1. Operating System

In order to run the experiments you will need to have a **Unix** based operating system such as **Ubuntu** or **macOS**.

### 2. Python 3.7

Make sure you have the **Python 3.7** version installed. You can download Python by accessing the following [Link](https://www.python.org/downloads/release/python-379/).

### 3. Android SDK

You will need to run multiple tools from the Android SDK. The best way to install the Android SDK is by installing Android Studio. You can download and install Android Studio by accessing this [Link](https://developer.android.com/studio).

### 4. Install the Apktool

This tool is needed to decompile the **framework-res.apk** file that is stored on the Android Device. To install Apktool, follow the steps described [here](https://ibotpeaches.github.io/Apktool/install/).

### 5. Extract Power Profile XML from Android Device

Because these experiments need to run the **batterystats** profiler, you will need to extract the **power_profile.xml** file from the android device you plan to run your experiments on. To achieve this, the following steps are necessary:

1. Connect the Android Device to the computer using a cable.
2. Find your device's id:
```shell
adb devices
```
3. Copy the DEVICE_ID displayed by the preivous command and connect to the device using **adb**: 
```shell
adb connect <DEVICE_ID>
```

4. Pull the **framework-res.apk** file from the android device:
```shell
adb pull /system/framework/framework-res.apk
```

5. Decompile **framework-res.apk** file using apktool
```shell
apktool d framework-res.apk
```

6. After the apktool is done decompiling the APK, a folder called framework-res should be created in the current directory. The power_profile.xml file should be located at: ***./framework-res/res/xml/power_profile.xml***. Copy this file to the **power_profiles** folder of the repository. Example:
```shell
cp ./framework-res/res/xml/power_profile.xml ~/android-runner/power_profiles
```

### 6. Update experiment path dependencies
In order to correctly setup the experiment, you will need to setup some paths in the experiment config file. For this open the experiment configuration template which you can find in the repository at: ***./android-runner/examples/perfume_power/config_web_template.json***. **WARNING! ONLY CHANGE VALUES IN THE config_web_template.json FILE AND NOT IN THE config_web.json FILE DIRECTLY**.

In the config_web_template.json file, change the following paths: 

**"monkeyrunner_path"**: Change to the monkeyrunner file location inside the Android sdk folder. For macOS, the monkeyrunner is located at: **~/Library/Android/Sdk/tools/bin/monkeyrunner**.

**"systrace_path"**: Change to the systrace file location inside the Android sdk folder. For macOS, the systrace file is located at: **~/Library/Android/Sdk/platform-tools/systrace/systrace.py**.

**"powerprofile_path"**: Update with the path to the power_profile.xml file you copied to power_profiles folder: **power_profiles/power_profile.xml**

 