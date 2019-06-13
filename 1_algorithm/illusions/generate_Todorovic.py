# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 14:15:32 2018

@author: root
"""
# Libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

def generateTodorovic(outputSize, height, factor, colors):
    #Parameters
    #outputSize = 128 # Size of the output image
    #height = 0.1 # Height of the target
    #spatialFreq = 0.05 #size of the inducer patter with respect to image size
    
    # Target position

    
    # Colors
    lightInducerR = colors[0,0]
    lightInducerG = colors[0,1]
    lightInducerB = colors[0,2]
    
    darkInducerR = colors[1,0]
    darkInducerG = colors[1,1]
    darkInducerB = colors[1,2]
    
    targetR = colors[2,0]
    targetG = colors[2,1]
    targetB = colors[2,2]

  
    
    
    image = np.ones((outputSize,outputSize,3))
    
    image[:,0:round(outputSize/2),0] = lightInducerR
    image[:,0:round(outputSize/2),1] = lightInducerG
    image[:,0:round(outputSize/2),2] = lightInducerB
    
    
    image[:,round(outputSize/2):-1,0] = darkInducerR
    image[:,round(outputSize/2):-1,1] = darkInducerG
    image[:,round(outputSize/2):-1,2] = darkInducerB
    
    
    # Left target
    leftTargetX = round(outputSize/4)
    leftTargetY = round(outputSize/2)



    image[leftTargetY-round(height/2):leftTargetY+round(height/2),
          leftTargetX-round(height/2):leftTargetX+round(height/2),0] = targetR     
                
                      
    
    image[leftTargetY-round(height/2):leftTargetY+round(height/2),
          leftTargetX-round(height/2):leftTargetX+round(height/2),1] = targetG        

          
    image[leftTargetY-round(height/2):leftTargetY+round(height/2),
          leftTargetX-round(height/2):leftTargetX+round(height/2),2] = targetB



    factor = 0.15
    dispX = [round(-height*factor),round(height*factor),round(-height*factor),round(height*factor)]
    dispX2 = [height,0,height,0]
    dispX3 = [0,height,0,height]


    dispY = [round(-height*factor),round(-height*factor),round(height*factor),round(height*factor)]
    dispY2 = [height,height,0,0]
    dispY3 = [0,0,height,height]

    for i in range(4):


        image[leftTargetY+dispY[i]-dispY2[i]:leftTargetY+dispY[i]+dispY3[i],
          leftTargetX+dispX[i]-dispX2[i]:leftTargetX+dispX[i]+dispX3[i],0] = darkInducerR

        image[leftTargetY+dispY[i]-dispY2[i]:leftTargetY+dispY[i]+dispY3[i],
          leftTargetX+dispX[i]-dispX2[i]:leftTargetX+dispX[i]+dispX3[i],1] = darkInducerG

        image[leftTargetY+dispY[i]-dispY2[i]:leftTargetY+dispY[i]+dispY3[i],
          leftTargetX+dispX[i]-dispX2[i]:leftTargetX+dispX[i]+dispX3[i],2] = darkInducerB




          
    # Right target

    rightTargetX = round(outputSize/4)+round(outputSize/2)
    rightTargetY = round(outputSize/2)


    image[rightTargetY-round(height/2):rightTargetY+round(height/2),
          rightTargetX-round(height/2):rightTargetX+round(height/2),0] = targetR      
                
                      
    
    image[rightTargetY-round(height/2):rightTargetY+round(height/2),
          rightTargetX-round(height/2):rightTargetX+round(height/2),1] = targetG              

          
    image[rightTargetY-round(height/2):rightTargetY+round(height/2),
          rightTargetX-round(height/2):rightTargetX+round(height/2),2] = targetB                

    for i in range(4):


        image[rightTargetY+dispY[i]-dispY2[i]:rightTargetY+dispY[i]+dispY3[i],
          rightTargetX+dispX[i]-dispX2[i]:rightTargetX+dispX[i]+dispX3[i],0] = lightInducerR

        image[rightTargetY+dispY[i]-dispY2[i]:rightTargetY+dispY[i]+dispY3[i],
          rightTargetX+dispX[i]-dispX2[i]:rightTargetX+dispX[i]+dispX3[i],1] = lightInducerG

        image[rightTargetY+dispY[i]-dispY2[i]:rightTargetY+dispY[i]+dispY3[i],
          rightTargetX+dispX[i]-dispX2[i]:rightTargetX+dispX[i]+dispX3[i],2] = lightInducerB


    return image

