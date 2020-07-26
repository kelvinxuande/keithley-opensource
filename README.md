# Keithley opensource
Python GUI with optional arduino input for automation with Keithley Instruments

## Description
Keithley Instruments develop and sell a wide range of measurement and data acquisition products commonly used by professional
companies and hobbists. On top of the basic features that these products carry, [Keithley](https://www.tek.com/keithley) seperately sell tailor made add-on software that give assess to more features which are useful for scaling and semi-automation.

Purchasing these additional features is highly recommended. However, for hobbists just keen on tkintering with these machines but find purchasing these features out-of-budget, the scripts in this repository provides an additional layer of semi-automation that saves time, money and energy.

#### Disclaimer
The software is distributed 'as is' and with no warranties of any kind, whether express or implied, including and without limitation, any warranty of merchantability or fitness for a particular purpose. The user (you) must assume the entire risk of using the software. In no event shall any individual, company or organization involved in any way in the development, sale or distribution of this software be liable for any damages whatsoever relating to the use, misuse, or inability to use this software (including, without limitation, damages for loss of profits, business interruption, loss of information, or any other loss).'

However, should you face any difficulties in Testing/ Deploying the script, feel free to open an issue or contact the author via email.

* This README assumes that you have some knowledge of your keithley machine, arduino and python.
* Prototyping and testing was done on Keithley's DMM6500. With minimal knowledge on python, your instrument and RSvisa software, the script can be easily modified to work with similar Keithley products.

### Features
1) Two distinct modes of semi-automation - manual triggering and automatic polling of measurements.
2) As a proof-of-concept, the method of manual triggering was implemented with an arduino (UNO) push button. This button in turn signals to the PC to query from the instrument. With some knowledge of python, input methods can be easily modified.
3) As a proof-of-concept, there are two methods of output were implemented - Upon script completion, a database file (created, or updated with seperate sessions appended) and a csv file (unique for each session) is created. Again, with some knowledge of python, it is easy to change output methods.

### Script flowchart
![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/Program%20Flowchart.png)

### For Testing or Deployment?
Under Test mode, the script is hardcoded to run with the absence of some required hardware/ software, without fatal errors. Unlike the Deployment mode, it does not provide any useful data. Rather, it is meant to showcase the features, logic flow and GUI. The source code for Testing is the same as the one for Deployment, with the exception of some lines of codes (e.g. ones that involve querying) commented out.
<br/>*It is highly recommended to run tests before Deployment. To get started, follow the guiding steps below:*

## Running Tests
### Preinstallation
1) [Python 3.4](https://www.python.org/downloads/) or newer
2) For validating outputs, a simple database viewer/ [SQLite Browser](https://sqlitebrowser.org/) and MS Excel

*Points 3 and 4 are optional and only necessary for manual triggering with an Arduino Uno PushButton:*

3) [Arduino IDE](https://www.arduino.cc/en/main/software)
4) [Arduino PushButton](https://www.arduino.cc/en/Tutorial/StateChangeDetection) setup

Hardware Setup | Software Testing
------------ | -------------
![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/arduino_pushButton.png) | ![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/Arduino%20PushButton1.png)

### Installation and running tests
* Download and extract zipped Repository
* Run an instance of cmd prompt in the main folder, and install additional requirements using pip:
```python
pip install -r requirements.txt
```
* Once the requirements have finished installing, run an instance of cmd prompt in the main folder and execute the script:
```python
python main.py
```

### Expected outputs
Setup screen | Polling screen
------------ | -------------
![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/setup_screen.PNG) | ![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/polling_screen.PNG)

Setup screen | Polling screen
------------ | -------------
Text field titles are linked to database headings and can be easily modified. **To prevent errors, please select 'Polling [BETA]' under MEASUREMENT MODE in the setup screen if Arduino PushButton is not connected.* Once this is done, select 'start session'. | The script gives an estimation of the time required to complete a 'poll job', given a user input for the period and number of repetitions for polling. The 'poll job' begins when the user selects 'start polling', with the value '0.1' as a dummy measurement.

The estimation updates if there is a change in start time. There is also an infinite progress bar that indicates that the script is 'alive'.

*The script was written such that both the measuring instrument and the Arduino PushButton is required for Deployment.*
*To maintain script consistency so that users can easily transit from Testing to Deployment, this requirement was kept for testing; with settings hardcoded for both the Arduino and Digital Multimeter/ measuring equipment to be 'visually/ virtually' connected.*

**If Arduino Uno is connected for manual triggering:**

Manual Triggering Screen | Description
------------ | -------------
![alt text](https://github.com/kelvinxuande/keithley_openSource/blob/master/images/Manual%20Triggering%20Screen.PNG) | Everytime the PushButton is pressed, a measurement is recorded; with the dummy measurement '0.1' registered for testing purposes.<br/>There is also a DELETE LAST option to delete the last registered measurement, and a PAUSE button as a safety feature.

## Deployment
### Preinstallation
* Installing the necessary drivers as per your measuring equipment. e.g. [Keithley DMM6500](https://www.tek.com/digital-multimeter/daq6510-software/keithley-ivi-com-ivi-c-driver-models-dmm6500-and-daq6510)
* Confirming the connection between your measuring equipment and your PC.
  - Commands such as 'READ?' can be sent using your PC to the measuring equipment.
  - Measurements are returned from your measuring equipment to your PC.
  - [Recommended third-party software](https://www.rohde-schwarz.com/sg/applications/r-s-visa-application-note_56280-148812.html)

### Installation
#### Configuring serial number
* From the 'connection confirmation above, a serial number corresponding to your machine should be obtained. Copy the serial number and replace the one found in `settings > line 25`
```python
resourceString = 'USB0::0x05E6::0x6500::04391587::INSTR'
```
#### Removing hardcoded hardware parameters
* Comment out lines 40 and 41 in `settings`
```python
hardware_status[1] = 1 # test code
hardware_status[0] = 1 # test code
```
#### Removing hardcoded measurements
* Ctrl-f and comment out lines with `'value = 0.1'`  
* Uncomment nearby corresponding lines that works with 'true values'
#### Once again, run an instance of cmd prompt in the main folder and execute the script, with the required hardware connected
```python
python main.py
```
* Both 'Arduino' and 'Digital Multimeter' should be indicated as 'connected'. - This can be controlled by manipulating the hardcoded parameters.
* Measurements should be queried only when desired, with the 'true values' reflected.

### Enhancements for Deployment
#### Additional manual triggering options
* [Micro SMD PushButtons](https://www.alibaba.com/product-detail/smd-smt-side-push-button-tact_60104431684.html)
* [USB Footpedals](https://www.dhgate.com/product/usb-foot-pedal-switch-control-keyboard-action/411540352.html)

### Built With

* [Python](https://www.python.org/downloads/)
* [Python's Multithreading](https://docs.python.org/3.7/library/threading.html)
* [PyVISA](https://pyvisa.readthedocs.io/en/latest/)
* [pySerial](https://pythonhosted.org/pyserial/)
* [Sqlite3](https://docs.python.org/3/library/sqlite3.html)
* [Tkinter](https://docs.python.org/3/library/tk.html)
* [Arduino](https://www.arduino.cc/en/main/software)


### Author

[Kelvin Tan Xuan De](https://github.com/kelvinxuande)
