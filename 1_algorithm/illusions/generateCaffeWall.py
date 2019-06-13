import numpy as np

def generateCaffeWall(image,thickLine=1,squareSize=15,rows=4):
  
  sizeImg = image.shape[0]
  numSquares = int(sizeImg/(squareSize*2))+1
  
  squareAxis = int(sizeImg/2-(rows*squareSize)/2)
  squareColumn = int(squareSize/2)
  initColum = int(squareSize/2)

  for row in range(rows): 
    


    for column in range(numSquares):

      image[squareAxis:squareAxis+squareSize,squareColumn:squareColumn+squareSize] = 0

      squareColumn += 2*squareSize


    if(row+1<rows):
      image[squareAxis+squareSize:squareAxis+squareSize+ thickLine,:] = 0.6


    squareAxis += squareSize + thickLine
    initColum += int(squareSize/2)
    squareColumn = int(squareSize/2)

    if(initColum <=(squareSize)):

      squareColumn += int(squareSize/2) 

    else:
      squareColumn = int(squareSize/2)
      initColum = int(squareSize/2)
      
      
  return image