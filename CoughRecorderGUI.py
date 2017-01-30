'''
Created on Jan 23, 2017

@author: Prad
'''
import sys
import winsound
import time
import os
import threading
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit,  QMessageBox, QGridLayout, QLCDNumber
from PyQt5.Qt import QSize, QSizePolicy, QVBoxLayout, QGroupBox, QTabWidget, QTextEdit
#This is the main application
# Other files in the project are not a part of the application

#This is the main application
# Other files in the project are not a part of the application

class CoughRecorderGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Cough Trial Tool'
        self.left = 300
        self.top = 300
        self.right = 200
        self.width = 380
        self.height = 400
        self.currentlyRecording=False
        self.stopRecord = False
        self.currentlyCoughing = 0
        self.coughCount = 0
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
        
        #current status label
        
        currentStatusLabel = QLabel('Current Status:')
        currentStatusLabel.setMinimumWidth(100)
        currentStatusLabel.setFont(largefont)
        
        #Record indicator label
        self.recordIndicatorLabel = QLabel('NOT Recording') 
        self.recordIndicatorLabel.setMinimumWidth(100)
        self.recordIndicatorLabel.move(30,120)
        self.recordIndicatorLabel.setFont(largefont)
        
        
        self.recordInstructionLabel = QLabel('Click "Start Recording" To begin recording.') 
        self.recordInstructionLabel.setMinimumWidth(300)
        self.recordInstructionLabel.setFont(largefont)

        
        coughLabelInstr = QLabel('After starting recording, press \'c\' to record a cough.')
        coughLabelInstr.setMinimumWidth(100)
        coughLabelInstr.setFont(normalfont)
        
        #cough count label
        coughCountLabel = QLabel('Cough Count:',self)
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
        self.recordBtn.setToolTip('Press this button to begin recording the trial.')
        self.recordBtn.move(30,80) 
        self.recordBtn.released.connect(self.recordButtonClicked)
        self.recordBtn.setFont(normalfont)
        
        stoprecordBtn = QPushButton('STOP Recording', self)
        stoprecordBtn.setToolTip('Press this button to STOP Recording data.')
        stoprecordBtn.move(190,80) 
        stoprecordBtn.released.connect(self.stopRecordingButtonClicked)
        stoprecordBtn.setFont(normalfont)

        #layout
        applayout = QVBoxLayout()
        
        
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
        ctrlBox.setMinimumHeight(150)
        ctrlBoxLayout.addWidget(self.recordBtn,1,0)
#         ctrlBoxLayout.setVerticalSpacing(30)
        ctrlBoxLayout.addWidget(stoprecordBtn,1,1)
        ctrlBoxLayout.addWidget(coughLabelInstr,2,0,1,2,alignment=Qt.AlignCenter)
        ctrlBoxLayout.addWidget(coughCountLabel,3,0,alignment=Qt.AlignCenter)
        ctrlBoxLayout.addWidget(self.coughCountDisplay,3,1,alignment=Qt.AlignCenter)
        
        statusBox = QGroupBox('Status')
        statusBox.setFont(smallfont)
        statusBox.setMaximumHeight(100)
#         statusBoxLayout = QVBoxLayout() #probably should be grid layout
        statusBoxLayout = QGridLayout()
        statusBoxLayout.addWidget(currentStatusLabel,1,0,alignment=Qt.AlignCenter)
        statusBox.setLayout(statusBoxLayout)
        statusBoxLayout.addWidget(self.recordIndicatorLabel,1,1,alignment=Qt.AlignCenter)
        statusBoxLayout.addWidget(self.recordInstructionLabel,2,0,1,2,alignment=Qt.AlignCenter)
        
#         statusBoxLayout.addWidget(stoprecordBtn)
        
        applayout.addWidget(settingsBox)
        applayout.addWidget(ctrlBox)
        applayout.addWidget(statusBox)
        
        helpInstructions = QTextEdit()
        helpInstructions.setReadOnly(True)
        helpInstructions.setText('Help instructions would go here.\n\nJunk text has been added in for now since protocol is not completely defined. \n\n\n\n\n\n \nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        
        #create the tabs
        self.tabs = QTabWidget()
        self.appTab = QWidget()
        self.helpTab = QWidget()
        self.appTab.setLayout(applayout)
        
        helplayout = QVBoxLayout()
        helplayout.addWidget(helpInstructions)
        self.helpTab.setLayout(helplayout)
        
        self.tabs.addTab(self.appTab, "Application")
        self.tabs.addTab(self.helpTab,"Help and Instructions")

        self.layout = QVBoxLayout(self)        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        self.textboxDevID.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)   
    
    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(QSize(self.width,self.height))   
        self.show()
        
#     def testPrint(self):
#         print('If this message is printed before the label text changes, you\'re screwed')
    
    #This function is called to update the Label indicating if we are recording
    def updateRecordStatusLabel(self,statusStr):
        self.recordIndicatorLabel.setText(statusStr)
        
    def updateRecordInstructionLabel(self,statusStr):
        self.recordInstructionLabel.setText(statusStr)

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
                self.updateCoughCount(self.coughCount) 
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
                
                self.updateRecordStatusLabel('Recording NOW')                
                self.updateRecordInstructionLabel('    Press "Stop" to halt recording.')
                
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
#                         print(self.coughCount)
                        return
                    time.sleep(.000001)
#                 print(time.time()-t0)
                
            #----- Initialize File IO Thread---------------------
            t = threading.Thread(target = callback)
            t.start()
        
    

    
    
    def stopRecordingButtonClicked(self):

        self.stopRecord = True
        time.sleep(0.01)
        self.stopRecord = False
        self.updateRecordStatusLabel('NOT Recording')                
        self.updateRecordInstructionLabel('Click "Start Recording" to begin recording.')
        
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