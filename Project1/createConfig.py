#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create configuration file for use in loopAsterex #
# Step 0                                           #
# Script by: Branden Bio						   #
# Version 1.0                                      #
# Date created: 07/14/2023                         #

import os
from os import path
from pathlib import Path
import subprocess
import sys
import pandas as pd

if len(sys.argv) <= 1:
    print('ERROR: Please provide experiment name as argument.')
    exit(1)

currExp = str(sys.argv[1])

# Setup directories
inputFile = os.path.expanduser('~/Repository/Projects/Spatial Reasoning/Pragmatic Spatial Reasoning/Experiment ' \
    + currExp + '/Code/Design.csv')
homeDir = str(Path(__file__).parent.resolve())
currExpDir = homeDir + '/' + currExp + '/'
outputFile = currExpDir + "tempConfig.txt"

# Read in problem configuration file and create config matrix
df = pd.read_csv(inputFile, usecols= ['ProblemNumber','Direction'])
df = df[df["ProblemNumber"] < 9]
df['Direction'] = df['Direction'].str.lower()
if os.path.exists(outputFile) == True:
    subprocess.run(['rm', outputFile])
with open(outputFile,"a") as config:
    for i in range(8):
        dat1 = str(df.loc[i]['ProblemNumber'])
        dat2 = df.loc[i]['Direction']
        data = dat1 + ',' + dat2 + ',' + '*TARGET{}*\n'.format(dat1)
        config.write(data)
    config.close()
if os.path.exists(outputFile) == True:
    print('***********************')
    print('tempConfig.txt created!')
    print('***********************')
else:
    print('*******************************')
    print('tempConfig.txt not completed :(')
    print('*******************************')
print('****************')
print('Script complete!')
print('****************')
