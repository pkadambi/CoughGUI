'''
Created on Jan 23, 2017

@author: Prad
'''
import numpy as np
import sys
import winsound
import time
import os
import pyaudio
import glob
import threading
from PyQt5 import QtWidgets , QtGui
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QSplitter, QFrame, QMessageBox, QGridLayout, QLCDNumber
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QHBoxLayout, QSize, QSizePolicy, QFormLayout, QVBoxLayout, QGroupBox, QFormLayout, QTabWidget

class CoughRecorderGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Cough Trial Tool'
        self.left = 300
        self.top = 300
        self.right = 200
        self.width = 340
        self.height = 400
        self.currentlyRecording=False
        self.stopRecord = False
        self.currentlyCoughing = 0
        self.coughCount = 0
        self.recordStateIndicator = 'Current Status: NOT Recording.\nClick "Start Recording" To begin recording'
        self.deviceID=-1
        self.initUI()          
    #set coughingCurrently to 1 when button pressing
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_C:
            self.currentlyCoughing = 0         
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_C:
            self.coughCount += 1
            self.currentlyCoughing = 1
            self.updateCoughCount(self.coughCount) 
    
    def updateCoughCount(self, count):
        self.coughCountDisplay.display(self.coughCount)
    def initUI(self):   
        
        largefont = QtGui.QFont('Times', 12)
        largefont.setBold(False)
        normalfont= QtGui.QFont('Times', 8)
        normalfont.setBold(False)
        smallfont = QtGui.QFont('Times', 8)
        smallfont.setBold(True)
        
        #Device ID Text Box
        self.textboxDevID = QLineEdit(self)
        self.textboxDevID.setMaximumWidth(50)
        self.textboxDevID.setMaximumHeight(50)
        self.textboxDevID.move(190, 16)
        self.textboxDevID.resize(50,40)
        
        #Record indicator label
        self.recordIndicatorLabel = QLabel(self.recordStateIndicator,self) 
        self.recordIndicatorLabel.setMinimumWidth(300)
        self.recordIndicatorLabel.move(30,120)
        self.recordIndicatorLabel.setFont(largefont)
        
        #cough count label
        coughCountLabel = QLabel('Coughs Counted:',self)
        coughCountLabel.setMinimumWidth(100)
        coughCountLabel.setFont(largefont)
        
        #cough count lcd display
        self.coughCountDisplay = QLCDNumber(self)
        self.coughCountDisplay.setMinimumHeight(50)
        self.coughCountDisplay.setMinimumWidth(100)
        self.coughCountDisplay.display(self.coughCount)
        
        #Indicate input device ID
        self.promptDeviceIDLabel = QLabel('Enter device ID:\n(REQUIRED)',self) 
        self.promptDeviceIDLabel.setMinimumWidth(10)
#         self.promptDeviceIDLabel.setMaximumWidth(150)
        self.promptDeviceIDLabel.move(10,20) 
        self.promptDeviceIDLabel.setFont(largefont)
#         self.promptDeviceIDLabel.setAcceptDrops()
#         self.statusBar()
        
        #Button for recording
        self.recordBtn = QPushButton('Start Recording', self)
        self.recordBtn.setToolTip('Press this button to begin recording the trial')
        self.recordBtn.move(30,80) 
        self.recordBtn.released.connect(self.recordButtonClicked)
        self.recordBtn.setFont(normalfont)
        
        stoprecordBtn = QPushButton('STOP Recording', self)
        stoprecordBtn.setToolTip('Press this button to STOP Recording data')
        stoprecordBtn.move(190,80) 
        stoprecordBtn.released.connect(self.stopRecordingButtonClicked)
        stoprecordBtn.setFont(normalfont)

        #layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        settingsBox = QGroupBox('Settings')
        settingsBox.setFont(smallfont)
#         settingsBoxLayout = QHBoxLayout() #probably should be grid layout
#         settingsBoxLayout = QFormLayout()
        settingsBoxLayout = QGridLayout()
        settingsBoxLayout.setSpacing(10)
        settingsBoxLayout.addWidget(self.promptDeviceIDLabel,1,0)
        settingsBoxLayout.addWidget(self.textboxDevID,1,1,alignment=Qt.AlignCenter)
#         settingsBoxLayout.addRow(self.promptDeviceIDLabel, self.textboxDevID)
        settingsBox.setLayout(settingsBoxLayout)
#         settingsBoxLayout.addWidget(self.promptDeviceIDLabel)
#         settingsBoxLayout.addWidget(self.textboxDevID)
        
        ctrlBox = QGroupBox('Recording')
        ctrlBox.setFont(smallfont)
        ctrlBoxLayout = QGridLayout() #probably should be grid layout
#         ctrlBoxLayout.setSpacing(10)
        ctrlBox.setLayout(ctrlBoxLayout)
        ctrlBoxLayout.addWidget(self.recordBtn,1,0)
        ctrlBoxLayout.addWidget(stoprecordBtn,1,1)
        ctrlBoxLayout.addWidget(coughCountLabel,2,0,alignment=Qt.AlignCenter)
        ctrlBoxLayout.addWidget(self.coughCountDisplay,2,1,alignment=Qt.AlignCenter)
        
        statusBox = QGroupBox('Status')
        statusBox.setFont(smallfont)
        statusBoxLayout = QVBoxLayout() #probably should be grid layout
        statusBox.setLayout(statusBoxLayout)
        statusBoxLayout.addWidget(self.recordIndicatorLabel,alignment=Qt.AlignCenter)
        
#         statusBoxLayout.addWidget(stoprecordBtn)
        
        layout.addWidget(settingsBox)
        layout.addWidget(ctrlBox)
        layout.addWidget(statusBox)
        
        
        self.textboxDevID.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)   
    
    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(QSize(self.width,self.height))
        
#         QMessageBox.question(self, 'PyQt5 message', "Do you want to save?",QMessageBox.Ok, QMessageBox.Ok)


#         devIDwarning = QMessageBox()
#         devIDwarning.setText( "Please enter a valid device ID. \nValid device IDs can only be integers greater than 0.")
#         devIDwarning.setIcon(QMessageBox.Warning)
#         devIDwarning.show()
        self.show()
        
#     def testPrint(self):
#         print('If this message is printed before the label text changes, you\'re screwed')
    
    #This function is called to update the Label indicating if we are recording
    def updateRecordStatusLabel(self,statusStr):
        self.recordIndicatorLabel.setText(statusStr)

#     def displayQMessage(self,messagetouser):
#         reply = QMessageBox.question(self, 'Message',
#         messagetouser, QMessageBox.Yes | 
#         QMessageBox.No, QMessageBox.No)

    #--- Redefine Exit function to ensure that the application closes----------
    def closeEvent(self, *args, **kwargs):
        
        self.stopRecord = True
        return QWidget.closeEvent(self, *args, **kwargs)
    #--------------------------------------------------------------------------
#     def playSound(self, devID):
#         def callback0():
#             winsound.Beep( 1000+self.deviceID*100, 1500)
#             
#         def callback1():
#             
#             winsound.Beep( 1000-self.deviceID*100, 1500)
#         t0 = threading.Thread(target = callback0)
#         t0.start()
#         t1 = threading.Thread(target = callback1)
#         t1.start()
    def recordButtonClicked(self):
        #1. create new file given device ID
            #maybe allow to select the folder
            #1a. check for old files with name, rename
            #create file and then
        #code for where pressing the C button will record the cough
        #Update status label

        #if currently record
#         if not self.currentlyRecording:

            #----- Check to see if the device ID is valid ---------------------------------------------------------------------------------------
            try:
                    self.deviceID = int(self.textboxDevID.text())
            except (RuntimeError, TypeError, NameError,ValueError):
                QMessageBox.critical(self, 'Error',  "Please enter a valid device ID. \nValid device IDs can only be integers (whole numbers) greater than 0.", QMessageBox.Ok)
                return
            
            if self.deviceID<0:
                QMessageBox.critical(self, 'Error',  "Please enter a valid device ID. \nValid device IDs can only be integers (whole numbers) greater than 0.", QMessageBox.Ok)
                return
            #------------------------------------------------------------------------------------------------------------------------------------
            
            def callback():
                self.coughCount = 0
                self.recordBtn.setEnabled(False)
                self.currentlyRecording=True
                execpath = os.getcwd() 
                datapath = execpath + '/Data/'
                if not os.path.exists(datapath):
                    os.makedirs(datapath)
                i = 0
                for root, dirs, files in os.walk(datapath):
                    for file in files:
                        if file.endswith(".txt"):   
                            if ((i == int(file[18]) and self.deviceID == int(file[6])) or i>1000):
                                i+=1
                                continue
                            else:
                                break
                newfilename = datapath+'Device'+str(self.deviceID)+'GroundTruth'+str(i)+'.txt'
                txtfile = open(newfilename, 'w')
#                 print(self.deviceID)
#                 self.testPrint()
                #create directory to 
                #Play the indicator tone
                time.sleep(1)
                winsound.Beep( 1000+self.deviceID*100, 1500)
#                 self.playSound(self.deviceID)
                
                self.updateRecordStatusLabel('Current Status: Recording NOW.\nPress "Stop" to halt recording')                
                
                
                # Get the new file to write into here
                
                #Simulate writing to file for now
                i, total = 0,0
                t0 = time.time()
                
                #----- File write loop---------------------
                while True:
                    
                    txtfile.write(str(time.time()-t0) + ', '+ str(self.currentlyCoughing)+'\n')
#                     print('Time:',time.time()-t0,'\t','Cough Truth:\t',self.currentlyCoughing)
                   
                    i+=1
                    if(self.stopRecord):
                        self.recordBtn.setEnabled(True)
                        print(self.coughCount)
                        return
                    time.sleep(.000001)
                print(time.time()-t0)
                
            #----- Initialize File IO Thread---------------------
            t = threading.Thread(target = callback)
            t.start()
        
    

    
    
    def stopRecordingButtonClicked(self):

        self.stopRecord = True
        time.sleep(0.01)
        self.stopRecord = False
        self.updateRecordStatusLabel('Current Status: NOT Recording.\nClick "Start Recording" To begin recording')
        
'''
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()
'''
            
            
#---Problem code----------------- old way of handling events
#     @pyqtSlot()
#     def on_click_record(self):
#         #check if valid device id is given here first
#         self.updateRecordStatus('Current Status: Recording NOW')
#         self.deviceID = int(self.textboxDevID.text())
#         print(self.deviceID)
#         
#         self.testPrint()
#         time.sleep(4)
#         #play the sound
#         #winsound.Beep(1000+self.deviceID*100, 3000)
#         winsound.Beep( 1000+self.deviceID*100, 3000)
#         
#     def on_click_stop(self):
#         self.updateRecordStatus('Current Status: Recording done, Ready for next trial')
#----- Problem code------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CoughRecorderGUI()
    sys.exit(app.exec_())  

'''
def main():
    
    w = QWidget();
    w.setFixedSize(250,150)
    w.move(300,300)
    w.setWindowTitle('Cough Data')
    w.show()
    sys.exit(app.exec_())
   ''' 