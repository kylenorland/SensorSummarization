import numpy as np
import cv2 as cv
from PIL import Image
import PIL.ImageOps
from PIL import ImageChops
import io
import os
from collections import defaultdict
import glob2 as glob

percentDiff = 0
pixelsDiff = 0
hsv = None



"""
lower_topColor = np.array([50,20,5])
upper_topColor = np.array([150,70,200])
"""




def checkMotion(baseImage, imageInQuestion):
    global percentDiff
    global pixelsDiff
    global hsv
    
    #Open the images and get their difference
    im1 = Image.open(baseImage)
    im2 = Image.open(imageInQuestion)
    diff=ImageChops.difference(im1, im2)
    #diff.save("differencePicture.jpg")
    invertedImage = diff

    #Close the originals
    im1.close()
    im2.close()
        
    #Get diff image and invert it
    #invertedImage = Image.open('differencePicture.jpg')
    image = PIL.ImageOps.invert(invertedImage)
    image.save('originalImage.jpg')
    im = cv.imread('originalImage.jpg')

    #Convert color to hsv
    hsv = cv.cvtColor(cv.blur(im,(5,5)), cv.COLOR_BGR2HSV)

    #Create mask of diff and apply it. This checks if a person was there.
    lower_diffColor = np.array([0,0,0])
    upper_diffColor = np.array([360,360,200])
    diffMask = cv.inRange(hsv, lower_diffColor, upper_diffColor)
    res = cv.bitwise_and(im,im, mask= diffMask)

    #Print the diff image and its percentage
    #cv.imshow('res',res)
    
    nonZeroDiff = cv.countNonZero(diffMask)
    pixelsDiff = nonZeroDiff
    totalPixels = 2048*1536
    percentDiff =(nonZeroDiff/totalPixels)
    #print(nonZeroDiff/totalPixels)

    #Return the difference picture (in cv form)
    return im;

def checkColors(im, topColor, bottomColor):
    global hsv
    global pixelsDiff
    
    #Create mask for top color(blue) and apply it
    lower_topColor = np.array([50,42,5])
    upper_topColor = np.array([150,70,200])
    topMask = cv.inRange(hsv, lower_topColor, upper_topColor)
    topFound = cv.bitwise_and(im,im, mask= topMask)

    #Create mask for bottom color(black) and apply it
    lower_bottomColor = np.array([50,2,5])
    upper_bottomColor = np.array([150,42,140])
    bottomMask = cv.inRange(hsv, lower_bottomColor, upper_bottomColor)
    bottomFound = cv.bitwise_and(im,im, mask=bottomMask)

    #Count the nonzero pixels in each image
    
    nonZeroBottom = cv.countNonZero(bottomMask)
    nonZeroTop = cv.countNonZero(topMask)
    totalPixels = 2048*1536

    bottomRatio = (nonZeroBottom/pixelsDiff)
    topRatio = (nonZeroTop/pixelsDiff)
    
    print("black percent= " + str(bottomRatio))
    print("blue percent= " + str(topRatio))

    #print(cv.countNonZero(bottomMask))
    #print(cv.countNonZero(topMask))

    #Print the images
    #cv.imshow('topMask', topMask)
    #cv.imshow('bottomMask', bottomMask)
    #cv.imshow('bottom', bottomFound)
    #cv.imshow('top', topFound)

    #Return true if the colors comprise a decent amount of the found image
    if(bottomRatio+topRatio > 0.1):
        return True;
    else:
        return False;
    
def checkPerson(desiredCamera, startTime, endTime):

    #Get base path
    baseImage = "floor2BaseImages/" + str(desiredCamera) + ".jpg"
    filePath = "AllCameraImages\\" + str(desiredCamera)
    counter = 0
    blue = "blue"
    black = "black"
    
    """
    #Individual test
    baseImage = "AllCameraImages/10/10-20180718164158358.jpg"
    imageInQuestion ="AllCameraImages/10/10-20180718164056750.jpg"
    diffImage = checkMotion(baseImage, imageInQuestion)
    return False;
    """
    foundFile = False                                #Check if the photo has been found

    #Get the image that matches the time frame
    photosFound = []                                      #Grab the photos that match the search
    searchString = filePath + "\\"+str(desiredCamera) +"-"+ str(startTime)+"*.jpg"
    searchString2 = filePath + "\\"+str(desiredCamera) +"-"+ str(startTime+1)+"*.jpg"
    photosFound = glob.glob(searchString)                   #Add the photos found to the array
    photosFound.extend(glob.glob(searchString2))
    #print(photosFound)
    if str(photosFound) !="[]":
        print(photosFound[0])
    else:                                                   #If no image is in that range (Should be rare)
        topReturn = dict()
        topReturn['personFound'] = False
        topReturn['photoName']="No photo found in time frame"
        return topReturn

    imageInQuestion = photosFound[0]                        #Set the image in question to the one found

    
    newIm = Image.open(imageInQuestion)
    diffImage = checkMotion(baseImage, imageInQuestion)
    #print(percentDiff)

    if (percentDiff > 0.001):                           #If a person was detected 
        #print(imagePath +" " + "has motion")
        counter +=1
        photoTitle = ("FoundImages/" +str(desiredCamera)+"-"+str(startTime)+".jpg")
        #cv.imwrite(photoTitle,diffImage)
        newIm.save(photoTitle)
        newIm.close()

        topReturn = dict()
        topReturn['personFound'] = True
        topReturn['photoName']=photoTitle
        foundFile = True
        return topReturn;
        """
        if(checkColors(diffImage, blue, black)==True):
            newIm.save(photoTitle)
            newIm.close()
            return True;
        else:
            newIm.close()
            return False;
        """
        #print(checkColors(diffImage, blue, black))                
    else:
        newIm.close()
        topReturn = dict()
        topReturn['personFound'] = False
        topReturn['photoName']="No photo found checked"
        foundFile = True
        return topReturn;            
        

            
#########################################################################
                           # MAIN
#########################################################################
#Initial Variables

desiredCamera = 10
startTime = 164141
endTime = 164230

#Run the method
result = checkPerson(desiredCamera,startTime, endTime)
print(result['personFound'])

"""

#Save the result image


#cv.imwrite('ResultImage.jpg',res)

#cv.waitKey(0)
#cv.destroyAllWindows()


"""
"""
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 50, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


#

#Finds the biggest contour
image_with_contours = cv.drawContours(im, contours, -1, (0,255,0), 3)
cv.imshow("Contours", image_with_contours)
cv.waitKey(5000)
cv.killAllWindows()
"""
