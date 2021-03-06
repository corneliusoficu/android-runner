# Investigating the Correlation between Perfume.js PerformanceMetrics and Energy Efficiency of Web Applications

This repository is a companion page for the paper "Investigating the Correlation between Perfume.js PerformanceMetrics and Energy Efficiency of Web Applications". The paper can be downloaded [here](./Investigating_Perfume_Performance_Metrics.pdf).

It contains all the material required to replicate our analysis, including an updated version of the [android-runner](https://github.com/S2-group/android-runner/blob/master/documentation/A_Mobile_2020.pdf) framework used for automating the execution of the experiments; [scripts](./scripts) for setting up the environment for the experiments; [data-analysis](./data-analysis) results and scripts written in R required to execute the data analysis and an [experiment-data](./experiment-data) folder containing roughly 26 hours of experiment data that we've obtained, together with data aggregation scripts.

![alt text](./resources/experiment-execution.png )

#### *Diagram of the experiment execution*

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

# Setting up the environment for the experiments

### 1. Setup Python virtual environment and install all dependencies
We strongly recommend to create a virtual environment before executing any Python scripts. This way you can isolate the experiment environment from your global Python environment.

Make sure you are in the root level of the repository and navigate to the scripts folder:
```shell
cd ./scripts
```
Setup Python venv
```shell
python3 -m venv venv
```
Install requirements
```shell
pip install -r requirements.txt
```

### 2. Sample a random number of website names
For this step, you have to randomly sample a number of websites from a csv file containing a list of websites in the form: *index,website*. We've included in this repository, in the [tranco](./tranco) folder, a list of the most accessed websites. To run the command execute the following:
```shell
python3 sample_random_websites.py -i ../tranco/top-1m.csv \
-o RANDOMLY_SAMPLED_WEBSITES.csv -n 5
```
Usage:

* **-i** <ins>INPUT_CSV_FILE</ins>: Csv file containing a list of websites from which to sample from. A line should contain the format: *number,website*. An example can be found in the [tranco/top-1m.csv](./tranco/top-1m.csv) file.

* **-o** <ins>OUTPUT_FILE_CSV</ins>: Csv file containing the randomly sampled websites

* **-n** <ins>NUMBER</ins>: Number of websites to randomly sample

### 3. Pull local versions of the randomly sampled websites
For this, make sure you have the ***wget*** package. For macOS, you can easily install it using brew:
```shell
brew install wget
```
Pull the websites locally:
```shell
python3 pull_hosts.py -i RANDOMLY_SAMPLED_WEBSITES.csv -f local_websites/
```
Usage:
* **-i** <ins>INPUT_CSV</ins>: Csv file containing the randomly sampled websites list

* **-f** <ins>FOLDER_NAME</ins>: Location where to store the pulled websites

### 4. Inject **perfume.js** library and sender script
In order to collect perfume.js metrics from the locally downloaded websites, you will have to run this script that will inject the neccessary JS scripts in the \<head> section of every index.html page of the locally downloaded websites.
```shell
python3 inject_perfume.py -f local_websites -i http://192.168.100.95:8080
``` 
Usage:
* **-f** <ins>FOLDER_NAME_LOCAL_WEBSITES</ins>: Folder name containing the previously downloaded websites

* **-i** <ins>LOCAL_IP_ADDRESS</ins>: local ip address of your computer with port 8080. This is the address of the collector server for perfume.js metrics used in the android-runner framework

### 5. Launch file server for the local websites
Make sure you are in the scripts folder when starting the server. A webserver will be started on port **9191**.
```shell
python3 serve_local_websites.py
```

### 6. Generate the config file for the experiments
```shell
python3 generate_config_file.py -f RANDOMLY_SAMPLED_WEBSITES.csv -i http://192.168.100.95:9191
```

This will generate the experiments config file using the template file json. After the script finishes, the **config_web.json** from [android-runner/examples/perfume_power/](./android-runner/examples/perfume_power/config_web.json) should contain the links to the locally downloaded websites.

Usage:
* **-f** <ins>RANDOMLY_SAMPLED_CSV_FILE</ins>: CSV file with the randomly sampled websites

* **-i** <ins>LOCAL_IP_ADDRESS</ins>: local ip address of your computer and port 9191, representing the websites that will be used for the experiment.

# Running the experiment

To run the experiment, simply execute the following shell script:
```shell script
./execute_experiment.sh 5
```

This shell script will execute the experiment 5 times in a row.

**When the script finishes, the experiment results will be available at** [android-runner/examples/perfume_power/output](./android-runner/examples/perfume_power/output)
