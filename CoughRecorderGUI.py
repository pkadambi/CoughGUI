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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QSplitter, QFrame, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QHBoxLayout, QSize

class CoughRecorderGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Cough Trial Tool'
        self.left = 300
        self.top = 300
        self.right = 200
        self.width = 300
        self.height = 200
        self.currentlyRecording=False
        self.stopRecord = False
        self.currentlyCoughing = 0
        self.coughCount = 0
        self.recordStateIndicator = 'Current Status: NOT Recording.\nClick "Record" To start recording'
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

    def initUI(self):
        hbox = QHBoxLayout(self)
        
        #Top, middle, and bottom pannels initialized for Settings, Record, and Status areas
        topSettingsFrame = QFrame(self)
        topSettingsFrame.setFrameShape(QFrame.StyledPanel)      
        
        
        middleRecordFrame = QFrame(self)
        middleRecordFrame.setFrameShape(QFrame.StyledPanel) 
        
        
        bottomStatusFrame = QFrame(self)
        bottomStatusFrame.setFrameShape(QFrame.StyledPanel) 
        
        
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(topSettingsFrame)
        splitter1.addWidget(middleRecordFrame)
        splitter1.addWidget(bottomStatusFrame)
        
        self.setLayout(hbox)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(QSize(self.width,self.height))
        self.textboxDevID = QLineEdit(self)
        self.textboxDevID.move(190, 16)
        self.textboxDevID.resize(50,40)
        
        #Record indicator label
        self.recordIndicatorLabel = QLabel(self.recordStateIndicator,self) 
        self.recordIndicatorLabel.setFixedWidth(300)
        self.recordIndicatorLabel.move(30,120)
        
        #Indicate input device ID
        self.promptDeviceIDLabel = QLabel('Enter device ID (REQUIRED):',self) 
        self.promptDeviceIDLabel.setFixedWidth(150)
        self.promptDeviceIDLabel.move(30,20) 
#         self.statusBar()
        
        #Button for recording
        self.recordBtn = QPushButton('Record', self)
        self.recordBtn.setToolTip('Press this button to begin recording the trial')
        self.recordBtn.move(30,80) 
        self.recordBtn.released.connect(self.recordButtonClicked)
        
        stoprecordBtn = QPushButton('STOP', self)
        stoprecordBtn.setToolTip('Press this button to STOP Recording data')
        stoprecordBtn.move(190,80) 
        stoprecordBtn.released.connect(self.stopRecordingButtonClicked)
        
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
                
                
                self.updateRecordStatusLabel('Current Status: Recording NOW.\nPress "Stop" to stop recording')                
                
                
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
#                     time.sleep(.000001)
                print(time.time()-t0)
                
            #----- Initialize File IO Thread---------------------
            t = threading.Thread(target = callback)
            t.start()
        
    

    
    
    def stopRecordingButtonClicked(self):

        self.stopRecord = True
        time.sleep(0.01)
        self.stopRecord = False
        self.updateRecordStatusLabel('Current Status: NOT Recording.\nClick "Record" To start recording')
        
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