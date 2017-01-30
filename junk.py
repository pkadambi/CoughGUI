'''
Created on Jan 29, 2017

@author: Prad

import time
start = time.time()

time.sleep(0.000001)
end = time.time() - start
print(end)


import os
import glob
path = os.getcwd() 
newfilename = 'Trial'
i = 0
for root, dirs, files in os.walk(path+'/Data'):
    for file in files:
        if file.endswith(".txt"):   
            if i == int(file[5]) or i>30:
                i+=1
                continue
print(i)
#        
#            path_file = os.path.join(file)
#            print(path_file)

currentlyCoughing=1
import os
import time
path = os.getcwd() 
newfilename = 'Trial'
i = 0
for root, dirs, files in os.walk(path+'/Data'):
    for file in files:
        if file.endswith(".txt"):   
            if i == int(file[11]) or i>30:
                i+=1
                continue
            else:
                break
print(i)
fn = path+'/Data/'+'GroundTruth'+str(i)+'.txt'


txtfile = open(fn, 'w')
t0 = time.time()
time.sleep(0.0001)
print(time.time()-t0)
txtfile.write(str(time.time()-t0) + ', '+ str(currentlyCoughing))
'''

asdf=1
if(asdf):
    print('pythons cool')
else:
    print('screw python')
#0.0010030269622802734