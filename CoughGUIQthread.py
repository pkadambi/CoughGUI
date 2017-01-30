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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QSplitter, QFrame
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QHBoxLayout

class CoughGUIQthread(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Cough Data Recorder Tool'
        self.left = 300
        self.top = 300
        self.right = 200
        self.width = 300
        self.height = 200
        self.currentlyRecording=0
        self.stopRecord = False
        self.recordStateIndicator = 'Current Status: NOT Recording'
        self.deviceID=-1
        self.initUI()          
        

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
        recordBtn = QPushButton('Record', self)
        recordBtn.setToolTip('Press this button to begin recording the trial')
        recordBtn.move(30,80) 
        recordBtn.clicked.connect(self.recordButtonClicked)
        
        stoprecordBtn = QPushButton('STOP', self)
        stoprecordBtn.setToolTip('Press this button to STOP Recording data')
        stoprecordBtn.move(190,80) 
        stoprecordBtn.clicked.connect(self.stopRecordingButtonClicked)
        
        self.show()
        
    def testPrint(self):
        print('If this message is printed before the label text changes, you\'re screwed')
    
    #This function is called to update the Label indicating if we are recording
    def updateRecordStatusLabel(self,statusStr):
        self.recordIndicatorLabel.setText(statusStr)

    #def      
    def stopRecordingButtonClicked(self):
        stopRecord = True
        print('FuckThis')
        time.sleep(0.2)
        stopRecord = False
        self.updateRecordStatusLabel('Current Status: NOT Recording')
    def recordButtonClicked(self):
        #1. create new file given device ID
            #maybe allow to select the folder
            #1a. check for old files with name, rename
            #create file and then
        #code for where pressing the C button will record the cough
        
        #Update status label
        self.updateRecordStatusLabel('Current Status: Recording NOW')
            


        
        def callback():
            
            #Get the device id
            self.deviceID = int(self.textboxDevID.text())
            print(self.deviceID)
            self.testPrint()
                
            #Play the indicator tone
            time.sleep(1)
            winsound.Beep( 1000+self.deviceID*100, 1500)
                
            #Simulate writing to file for now
            i, total = 0,0
            start = time.time()
            
            while (i<5000):
                time.sleep(0.00001) #minimum sleep time will be 1ms
                total+=1
                #print(total,self.stopRecord)
                i+=1
                if(self.stopRecord):
                    break
            print(time.time()-start)
            
        t = threading.Thread(target = callback)
        t.start()
        

        
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
    ex = CoughGUIQthread()
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