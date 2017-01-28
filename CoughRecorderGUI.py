'''
Created on Jan 26, 2017

@author: Prad
'''
import numpy as np
import sys
import winsound
import time
import pyaudio
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSlot

class CoughRecorderGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Cough Data Recorder Tool'
        self.left = 300
        self.top = 300
        self.right = 200
        self.width = 300
        self.height = 200
        self.currentlyRecording=0
        self.recordStateIndicator = 'Current Status: NOT Recording'
        self.deviceID=-1
        self.initUI()          

    def initUI(self):
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
        
        recordBtn = QPushButton('Record', self)
        recordBtn.setToolTip('Press this button to begin recording the trial')
        recordBtn.move(30,80) 
        recordBtn.clicked.connect(self.on_click_record)
        
        stoprecordBtn = QPushButton('STOP', self)
        stoprecordBtn.setToolTip('Press this button to STOP Recording data')
        stoprecordBtn.move(190,80) 
        stoprecordBtn.clicked.connect(self.on_click_stop)
        
        self.show()
        
    def testPrint(self):
        return 'If this message is heard before the label text changes, Fuck Python'
    
    def updateRecordStatus(self,statusStr):
        self.recordIndicatorLabel.setText(statusStr)

    def buttonClicked(self):
        sender = self.sender()
        pass
        #code for where pressing the C button will record the cough

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()
            
            
            
#---Problem code-----------------
    @pyqtSlot()
    def on_click_record(self):
        #check if valid device id is given here first
        self.updateRecordStatus('Current Status: Recording NOW')
        self.deviceID = int(self.textboxDevID.text())
        print(self.deviceID)
        
        self.testPrint()
        time.sleep(4)
        #play the sound
        #winsound.Beep(1000+self.deviceID*100, 3000)
        winsound.Beep( 1000+self.deviceID*100, 3000)
        
    def on_click_stop(self):
        self.updateRecordStatus('Current Status: Recording done, Ready for next trial')


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