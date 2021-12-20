##########################################
## Name: Flow meter gui script			##
## Author: Tomas Korinek				##
## Last update: 16.11.2021				##
## Version: 3							##
##			3 - class based gui			##
##			2 - button functions		##
##			1 - function based gui		##
##########################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
import time
import sys
import locatePeaks


class Main():
	def __init__(self):
		self.mTime = 0
		self.status = True
		self.running = False
		self.zeroTime = 0.0
		self.t = []
		self.y = []
		self.y1 = []
		self.myTime()
		print("Time ", self.time)
		
		self.t.append(0.0)
		self.y.append(300 + np.sin(2*np.pi*self.t[-1]/5))
		self.y1.append(2+np.sin(2*np.pi*self.t[-1]/10)+0.5*np.sin(2*np.pi*self.t[-1]/2))
		plt.ion()
		
		self.fig, self.axs = plt.subplots(2)
		plt.subplots_adjust(bottom=0.3)
		self.l, = self.axs[0].plot(self.t, self.y, c="black",label="P1")
		self.l1, = self.axs[1].plot(self.t, self.y1, c="red",label="P2")
		self.axs[0].set_ylabel("Temperature (K)")
		self.axs[1].set_ylabel("Volumetric flow (m^3/s)")
		self.axs[1].set_xlabel("Time (s)")
		
		self.axslider = plt.axes([0.178, 0.15, 0.2, 0.075])
		self.axslider2 = plt.axes([0.178, 0.05, 0.2, 0.075])
		self.axstart = plt.axes([0.71, 0.15, 0.09, 0.075]) 
		self.axstop = plt.axes([0.81, 0.15, 0.09, 0.075]) 
		self.axsave = plt.axes([0.71, 0.05, 0.09, 0.075])
		self.axquit = plt.axes([0.81, 0.05, 0.09, 0.075])
		self.axbox = plt.axes([0.55, 0.12, 0.1, 0.075])
		
		self.slider = Slider(self.axslider,"Sensor distance",5,100,valinit=60,valstep=1)
		self.slider2 = Slider(self.axslider2,"Tube diameter",5,50,valinit=20,valstep=1)
		self.bstart = Button(self.axstart, 'START',hovercolor="green")
		self.bstop = Button(self.axstop, 'STOP',hovercolor="red")
		self.bsave = Button(self.axsave, 'SAVE')
		self.bquit = Button(self.axquit, 'QUIT',hovercolor="red")
		self.flowBox = TextBox(self.axbox,"Flow")
		self.bquit.on_clicked(self.quitClicked)
		self.bstart.on_clicked(self.startClicked)
		self.bstop.on_clicked(self.stopClicked)
		self.bsave.on_clicked(self.saveClicked)
		plt.pause(0.05)
		while self.status == True:
			self.run()
	
	def run(self):
		if self.running == True:
			self.myTime()
			self.t.append(self.time)
			self.axs[0].axis([self.t[-1]-10, self.t[-1], 295, 305])
			self.axs[1].axis([self.t[-1]-10, self.t[-1], 0, 4])
			self.y.append(300 + np.sin(2*np.pi*self.t[-1]/5))
			self.y1.append(2+np.sin(2*np.pi*self.t[-1]/10)+0.5*np.sin(2*np.pi*self.t[-1]/2)) 
			self.flowBox.set_val("{:.2f}".format(self.y1[-1]))
			self.l.set_xdata(self.t)
			self.l.set_ydata(self.y)
			self.l1.set_xdata(self.t)
			self.l1.set_ydata(self.y1)
			plt.draw()
		plt.pause(0.5)
	
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
		with open("outputFile", "w") as f:
			f.write("Data\n")
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
	case = Main()

