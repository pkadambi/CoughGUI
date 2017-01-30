'''
Created on Jan 26, 2017

@author: Prad
'''
import numpy as np
import sys
import winsound
import time
import pyaudio
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QSplitter, QFrame, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QHBoxLayout

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
        self.currentlyCoughing = False
        self.recordStateIndicator = 'Current Status: NOT Recording'
        self.deviceID=-1
        self.initUI()          
    #set coughingCurrently to 1 when button pressing
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_C:
            self.currentlyCoughing = False         
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_C:
            self.currentlyCoughing = True 

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
        
        self.textboxDevID = QLineEdit(self)
        self.textboxDevID.move(190, 16)
        self.textboxDevID.resize(50,20)
        
        #Record indicator label
        self.recordIndicatorLabel = QLabel(self.recordStateIndicator,self) 
        self.recordIndicatorLabel.setFixedWidth(300)
        self.recordIndicatorLabel.move(30,120)
        
        #Indicate input pID
        self.promptDeviceIDLabel = QLabel('Enter device ID (REQUIRED):',self) 
        self.promptDeviceIDLabel.setFixedWidth(150)
        self.promptDeviceIDLabel.move(30,20) 
#         self.statusBar()
        
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
        
    def testPrint(self):
        print('If this message is printed before the label text changes, you\'re screwed')
    
    #This function is called to update the Label indicating if we are recording
    def updateRecordStatusLabel(self,statusStr):
        self.recordIndicatorLabel.setText(statusStr)

#     def displayQMessage(self,messagetouser):
#         reply = QMessageBox.question(self, 'Message',
#         messagetouser, QMessageBox.Yes | 
#         QMessageBox.No, QMessageBox.No)
#     
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
                self.recordBtn.setEnabled(False)
                self.currentlyRecording=True
                #Get the device id
    #             try:
    #                 self.deviceID = int(self.textboxDevID.text())
    #             except (RuntimeError, TypeError, NameError,ValueError):
    #                 #self.displayQMessage("Are you fucking retarded, a device id should be an integer")
    #                 QMessageBox.question(self, 'PyQt5 message', "Do you want to save?",QMessageBox.Ok, QMessageBox.Ok)
                    
    #                 devIDwarning = QMessageBox()
    #                 devIDwarning.setText( "Please enter a valid device ID. \nValid device IDs can only be integers greater than 0.")
    #                 devIDwarning.setIcon(QMessageBox.Critical)
    #                 devIDwarning.setStandardButtons(QMessageBox.Ok)
    #                 devIDwarning.show()
                    #QMessageBox(self, "Ok", "Done.", QMessageBox.NoButton)
    #                 QMessageBox.warning(None, "Invalid input", "Fill every blank.")
                    #devIDwarning = QMessageBox.Information(self, 
                    #                                      'Error',
                    #                                       "Please enter a valid device ID. \nValid device IDs can only be integers greater than 0.",QMessageBox.Yes | 
    #                                                        QMessageBox.No, QMessageBox.No)
    #                 return
                    
                print(self.deviceID)
                self.testPrint()
                #create directory to 
                #Play the indicator tone
                time.sleep(1)
                winsound.Beep( 1000+self.deviceID*100, 1500)
                self.updateRecordStatusLabel('Current Status: Recording NOW')                
                #Simulate writing to file for now
                i, total = 0,0
                t0 = time.time()
                
                while True:
                    time.sleep(.000001)
                    print('Time:',time.time()-t0,'\t','Cough Truth:\t',self.currentlyCoughing)
                   
                    i+=1
                    if(self.stopRecord):
                        self.recordBtn.setEnabled(True)
                        return
                
                print(time.time()-t0)
                
                
            t = threading.Thread(target = callback)
            t.start()
        
    


    
    def stopRecordingButtonClicked(self):

        self.stopRecord = True
        #print('FuckThis')
        time.sleep(0.2)
        self.stopRecord = False
        self.updateRecordStatusLabel('Current Status: NOT Recording')
        
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