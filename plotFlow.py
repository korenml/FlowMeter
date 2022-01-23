########################################
## Name: Flow meter gui script		##
## Author: Tomas Korinek				##
## Last update: 16.11.2021			##
## Version: 3						##
##			3 - class based gui		##
##			2 - button functions		##
##			1 - function based gui	##
########################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
import time
import sys

from locatePeaks import Locate, ReadData


class FlowMeter():
	def __init__(self,logfile):
		self.mTime = 0
		self.status = True
		self.running = False
		self.zeroTime = 0.0
		self.t = []
		self.y = []
		self.y1 = []
		self.myTime()
		self.data = ReadData(logfile)
		self.t = self.data.time
		self.y = self.data.temperature
		self.pulse = self.data.pulse
		fP = Locate(self.t,self.pulse,self.y)
		peaksP, peaksT = fP.returnPeaks()
		self.flowTime = fP.flowTime()
		plt.ion()

		self.initD = 20
		self.initL = 80
		self.surface = 0.25*np.pi*self.initD*self.initD/1000000
		self.sensorLength = self.initL/1000
		
		# Graph settings
		self.fig, self.axs = plt.subplots(2)
		plt.subplots_adjust(bottom=0.3)
		
		# initialize temperature graph 
		self.l, = self.axs[0].plot(self.t, self.y, c="black",label="P1")
		
		# calculate volumetric flow and initialize graph
		self.tF = np.linspace(self.t[0],self.t[-1],len(self.flowTime))
		self.volFlow = 60*1000*self.surface*self.sensorLength/self.flowTime
		self.l1, = self.axs[1].plot(self.tF, self.volFlow, c="red",label="P2")
		
		# Graph labels
		self.axs[0].set_ylabel("Temperature (K)")
		self.axs[1].set_ylabel("Volumetric flow (LPM)")
		self.axs[1].set_xlabel("Time (s)")
		
		# GUI widgets locations
		self.axslider = plt.axes([0.178, 0.15, 0.2, 0.075])
		self.axslider2 = plt.axes([0.178, 0.05, 0.2, 0.075])
		self.axstart = plt.axes([0.71, 0.15, 0.09, 0.075]) 
		self.axstop = plt.axes([0.81, 0.15, 0.09, 0.075]) 
		self.axsave = plt.axes([0.71, 0.05, 0.09, 0.075])
		self.axquit = plt.axes([0.81, 0.05, 0.09, 0.075])
		self.axbox = plt.axes([0.55, 0.12, 0.1, 0.075])
		
		# GUI initialization
		self.slider = Slider(self.axslider,"Sensor distance",5,100,valinit=self.initL,valstep=1)
		self.slider2 = Slider(self.axslider2,"Tube diameter",5,50,valinit=self.initD,valstep=1)
		self.bstart = Button(self.axstart, 'START',hovercolor="green")
		self.bstop = Button(self.axstop, 'STOP',hovercolor="red")
		self.bsave = Button(self.axsave, 'SAVE')
		self.bquit = Button(self.axquit, 'QUIT',hovercolor="red")
		self.flowBox = TextBox(self.axbox,"Flow")
		self.bquit.on_clicked(self.quitClicked)
		self.bstart.on_clicked(self.startClicked)
		self.bstop.on_clicked(self.stopClicked)
		self.bsave.on_clicked(self.saveClicked)
		self.slider.on_changed(self.update)
		self.slider2.on_changed(self.update2)
		
		
		plt.pause(0.05)
		while self.status == True:
			self.run()
	
	def run(self):
		if self.running == True:
			# clear old data
			self.data.clearData()
			# get data from peak locator
			self.data.getData()
			
			# set time
			self.t = self.data.time
			
			# graphs limits
			atMax = np.nanmax(self.y) + 0.5*(np.nanmax(self.y) - np.nanmin(self.y))
			atMin = np.nanmin(self.y) - 0.5*(np.nanmax(self.y) - np.nanmin(self.y))
			avolMax = np.nanmax(self.volFlow) + 0.5*(np.nanmax(self.volFlow) - np.nanmin(self.volFlow))
			avolMin = np.nanmin(self.volFlow) - 0.5*(np.nanmax(self.volFlow) - np.nanmin(self.volFlow))
			
			self.axs[0].axis([self.t[-1]-100, self.t[-1], atMin, atMax])
			self.axs[1].axis([self.t[-1]-100, self.t[-1], avolMin, avolMax])
			
			# set temperature
			self.y = self.data.temperature
			
			# peak location
			fP = Locate(self.t,self.pulse,self.y)
			self.flowTime = fP.flowTime()
			
			# volumetric flow calculation
			self.volFlow = 60*1000*self.surface*self.sensorLength/self.flowTime
			
			# flowtime graph input
			self.tF = np.linspace(self.t[0],self.t[-1],len(self.flowTime))
			
			# update graphs
			self.l.set_xdata(self.t)
			self.l.set_ydata(self.y)
			self.l1.set_xdata(self.tF)
			self.l1.set_ydata(self.volFlow)
			plt.draw()
		plt.pause(2)
	
	def update2(self,event):
		self.surface = 0.25*np.pi*self.slider2.val*self.slider2.val/1000000
	
	def update(self,event):
		self.sensorLength = self.slider.val/1000
	
	def quitClicked(self, event):
		print("quit")
		self.status = False
	
	def startClicked(self, event):
		self.zeroTime = time.process_time()
		self.running = True
		print("start")
	
	def stopClicked(self, event):
		self.running = False
		self.clear()
		print("stop")
	
	def saveClicked(self, event):
		with open("outputFile.csv", "w") as f:
			f.write("# Time, Volumetric flow\n")
			for i, tF in enumerate(self.tF, start=0):
				stream = str(self.tF[i]) + "," + str(self.volFlow[i]) + "\n"
				f.write(stream)
		print("save")

	def myTime(self):
		self.time = time.process_time() - self.zeroTime
		
	def clear(self):
		self.t = []
		self.y = []
		self.y1 = []
		self.t.append(0.0)
		self.y.append(300 + np.sin(2*np.pi*self.t[-1]/5))
		self.y1.append(2+np.sin(2*np.pi*self.t[-1]/10)+0.5*np.sin(2*np.pi*self.t[-1]/2))
		

if __name__ == "__main__":
	case = FlowMeter("testLog")

