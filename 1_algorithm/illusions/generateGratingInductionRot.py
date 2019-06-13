import numpy as np
import cv2


def generateGratingInductionRot(outputSize, height, spatialFreq, colors,angle):

    #Parameters
    #outputSize = 128 # Size of the output image
    #height = 0.02 # Height of the target
    #spatialFreq = 0.05 #size of the inducer patter with respect to image size
    
    outputSize2 = outputSize*2
    
    
    image = np.ones((outputSize2,outputSize2,3))
    
    # Colors
    lightInducerR = colors[0,0]
    lightInducerG = colors[0,1]
    lightInducerB = colors[0,2]
    
    darkInducerR = colors[1,0]
    darkInducerG = colors[1,1]
    darkInducerB = colors[1,2]
    
    #Background
    image[:,:,0] = colors[2,0]
    image[:,:,1] = colors[2,1]
    image[:,:,2] = colors[2,2]
    
    vericalPos = np.zeros((2,1))
    beginColumn = 0#round(outputSize*0.05)
    vericalPos[0] = 0#int(round(outputSize*0.05))
    stimulusWidth = outputSize-2*beginColumn
    stimulusWidth2 = outputSize2-2*beginColumn
    
    numBars = round(stimulusWidth2/(stimulusWidth*spatialFreq))
    sizeBar = round(stimulusWidth*spatialFreq)
    
    
    vericalPos[1] = int(round(outputSize/2 +(height*outputSize)/2))
    heightStim = int((outputSize-(height*outputSize)-vericalPos[0,0]*2)/2)
    
    # Counters and flags
    cont = 0;
    flagWhite = True;
    flagBlack = True;
    
    
    for j in range(1):
    
        for i in range(numBars):
           
            if((i%2) == 0):
            
                if(sizeBar*i+sizeBar<=outputSize2):
                
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,0] = lightInducerR
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,1] = lightInducerG
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,2] = lightInducerB
                
                else:
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize,0] = lightInducerR
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize,1] = lightInducerG
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize,2] = lightInducerB
        
                  
                
            else:
                if(sizeBar*i+sizeBar<=outputSize2):
                
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,0] = darkInducerR;
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,1] = darkInducerG;
                    image[:,beginColumn+ sizeBar*i:beginColumn+sizeBar*i+sizeBar,2] = darkInducerB;
                    
                else:
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize] = darkInducerR;
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize] = darkInducerG;
                    image[:,beginColumn+ sizeBar*i:beginColumn+outputSize] = darkInducerB;
                
                    
            
      
        
        cont += 1; 
        
        
    # Rotation
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LANCZOS4)
    
    # Cut
    resultCut = result[int(outputSize*0.3):outputSize+int(outputSize*0.3),int(outputSize*0.3):outputSize+int(outputSize*0.3),:]
    
    
    # Induction zone 
    
    heightStim = int((height*outputSize))
    
    resultCut[int(outputSize/2 -heightStim/2):int(outputSize/2 +heightStim/2),:,:] = 0.5
    
    return resultCut