# --------------------------------------------------------------------------------------------------
# Relational Tracking Simulation Data Reformatting
# --------------------------------------------------------------------------------------------------
# Subject pool: Simulated
# Date(s):      July 2024
# Code:         Branden Bio
# --------------------------------------------------------------------------------------------------
# Contents:
#  X. Reshape simulated data
# --------------------------------------------------------------------------------------------------

library(tidyverse)

##############
# Setup script
project <- "RT1"
simsDir <- "sims_cs70_co0_d4_com0"
baseDir <- "/Users/bbio/Repository/Projects/Perception/Relational Tracking"
humDir <- paste(baseDir, "/Experiment ", project, "/Data/Analysis", sep="")
inputDir <- paste(baseDir, "/modeling/", project, "/simulations/", simsDir, sep="")
outputDir <- paste(baseDir, "/Experiment ", project, "/Data/Analysis/simulations/", simsDir, sep="")
##############

dir.create(file.path(outputDir))

# Read in aggregated human data
data <- read.csv(paste(baseDir, "/modeling/", project, "/", project, "-humanData.csv", sep=""), header=T)
placementDF <- data %>% filter(ProblemType=="EXP") %>% select(ParticipantID,ProblemNumber,Direction,Answer,
                                                              translated_X_Coord_Obj1,translated_Y_Coord_Obj1,
                                                              translated_X_Coord_Obj2,translated_Y_Coord_Obj2,
                                                              Obj1_Leftof_Obj2,Obj1_Rightof_Obj2,Obj1_Above_Obj2,
                                                              Obj1_Below_Obj2,Acc)

# Read in individual problem simulations
cs  <- 70
co  <- 0
d   <- 4
com <- 0

current_file_pattern <- paste("cs", as.character(cs), "_co", as.character(co), 
                              "_d", as.character(d), "_com", as.character(com), ".csv", sep="")

files <- list.files(path=inputDir, pattern=current_file_pattern, full.names = TRUE)
aggregateData <- data.frame()
for (file in files) {
    temp <- read.csv(file)
    aggregateData <- bind_rows(aggregateData, temp)
}
simData <- aggregateData %>% select(SyntheticParticipantID, Arguments, InputFile, Response)

simData <- simData %>% rename("ParticipantID" = "SyntheticParticipantID",
                              "Direction" = "Arguments", 
                              "ProblemNumber" = "InputFile", 
                              "Answer" = "Response")

simData$ProblemNumber <- as.numeric(str_extract(simData$ProblemNumber, "\\d"))

simData$Direction <- str_extract(simData$Direction, "left|right|above|below")

simData[is.na(simData)] <- "No"
simData$Answer <- ifelse(simData$Answer=="A", "Yes", simData$Answer)

# Insert position information
comboData <- rbind(simData, placementDF)
comboData <- comboData %>%  arrange(ParticipantID, ProblemNumber)

#write.csv(comboData, paste(outputDir, "/", project, "-Simulations_", current_file_pattern, sep=""), row.names=FALSE)
