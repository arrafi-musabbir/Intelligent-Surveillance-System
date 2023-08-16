# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import pandas as pd
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
import urllib.request
import urllib
import cv2
import numpy as np
import time
import sys
from datetime import datetime
from threading import Thread
import random
# df = pd.DataFrame(columns=['datetime','battery', 'panel'])
DIR = os.path.join(os.getcwd(),'captured_videos')

from PyQt5 import QtCore, QtGui, QtWidgets
import serial.tools.list_ports
import serial
import webbrowser


from roboflow import Roboflow
rf = Roboflow(api_key="qoOnZEpyDZQDfK3no1Ur")
project = rf.workspace().project("a-2-object-detection")
roboflow_model = project.version(4).model


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		
		self.ser = None
		self.url = 'www.google.com'
  
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1920, 1080)
		MainWindow.setMinimumSize(QtCore.QSize(1920, 1080))
		MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setMinimumSize(QtCore.QSize(1920, 1080))
		self.centralwidget.setObjectName("centralwidget")
		self.background = QtWidgets.QLabel(self.centralwidget)
		self.background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
		self.background.setMinimumSize(QtCore.QSize(1920, 1080))
		self.background.setMaximumSize(QtCore.QSize(1920, 1080))
		self.background.setText("")
		self.background.setPixmap(QtGui.QPixmap("bg1.jpg"))
		self.background.setScaledContents(True)
		self.background.setObjectName("background")
		self.database = QtWidgets.QPushButton(self.centralwidget)
		self.database.setGeometry(QtCore.QRect(740, 630, 271, 391))
		self.database.setText("")
		self.database.setFlat(True)
		self.database.setObjectName("database")
		self.ops = QtWidgets.QPushButton(self.centralwidget)
		self.ops.setGeometry(QtCore.QRect(70, 70, 391, 331))
		self.ops.setText("")
		self.ops.setFlat(True)
		self.ops.setObjectName("ops")
		self.ops.setToolTip("Start operations")
		self.detected = QtWidgets.QPushButton(self.centralwidget)
		self.detected.setGeometry(QtCore.QRect(1610, 400, 131, 111))
		self.detected.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("radar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.detected.setIcon(icon)
		self.detected.setIconSize(QtCore.QSize(96, 96))
		self.detected.setFlat(True)
		self.detected.setObjectName("detected")
		self.detected.hide()
		self.comm = QtWidgets.QPushButton(self.centralwidget)
		self.comm.setGeometry(QtCore.QRect(1830, 10, 71, 81))
		self.comm.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("notConnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.comm.setIcon(icon1)
		self.comm.setIconSize(QtCore.QSize(64, 64))
		self.comm.setFlat(True)
		self.comm.setObjectName("connectESP")
		self.comm.setToolTip("Connect to receiver board")
		self.aiOps = QtWidgets.QLabel(self.centralwidget)
		self.aiOps.setGeometry(QtCore.QRect(1080, 130, 51, 51))
		self.aiOps.setText("")
		self.aiOps.setPixmap(QtGui.QPixmap("aiOps.png"))
		self.aiOps.setScaledContents(True)
		self.aiOps.setObjectName("aiOps")
		self.aiOps.setEnabled(False)
		self.startstop = QtWidgets.QLabel(self.centralwidget)
		self.startstop.setGeometry(QtCore.QRect(450, 50, 31, 31))
		self.startstop.setText("")
		self.startstop.setPixmap(QtGui.QPixmap("start.png"))
		self.startstop.setScaledContents(True)
		self.startstop.setObjectName("startstop")
		self.startstop.setEnabled(False)
		self.webApp = QtWidgets.QPushButton(self.centralwidget)
		self.webApp.setGeometry(QtCore.QRect(1014, 632, 891, 391))
		self.webApp.setText("")
		self.webApp.setFlat(True)
		self.webApp.setObjectName("webApp")
		self.webApp.setToolTip("Go to web application")
		
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.statusbar.showMessage("system intialiation...")

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		self.comm.clicked.connect(self.takeinputs)
		# self.ops.clicked.connect(self.startOps)
		self.ops.clicked.connect(self.detectionTask)
		self.webApp.clicked.connect(self.openWebApp)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

	def openWebApp(self):
		webbrowser.open(self.url, new=1)


	def startOps(self):
		
		def doStartOps():
			print("starting scanning ops")
			while True:
				# self.detected.hide()
				if self.ser == None:
					self.statusbar.show
					break
				elif self.ser.isOpen():
					
					self.startstop.setEnabled(True)
					line = self.ser.readline().decode().strip()
					if line == 'normal alert':
						
						print(line)
						self.detectionTask()
				else:
					break
				
		self.Thread1 = Thread(target = doStartOps).start()
		
	def detectionTask(self):
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("radar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.detected.setIcon(icon)
		self.detected.setIconSize(QtCore.QSize(96, 96))
		self.detected.setFlat(True)
		self.detected.setObjectName("detected")
		self.detected.show()
		print("starting detecton ops")
		self.aiOps.setEnabled(True)
		self.Thread2 = Thread(target = self.captureframes).start()
				
	def captureframes(self):
		print("connecting to camera feed")
		video = cv2.VideoCapture(0)
		# video = cv2.VideoCapture('rtsp://admin:L2F7BF79@192.168.0.108:554/cam/realmonitor?channel=1&subtype=1&unicast=true&proto=Onvif') #IP Camera
		fps = video.get(cv2.CAP_PROP_FPS)
		print(f"frames per second: {fps}")
		if (video.isOpened() == False): 
			print("Error reading video file")
		success,image = video.read()
		frame_count = 0
		save_count = 0
		save_interval = 1
		original_time = time.time()
		
		while success:
			if save_count > 10:
				print("stopping detection ops")
				self.aiOps.setEnabled(False)
				print("resuming scanning ops")
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("radar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.detected.setIcon(icon)
				self.detected.setIconSize(QtCore.QSize(96, 96))
				self.detected.setFlat(True)
				self.detected.setObjectName("detected")
				self.detected.hide()
				break
			
			self.current_datetime = str(datetime.now().strftime("%H-%M-%S-%p-%a-%d-%B-%Y"))
			if frame_count % (fps * save_interval) == 0:
				cv2.imwrite(os.path.join(os.getcwd(),'captured_frames/{}.jpg'.format(self.current_datetime)), image)
				print(f"frames saved: {save_count}")
				self.object_detection_image(os.path.join(os.getcwd(),'captured_frames/{}.jpg'.format(self.current_datetime)), frame_count)
				print(f"detection saved: {save_count}")
				save_count += 1     
				
			success,image = video.read()
			frame_count += 1
			
		video.release()
		cv2.destroyAllWindows()
	
	
	def object_detection_image(self, path, frame_count):
			file = path
			# print(file)
			if file!= None:
				img1 = Image.open(file)
				img2 = np.array(img1)
				img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
				confThreshold = 50
				nmsThreshold= 60
				whT = 320
				# url = "https://raw.githubusercontent.com/zhoroh/ObjectDetection/master/labels/coconames.txt"
				# f = urllib.request.urlopen(url)
				# classNames = [line.decode('utf-8').strip() for  line in f]
				f = open(r'config_n_weights\\raw.githubusercontent.com_zhoroh_ObjectDetection_master_labels_coconames.txt','r')
				lines = f.readlines()
				classNames = [line.strip() for line in lines]
				config_path = r'config_n_weights\yolov3.cfg'
				weights_path = r'config_n_weights\yolov3.weights'
				net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
				net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
				net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

				
				def findObjects(outputs,img2):
					hT, wT, cT = img2.shape
					bbox = []
					classIds = []
					confs = []
					for output in outputs:
						for det in output:
							scores = det[5:]
							classId = np.argmax(scores)
							confidence = scores[classId]
							if confidence > (confThreshold/100):
								w,h = int(det[2]*wT) , int(det[3]*hT)
								x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
								bbox.append([x,y,w,h])
								classIds.append(classId)
								confs.append(float(confidence))

					indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold/100, nmsThreshold/100)
					obj_list=[]
					confi_list =[]
					#drawing rectangle around object
					animals = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow']
					for i in indices:
						box = bbox[i]
						x, y, w, h = box[0], box[1], box[2], box[3]
						cv2.rectangle(img2, (x, y), (x+w,y+h), (240, 54 , 230), 2)
						# print('Number of objects: ', i, 'confidence: ', confs[i], 'classID: ', classIds[i], 'class name: ', classNames[classIds[i]].upper())
						if classNames[classIds[i]].upper() == 'PERSON':
							rf_preds = roboflow_model.predict(path, confidence=30, overlap=30)
							for i in rf_preds.json()['predictions']:
								if i['class'] == 'uniformed-person':
									self.ser.write('a'.encode())
									rf_preds.save(os.path.join(os.getcwd(),'detected_uniformed_persons/{}.jpg'.format(self.current_datetime)))
									print('Uniformed-person detected')
									icon = QtGui.QIcon()
									icon.addPixmap(QtGui.QPixmap("military.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
									self.detected.setIcon(icon)
									self.detected.setIconSize(QtCore.QSize(96, 96))
									self.detected.setFlat(True)
									database = pd.read_excel('database.xlsx', index_col=None)
									database.loc[len(database)] = [self.current_datetime, 'uniformed-person', i['confidence']]
									database.to_excel('database.xlsx', index=False)
								else:
									self.ser.write('s'.encode())
									print('civilian detected')	
									rf_preds.save(os.path.join(os.getcwd(),'detected_frames/{}.jpg'.format(self.current_datetime)))
									icon = QtGui.QIcon()
									icon.addPixmap(QtGui.QPixmap("motion.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
									self.detected.setIcon(icon)
									self.detected.setIconSize(QtCore.QSize(96, 96))
									self.detected.setFlat(True)
									database = pd.read_excel('database.xlsx', index_col=None)
									database.loc[len(database)] = [self.current_datetime, 'uniformed-person', i['confidence']]
									database.to_excel('database.xlsx', index=False)
						elif classNames[classIds[i]] in animals:
							self.ser.write('d'.encode())
							icon = QtGui.QIcon()
							icon.addPixmap(QtGui.QPixmap("animal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
							self.detected.setIcon(icon)
							self.detected.setIconSize(QtCore.QSize(96, 96))
							self.detected.setFlat(True)
							print('animal detected')
							database = pd.read_excel('database.xlsx', index_col=None)
							database.loc[len(database)] = [self.current_datetime, 'animal', i['confidence']]
							database.to_excel('database.xlsx', index=False)						
						try:
							print("adding to database >>> ", self.current_datetime, " ||| ", i['class'], " ||| ", i['confidence'])
							database = pd.read_excel('database.xlsx', index_col=None)
							database.loc[len(database)] = [self.current_datetime, i['class'], i['confidence']]
							database.to_excel('database.xlsx', index=False)
							cv2.putText(img2,f'{i["class"]}',
								(x, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 0, 240), 2)
						except IndexError:
							pass

					
				blob = cv2.dnn.blobFromImage(img2, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
				net.setInput(blob)
				layersNames = net.getLayerNames()
				outputNames = [layersNames[i-1] for i in net.getUnconnectedOutLayers()]
				outputs = net.forward(outputNames)
				findObjects(outputs,img2)
				cv2.imwrite(os.path.join(os.getcwd(),'detected_frames/{}.jpg'.format(self.current_datetime)), img2)
				cv2.waitKey(0)
				cv2.destroyAllWindows()          
	
	def takeinputs(self):
		ports = []
		for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
			ports.append(port)
		
		if self.ser != None:
			self.ser.close()
			self.ser = None
			self.statusbar.showMessage("comm port disconnected")
			icon3 = QtGui.QIcon()
			icon3.addPixmap(QtGui.QPixmap("notConnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.comm.setIcon(icon3)
			self.comm.setIconSize(QtCore.QSize(64, 64))
			done = False
		else:
			port, done = QtWidgets.QInputDialog.getItem(MainWindow, 'Input Dialog', 'Connect the port: ', ports)
			
		if done :
			self.connectEsp(port) 
			done = False
		else:
			print("No port selected")
			self.statusbar.showMessage('No port selected')
			self.ser = None
			self.statusbar.showMessage("no comm port. error connecting to at port: {}".format(None))
			icon3 = QtGui.QIcon()
			icon3.addPixmap(QtGui.QPixmap("notConnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.comm.setIcon(icon3)
			self.comm.setIconSize(QtCore.QSize(64, 64))
	
	def connectEsp(self, port):

		try:
			self.ser = serial.Serial(
					port=port,
					baudrate = 115200,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS,
					timeout=1
			)
			
			self.ser.flush()
			self.statusbar.showMessage('Connected to {}'.format(port))
			icon3 = QtGui.QIcon()
			icon3.addPixmap(QtGui.QPixmap("commConnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.comm.setIcon(icon3)
			self.comm.setIconSize(QtCore.QSize(64, 64))
			# self.readTempHum()
		except:
			self.ser = None
			self.statusbar.showMessage("no comm port. error connecting to at port: {}".format(port))
			icon3 = QtGui.QIcon()
			icon3.addPixmap(QtGui.QPixmap("notConnected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.comm.setIcon(icon3)
			self.comm.setIconSize(QtCore.QSize(64, 64))
	
	
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.showFullScreen()
	sys.exit(app.exec_())