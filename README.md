# Thermflow
Post-processing script for molten salt flow meter at CTU-CIIRC
Author: Tomas Korinek
email: tomas.korinek@cvut.cz

## Installation
The current script does not need any instalation.

## Prerequisities
The script is written in Python 3 and was tested on Python 3.8.10. The script is using module *matplotlib*, *numpy*, *scipy*, *sys* and *time*.

## Running
To run the script just type

'''
python3 plotFlow.py
'''
or
'''
python plotFlow.py
'''
according to your personal settings.
The current script is reading the testLog file to read time, temperature and pulse dataset. In order to use another logfile, just change the name of file entering the FlowMeter class.

To see automatic ploting capability, try:
'''
python3 plotFlowTest.py
'''
it contains an early version of Thermflow script which was used for autoplot testing.


## Testing find peak algorithm
To test different find peaks algorithms just look and redefine the file *locatePeaks.py*
