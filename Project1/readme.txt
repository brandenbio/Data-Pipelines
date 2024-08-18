readme file for spatial reasoning modeling pipeline

*Step 0: setupSim.sh
Creates contingent directories for later scripts. Requires experiment name as input.

*Step 0: createConfig.py
Creates the first half of the problem configuration file that will get used in loopAsterex.py

*Step 1: image2Json.py
Takes images as input and outputs json files which are labels of objects detected by yolo. Runs for each problem in experiment. 

*Step 2: loopAsterex.py
Takes json label files and runs ASTEREX on them simulating participants. Runs for each problem in experiment. Also requires configuration file which gives problem number, prompt direction, and target object in a txt separated by commas, each problem on a separate line.
Ex: 1,left,apple
    2,right,cake

Step 3: simulatedDataReshaping.R
Reshapes simulated data into format closer to human data output for analysis.

* Requires experiment name as input. Experiment names must match for each step.
