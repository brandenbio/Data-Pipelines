#!/usr/bin/python
# -*- coding: utf-8 -*-

# Output JSON files (labels) and      #
# configuration file for modeling use #
# Script by: Branden Bio              #
# Version 1.1                         #
# Date created: 07/03/2024            #
# Date updated: 07/10/2024            #

import pandas as pd
import numpy as np
import os
import json

project = "RT1"

# Setup paths
homeDir = '/Users/bbio/Repository/Projects/Perception/Relational Tracking/modeling/'
expDir = homeDir + project + '/'
labDir = expDir + 'labels/'

# Read in aggregated human data
humanData = pd.read_csv(os.path.join(expDir, f'{project}-humanData.csv'))

# Filter data for relevant info
data = humanData[['ParticipantID','ProblemNumber', 'Direction', 'X_Coord_Obj1', 'Y_Coord_Obj1', 'X_Coord_Obj2', 'Y_Coord_Obj2']]

jsonString = '''{"image_size": {"width": 800, "height": 800}, "objects": 
[{"label": "A", "confidence": 0.912629, "dimensions": {"x": *X-COORD-A*, "y": *Y-COORD-A*, "width": 70, "height": 70}}, 
{"label": "B", "confidence": 0.919737, "dimensions": {"x": *X-COORD-B*, "y": *Y-COORD-B*, "width": 70, "height": 70}}]}'''

outputCSV = expDir + 'uniqueProblemInstances.csv'

pidArray = []

with open(outputCSV, 'a') as file:
    for row in range(len(data)):
        pid = data.iloc[row]['ParticipantID']
        pidArray += [pid]
        problemNumber = str(data.iloc[row]['ProblemNumber'])
        instance = str(len(np.unique(pidArray)))
        # Create JSON and replace template with contents from coord df
        tempJSON = jsonString
        currentJSON = tempJSON.replace(
        "*X-COORD-A*", str(data.iloc[row]['X_Coord_Obj1'])).replace(
        "*Y-COORD-A*", str(data.iloc[row]['Y_Coord_Obj1'])).replace(
        "*X-COORD-B*", str(data.iloc[row]['X_Coord_Obj2'])).replace(
        "*Y-COORD-B*", str(data.iloc[row]['Y_Coord_Obj2']))

        # Name output files
        outputJSON = labDir + f'Problem{problemNumber}_Instance{instance}.json'

        # Convert JSON string to a Python dictionary
        pyJSON = json.loads(currentJSON)

        # Write the dictionary to a JSON file
        with open(outputJSON, 'w') as json_file:
            json.dump(pyJSON, json_file)

        # Setup configuration file as input for loopAsterex.py
        # Create prompt for specific trial
        direction = data.iloc[row]['Direction']
        if direction == "left" or direction == "right":
            focus = r"what is to the " + direction + " of the B"
        elif direction == "above" or direction == "below":
            focus = r"what is " + direction + " the B"

        # Populate array with problem number, instance number, focus
        trial = [problemNumber,instance,focus]
        trial_str = ','.join(trial)

        # Append that array to uniqueProblemInstances.csv
        file.write(trial_str + '\n')
