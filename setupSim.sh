#!/bin/bash

# Setup folders for simulations with Yolo #
# Step 0                                  #
# Script by: Branden Bio				  #
# Version 2.0                             #
# Date created: 05/11/2023                #

expName=$1

parentDir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

expDir="${parentDir}/${expName}"

mkdir "$expDir"

cd "$expDir"

mkdir 'images' 'labels' 'simulations'
