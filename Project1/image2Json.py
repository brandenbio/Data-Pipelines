#!/usr/bin/python
# -*- coding: utf-8 -*-

# Run images through YOLO for object detection #
# output JSON files (labels) for modeling use  #
# Step 1                                       #
# Script by: Branden Bio                       #
# Version 4.0                                  #
# Date created: 07/14/2023                     #

from PIL import Image
from glob import glob
import os
from os import path
import subprocess
from pathlib import Path
import torch
import torchvision
import sys

if len(sys.argv) <= 1:
    print('ERROR: Please provide experiment name as argument.')
    exit(1)

os.chdir(Path(__file__).parent.resolve())

homeDir = os.getcwd()

os.chdir(r'yolov5')

import utils
#display = utils.notebook_init()

currExp = str(sys.argv[1])

# Setup directories
expDir = 'detections/' + currExp
baseDir = homeDir + '/yolov5/'
imgDir = homeDir + '/' + currExp + '/images/'
labDir = homeDir + '/' + currExp + '/labels/'
images = [Image.open(img) for img in glob(path.join(imgDir, '*.png'))]
outputDir = baseDir + expDir + '/'
configDir = homeDir + '/' + currExp + '/'
# Fields for JSON content
str0 = r'{"image_size": {"width": *IMGWIDTH*, "height": *IMGHEIGHT*}, "objects": ['
str1 = r'{"label": "*CLASS*", "confidence": *CONFIDENCE*, "dimensions": {"x": *X*, "y": *Y*, "width": *WIDTH*, "height": *HEIGHT*}}, '
str2 = r'{"label": "*CLASS*", "confidence": *CONFIDENCE*, "dimensions": {"x": *X*, "y": *Y*, "width": *WIDTH*, "height": *HEIGHT*}}]}'
# Read in tempConfig file to complete
tempConfigArray = []
with open(configDir + "tempConfig.txt","r") as tempC:
    tempConfigArray = tempC.readlines()
    tempC.close()
configOutputFile = configDir + "problemConfig.txt"

if os.path.exists(configOutputFile):
        subprocess.run(['rm', configOutputFile])

# Run Yolo on each trial image
for i, img in enumerate(images):
    x = i + 1
    imgWidth, imgHeight = img.size
    imgName = imgDir + 'Problem{}.png'.format(x)
    file = Path(outputDir + 'Problem{}'.format(x))
    if os.path.exists(file):
        pass
    else:
        subprocess.run(['python', 'detect.py', \
        '--weights', 'yolov5x.pt', \
        '--project', expDir, \
        '--name', 'currentActive', \
        '--save-txt', \
        '--save-conf', \
        '--source', imgName])
        currFile = outputDir + 'currentActive'
        outFile = outputDir + 'Problem{}'.format(x)
        os.rename(currFile, outFile)
    # Arrays to hold JSON contents 
    classNumArray = []
    classArray = []
    xArray = []
    yArray = []
    widthArray = []
    heightArray = []
    confidenceArray = []
    # Create temp file to store info of interest for JSON
    with open(outputDir + "Problem{}/labels/Problem{}.txt".format(x,x),"r") as ps:
        for line in ps:
            temp = line.split(' ')
            classNumArray.append(temp[0])
            xArray.append(temp[1])
            yArray.append(temp[2])
            widthArray.append(temp[3])
            heightArray.append(temp[4])
            confidenceArray.append(temp[5].replace('\n', ''))
        xArray = [eval(a)*imgWidth for a in xArray]
        yArray = [eval(b)*imgHeight for b in yArray]
        widthArray = [eval(c)*imgWidth for c in widthArray]
        heightArray = [eval(d)*imgHeight for d in heightArray]
        xArray = [str(e) for e in xArray]
        yArray = [str(f) for f in yArray]
        widthArray = [str(g) for g in widthArray]
        heightArray = [str(h) for h in heightArray]
        ps.close()
    # Format temp file contents
    with open(baseDir + "data/coco128.yaml","r") as yaml:
        lines = yaml.readlines()
        for place in classNumArray:
            num = "  {}: ".format(place)
            for line in lines:
                if num in line:
                    temp = line.replace(num, "")
                    classArray.append(temp.replace('\n', '').replace(' ', ''))
                    break
        yaml.close()
    # Create JSON and replace template with contents from temp file
    with open("Problem{}.json".format(x), "a") as json:
        for y in range(5):
            if y == 0:
                data = str0.replace(
                    "*IMGWIDTH*", str(imgWidth)).replace(
                    "*IMGHEIGHT*", str(imgHeight))
            elif 0 <= y <= 3:
                z = y - 1
                data = str1.replace(
                    "*CLASS*", classArray[z]).replace(
                    "*CONFIDENCE*", confidenceArray[z]).replace(
                    "*X*", xArray[z]).replace(
                    "*Y*", yArray[z]).replace(
                    "*WIDTH*", widthArray[z]).replace(
                    "*HEIGHT*", heightArray[z])
            else:
                z = y - 1
                data = str2.replace(
                    "*CLASS*", classArray[z]).replace(
                    "*CONFIDENCE*", confidenceArray[z]).replace(
                    "*X*", xArray[z]).replace(
                    "*Y*", yArray[z]).replace(
                    "*WIDTH*", widthArray[z]).replace(
                    "*HEIGHT*", heightArray[z])
            json.write(data)
        json.close()
        detectionFile = 'Problem{}.json'.format(x)
        dFilePath = labDir + detectionFile
        if os.path.exists(dFilePath):
            subprocess.run(['rm', detectionFile])
            print('{} already exists.'.format(detectionFile))
            pass
        else:
            subprocess.run(['mv', detectionFile, labDir])
    # Append and complete problemConfig.txt file
    with open(configOutputFile, "a") as config:
        target = max(set(classArray), key = classArray.count)
        data = tempConfigArray[i].replace("*TARGET{}*".format(x), target)
        config.write(data)
        config.close()
    print('********************')
    print('Problem {} completed!'.format(x))
    print('********************')
if os.path.exists(configOutputFile):
        subprocess.run(['rm', configDir + "tempConfig.txt"])
print('**********************')
print('All problems complete!')
print('**********************')
