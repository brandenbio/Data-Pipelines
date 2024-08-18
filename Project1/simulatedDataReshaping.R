# --------------------------------------------------------------------------------------------------
# Pragmatic Spatial Reasoning Simulation Data Reformatting
# --------------------------------------------------------------------------------------------------
# Subject pool: Simulated
# Date(s):      March 2023
# Update:       February 2024
# Code:         Branden Bio
# --------------------------------------------------------------------------------------------------
# Contents:
#  X. Reshape simulated data
# --------------------------------------------------------------------------------------------------

library(tidyverse)

##############
# Setup script
project <- "PSR2"
simsDir <- "sims_lesion_co_com"
baseDir <- "/Users/bbio/Repository/Projects/Spatial Reasoning/Pragmatic Spatial Reasoning"
humDir <- paste(baseDir, "/Experiment ", project, "/Data/Analysis", sep="")
inputDir <- paste(baseDir, "/scripts/", project, "/simulations/", simsDir, sep="")
outputDir <- paste(baseDir, "/Experiment ", project, "/Data/Analysis/simulations/", simsDir, sep="")
##############

# Read in aggregated human data
data <- read.csv(paste(humDir, "/", project, "-Aggregate.csv", sep=""), header=T)
placementDF <- data.frame()
for (n in 1:8) {
  temp <-data[data$ProblemNumber==n,c(4,8,9,14,15)][1,]
  placementDF <- bind_rows(placementDF, temp)
}

# Read in individual problem simulations
paramOff <- 1
cellsizes <- c(seq(50, 400, by = 50))
celloffset <- (seq(0, 100, by = 25))
distances <- c(seq(2, 8, by = 1))
compression <- c(seq(0.0, 1.0, by = 0.1))
if (paramOff == 1) {
  celloffset <- 0
  compression <- 0
}
for (cs in cellsizes) {
  for (co in celloffset) {
    for (d in distances) {
      for (com in compression) {
        current_file_pattern <- paste("cs", as.character(cs), "_co", as.character(co), "_d", 
                                      as.character(d), "_com", as.character(com), ".csv", sep="")
        #current_file_pattern <- paste("cs", as.character(cs), "_d", as.character(d), "_co", as.character(co), ".csv", sep="")
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
                                      "AnswerContent" = "Response")
        
        simData$ProblemNumber <- str_extract(simData$ProblemNumber, "(\\d)+")
        simData$ProblemNumber <- as.numeric(simData$ProblemNumber)
        
        simData$Direction <- str_extract(simData$Direction, "left|right|above|below")
        simData$Direction <- str_to_sentence(simData$Direction)
        
        simData$AnswerContent <- tolower(simData$AnswerContent)
        
        # Insert position information
        simData <- merge(simData, placementDF, by = "ProblemNumber", all.x = TRUE)
        simData <- simData %>% 
          select(ParticipantID, ProblemNumber, Direction, Position_1_1, Position_1_2, Position_4_1, Position_4_2, AnswerContent) %>% 
          arrange(ParticipantID)
        
        # Insert abstract information
        simData$AnswerAbstract <- simData$AnswerContent
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==1, 
                                         str_replace_all(simData$AnswerAbstract, c("cup" = "A", "sandwich" = "B", "carrot" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==2, 
                                         str_replace_all(simData$AnswerAbstract, c("apple" = "A", "hotdog" = "B", "cup" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==3, 
                                         str_replace_all(simData$AnswerAbstract, c("cake" = "A", "cup" = "B", "pizza" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==4, 
                                         str_replace_all(simData$AnswerAbstract, c("bottle" = "A", "cup" = "B", "carrot" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==5, 
                                         str_replace_all(simData$AnswerAbstract, c("banana" = "A", "carrot" = "B", "pizza" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==6, 
                                         str_replace_all(simData$AnswerAbstract, c("carrot" = "A", "hotdog" = "B", "broccoli" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==7, 
                                         str_replace_all(simData$AnswerAbstract, c("cup" = "A", "hotdog" = "B", "carrot" = "C")), 
                                         simData$AnswerAbstract)
        simData$AnswerAbstract <- ifelse(simData$ProblemNumber==8, 
                                         str_replace_all(simData$AnswerAbstract, c("cake" = "A", "apple" = "B", "carrot" = "C")), 
                                         simData$AnswerAbstract)
        
        
        simData$AnswerPosition <- simData$AnswerAbstract
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==1, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_1_1", "B#1" = "Position_1_2", 
                                                                                   "B#2" = "Position_4_2","C" = "Position_4_1")), 
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==2, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_1_2", "B#1" = "Position_1_1", 
                                                                                   "B#2" = "Position_4_2","C" = "Position_4_1")), 
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==3, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_4_2", "B#1" = "Position_1_1", 
                                                                                   "B#2" = "Position_4_1","C" = "Position_1_2")), 
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==4, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_4_1", "B#1" = "Position_4_2", 
                                                                                   "B#2" = "Position_1_1","C" = "Position_1_2")),  
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==5, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_1_2", "B#1" = "Position_4_1", 
                                                                                   "B#2" = "Position_4_2","C" = "Position_1_1")),  
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==6, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_1_1", "B#1" = "Position_1_2", 
                                                                                   "B#2" = "Position_4_1","C" = "Position_4_2")),  
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==7, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_4_1", "B#1" = "Position_1_1", 
                                                                                   "B#2" = "Position_1_2","C" = "Position_4_2")), 
                                         simData$AnswerPosition)
        simData$AnswerPosition <- ifelse(simData$ProblemNumber==8, 
                                         str_replace_all(simData$AnswerPosition, c("A" = "Position_4_1", "B#1" = "Position_1_1", 
                                                                                   "B#2" = "Position_4_2","C" = "Position_1_2")), 
                                         simData$AnswerPosition)
        
        simData$AnswerAbstract <- gsub("[#0-9]", "", simData$AnswerAbstract)
        
        simData$Condition <- ifelse(simData$ProblemNumber %% 2 != 0, "Ambiguous", "Unambiguous")
        
        simData <- simData %>% select(ParticipantID, ProblemNumber, Condition, Direction, 
                                      AnswerContent, AnswerPosition, AnswerAbstract) %>% arrange(ParticipantID)
        
        setwd(outputDir)
        write.csv(simData, paste(outputDir, "/", project, "-Simulations_", current_file_pattern, sep=""), row.names=FALSE)
      }
    }
  }
}
