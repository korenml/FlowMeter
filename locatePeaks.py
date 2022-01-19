##############################################
## Name: Flow meter find peaks script		##
## Author: Tomas Korinek					##
## Last update: 1.9.2021					##
## Version: 1								##
##############################################

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class Locate:
	def __init__(self, time, serie1, serie2, timeShift = 1.5, prominenceP=0.5, prominenceT=4):
		self.time = time
		self.s1 = serie1
		self.s2 = serie2
		
		self.peaksP, _ = find_peaks(self.s1,prominence=prominenceP)
		self.peaksT, _ = find_peaks(self.s2,prominence=prominenceT)
		self.delta = self.time[self.peaksT] - self.time[self.peaksP] -timeShift
		
	def returnPeaks(self):
		return self.peaksP, self.peaksT
	
	def flowTime(self):
		return self.delta

class ReadData:
	def __init__(self, filepath):
		self.filepath = filepath
		self.datalines = []
		self.time = []
		self.temperature = []
		self.pulse = []
		
		self.openFile()
		self.getData()
		
	def openFile(self):
		with open(self.filepath) as f:
			self.datalines = f.readlines()

	def getData(self):
		for i,dataLine in enumerate(self.datalines,start=0):
			if "#" in self.datalines[i]:
				pass
			else:
				data = self.datalines[i].split(" ")
				self.time = np.insert(self.time, len(self.time), float(data[0]))
				self.temperature = np.insert(self.temperature, len(self.temperature), float(data[1]))
				self.pulse = np.insert(self.pulse, len(self.pulse), float(data[2].replace("\n","")))
		
	def clearData(self):
		self.time = []
		self.temperature = []
		self.pulse = []

def main():

	data = ReadData("testLog")
	time = data.time
	pulse = data.pulse
	temperature = data.temperature
	fP = Locate(time,pulse,temperature)
	peaksP, peaksT = fP.returnPeaks()
	flowTime = fP.flowTime()
	endTime = time[-1]
	timeF = np.linspace(0,endTime,len(flowTime))

	fig, axs = plt.subplots(3,1)	
	axs[0].set_ylim(0,2)
	axs[0].plot(time,pulse)
	axs[0].scatter(time[peaksP],pulse[peaksP],s=15,marker="x",color="black")
	axs[1].plot(time,temperature)
	axs[1].scatter(time[peaksT],temperature[peaksT],s=15,marker="x",color="black")
	axs[1].set_ylim(280,320)
	axs[2].plot(timeF,flowTime)
	axs[2].set_ylim(np.min(flowTime)-1,np.max(flowTime)+1)
	plt.show()
	
if __name__ == "__main__":
	main()
