#!/usr/bin/python
# -*- coding: utf-8 -*-

# Loop over individual trials as input for ASTEREX 	#
# Step 2                                           	#
# Script by: Branden Bio						    #
# Version 4.0                                 		#
# Date created: 07/14/2023                     		#
# Date updated: 02/15/2024                     		#

import os
from os import path
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import re

if len(sys.argv) <= 5:
    print('ERROR: Please provide experiment name, cellsize, celloffset, distance, and compression as arguments.')
    exit(1)

currExp = str(sys.argv[1])
cs = str(sys.argv[2])
co = str(sys.argv[3])
dist = str(sys.argv[4])
com = str(sys.argv[5])

start_time = datetime.now()
start_string = start_time.strftime("%d/%m/%Y %H:%M:%S")

print('****************')
print('Script start:')
print(start_string)
print('****************')

os.chdir(os.path.expanduser(r'~/Repository/Models/ASTEREX/'))

# Setup directories
simFile = os.path.expanduser(r'~/Repository/Models/ASTEREX/out/simulation.csv')
homeDir = str(Path(__file__).parent.resolve())
currExpDir = homeDir + '/' + currExp + '/'
jsnDir = currExpDir + 'labels/'
outputDir = currExpDir + 'simulations/'

# Read in problem configuration file and create config matrix
configArray = []
with open(currExpDir + "problemConfig.txt","r") as config:
    lines = config.readlines()
    for line in lines:
        configArray.append(line.replace('\n', ''))
    config.close()

# Run Asterex on each trial json
for filename in os.listdir(jsnDir):
    if filename.endswith('.json'):
        file = os.path.join(jsnDir, filename)
        probNumber = re.findall(r'\d+', filename)
        probIndex = int(probNumber[0])-1
        currProblem = configArray[probIndex].split(',')
        direction = currProblem[1]
        target = currProblem[2]
        filename = filename.split('.')[0]
        outName = "{}_sim_cs{}_co{}_d{}_com{}.csv".format(filename,cs,co,dist,com)
        # Setup direction query input
        if direction == "left" or direction == "right":
            prompt = r"what is to the " + direction + " of the " + target
        elif direction == "above" or direction == "below":
            prompt = r"what is " + direction + " the " + target
        # Run asterex on JSON for each problem
        print('**********************')
        print('{} running!'.format(filename))
        #print('Prompt: {}'.format(prompt))
        print('**********************')
        subprocess.run(['python3', 'ASTEREX.py', '--input', file, '--vstm', 'initialize', \
        '--focus', prompt, '--simulate', '100', '--output', outName, '--cellsize', cs, \
        '--cellscalar', '1.0', '--celloffset', co, '--distance', dist, '--compression', com])
        print('**********************')
        print('{} complete!'.format(filename))
        print('**********************')
        #tFile = os.path.join(outputDir, 'simulation.csv')
        #oFile = os.path.join(outputDir + filename + '_simulation.csv')
        #if os.path.exists(simFile) != False:
        #    subprocess.run(['mv', simFile, outputDir])
        #    os.rename(tFile, oFile)
        #if os.path.exists(oFile) != False:
        #    print('**********************')
        #    print('{} completed!'.format(filename))
        #    print('**********************')
        #else:
        #    print('********************')
        #    print('{} not completed'.format(filename))
        #    print('********************')
end_time = datetime.now()
end_string = end_time.strftime("%d/%m/%Y %H:%M:%S")
print('****************')
print(end_string)
print('Script complete!')
print('****************')
