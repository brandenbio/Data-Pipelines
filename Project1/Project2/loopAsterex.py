#!/usr/bin/python
# -*- coding: utf-8 -*-

# Loop over individual trials #
# as input for ASTEREX 	      #
# Step 2                      #
# Script by: Branden Bio	  #
# Version 5.0                 #
# Date created: 07/14/2023    #
# Date updated: 07/10/2024    #

import errno
import os
from os import path
from datetime import datetime
import pandas as pd
import subprocess
import sys

currExp = 'RT1'
cs = str(70)
co = str(0)
dist = str(4)
com = str(0)

start_time = datetime.now()
start_string = start_time.strftime("%d/%m/%Y %H:%M:%S")

print('****************')
print('Script start:')
print(start_string)
print('****************')

# Setup directories
homeDir = os.path.expanduser(r'~/Repository/Projects/Perception/Relational Tracking/modeling/')
expDir = homeDir + currExp + '/'
jsnDir = expDir + 'labels/'
simDir = expDir + 'simulations/'
outputDir = os.path.join(simDir, f'sims_cs{cs}_co{co}_d{dist}_com{com}')
try:
    os.mkdir(outputDir)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

# Read in problem configuration file and create config matrix
columnNames = ['problem','instance','focus']
config = pd.read_csv(os.path.join(expDir, 'uniqueProblemInstances.csv'), names=columnNames, header=None)

os.chdir(os.path.expanduser(r'~/Repository/Models/ASTEREX/'))

for index, row in config.iterrows():
    # Setup inputs for Asterex
    problemNumber = row['problem']
    instanceNumber = row['instance']
    focus = row['focus']
    filename = f'Problem{problemNumber}_Instance{instanceNumber}'
    inputFilename = filename + '.json'
    inputFile = os.path.join(jsnDir, inputFilename)
    outputFile = f'{filename}_sim_cs{cs}_co{co}_d{dist}_com{com}.csv'

    # Run Asterex on JSON for each problem
    print('**********************')
    print('{} running!'.format(filename))
    print('**********************')
    subprocess.run(['python3', 'ASTEREX.py', '--input', inputFile, '--vstm', 'initialize', \
        '--focus', focus, '--simulate', '100', '--output', outputFile, '--cellsize', cs, \
        '--cellscalar', '1.0', '--celloffset', co, '--distance', dist, '--compression', com])
    subprocess.run(['mv', './out/' + outputFile, outputDir])
    print('**********************')
    print('{} complete!'.format(filename))
    print('**********************')

end_time = datetime.now()
end_string = end_time.strftime("%d/%m/%Y %H:%M:%S")
print('****************')
print(end_string)
print('Script complete!')
print('****************')
