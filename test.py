'''
Created on Jan 23, 2017

@author: Prad
'''
import winsound
#import numpy as np

#import pygame

#data = np.random.uniform(-1,1,44100)
#scaled = np.int16(data/np.max(np.abs(data))*32767)
a = 500+600
a=int('')
c = a+30
print(c)
winsound.Beep(a,500)
#winsound.Beep(300,500)
#winsound.Beep(400,500)
#winsound.Beep(500,500) 
#winsound.Beep(600,500)
#winsound.Beep(700,500)
#winsound.Beep(800,500)
#winsound.Beep(900,500)
#winsound.PlaySound(scaled)



#this is the sound that indicates start speaking
#winsound.MessageBeep(winsound.MB_OK)


'''
import os.path
import pygame.mixer, pygame.time, pygame.sndarray
mixer = pygame.mixer
sndarray = pygame.sndarray
time = pygame.time
from math import sin
from Numeric import *


#choose a desired audio format

mixer.init(11025, 16, 0) #raises exception on fail

print mixer.get_init()

sound = mixer.Sound('data/secosmic_lo.wav')



a1 = sndarray.array(sound)
print 'SHAPE1:', a1.shape

length = a1.shape[0]
myarr = zeros(length+12000)
myarr[:length] = a1
myarr[3000:length+3000] += a1>>1
myarr[6000:length+6000] += a1>>2
myarr[9000:length+9000] += a1>>3
myarr[12000:length+12000] += a1>>4

print 'SHAPE2:', myarr.shape
sound2 = sndarray.make_sound(myarr.astype(Int16))
sound2.play()

while mixer.get_busy():
    time.wait(200)
'''