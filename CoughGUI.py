'''
@god: Prad
    I eat pythons for breakfast.
'''
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
#THIS CODE IS THE OLD WRONG CODE
from PyQt5 import QtGui, QtCore
import numpy as np
import sys
import winsound
import pyaudio
#import ossaudiodev
#from scipy.io.wavefile import write
#from win32gui import SetLayout
'''
data = np.random.uniform(-1,1,44100)
scaled = np.int16(data/np.max(np.abs(data))*32767)
write
'''



class CoughGUI(QtGui.QWidget):
    
    def __init__ (self):
        super(CoughGUI,self).__init__()
        self.createUI()
    
    #def write(time, groundTruth):
    
    #def generateTone(basisVector):
    
    #def playTone():
        
    def createUI(self):
        self.mengLayout = QtGui.QGridLayout()
        self.mengLayout.addWidget(self.recordButton())
        self.setLayout(self.mengLayout)
        self.show()
        
    def recordButton(self):
        frame  = QtGui.QWidget()
        frameLayout = QtGui.QVBoxLayout()
        label = QtGui.QLabel("Record Button")
        frameLayout.addWidget(label)
        frame.setLayout(frameLayout)

        return frame
 
def main():
    app = QtGui.QApplication(sys.argv)
    bs = CoughGUI()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()