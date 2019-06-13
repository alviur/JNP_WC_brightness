# Libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

'''
 def makeCheckerboardPattern(self):
    spacing = self.square_size
    xspacing = (self.width - self.cols * self.square_size) / 2.0
    yspacing = (self.height - self.rows * self.square_size) / 2.0
    for x in range(0,self.cols):
      for y in range(0,self.rows):
        if x%2 == y%2:
          square = SVG("rect", x=x * spacing + xspacing, y=y * spacing + yspacing, width=spacing, height=spacing, fill="black", stroke="none")
          self.g.append(square)

'''

def generate_checkerboard(spacing,size):

	width = height = size
	cols = rows = round(height/spacing)

	square_size = spacing
	xspacing = round((width - cols *square_size) / 2)
	yspacing = round((height - rows *square_size) / 2)


	whiteFlag = False
	blackFlag = False

	targetRow = round(rows/2)


	outImg = np.ones((height,width))

	for x in range(0,cols):
		for y in range(0,rows):

			if x%2 == y%2:

				cv2.rectangle(outImg, (x * spacing + xspacing,y * spacing + yspacing), (x * spacing + xspacing+spacing-1,y * spacing + yspacing+spacing-1),(0,0,0),-1,0)

				if(y+1>=targetRow and x+1>=targetRow and blackFlag==False and y<x):

					cv2.rectangle(outImg, (x * spacing + xspacing,y * spacing + yspacing), (x * spacing + xspacing+spacing-1,y * spacing + yspacing+spacing-1),(0.5,0.5,0.5),-1,0)
					blackFlag=True




			if(y+1>=targetRow and x+1>=targetRow and whiteFlag==False and x%2 != y%2):


				cv2.rectangle(outImg, (x * spacing + xspacing,y * spacing + yspacing), (x * spacing + xspacing+spacing-1,y * spacing + yspacing+spacing-1),(0.5,0.5,0.5),-1,0)
				whiteFlag=True


	return outImg
