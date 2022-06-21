#!/usr/bin/env Rscript
library(tidyverse)
library(dplyr)
library(fs)

args = commandArgs(trailingOnly=TRUE)
if (length(args)<3) {
  stop ("must provide UWB path, GPS path, output path ")
}

inFile = args[1]
GPSfile = arg[2]
outFile = args[3]

path = setwd(arg[1])
GPS_Path = GPSfile

files<-list.files(path)

filer <-files

# Cleaning up the UWB files
clean <- function(data) {
  new <- data %>%
    select(time_uwb, x, y)
  
  new$time_uwb <- new$time_uwb/10^4 # to align the UWB and GPS time
  
  return(new)
}

for (x in filer) {
  n <- write.csv(clean(read.csv(x)), paste0(x, ".csv"))
}

# necessary to change the timestamps to match
GPS <- read.csv(GPS_Path)
GPS$time_us <- GPS$time_us*100 # to align the UWB and GPS time

# Parsing the CSV filers
l <- fs::dir_ls(path)
namess <- filer
file_contents<- list()
for (i in seq_along(l)){
  file_contents[[i]]<- read_csv(file = l[[i]])
}

file_contents <- set_names(file_contents, namess)

namess%>%
  map(function(path){
    read_csv(path)
  })

# Time Align
time_filter <- function(time_in) {
  b <- filter(GPS, time_us >= time_in[1] 
              & time_us <= time_in[length(time_in)])%>%
    select(time_us, x, y)
  b <- data.frame(b)
  return(b)
}

out <- numeric()

for (i in file_contents) {
  a <- i$time_uwb
  b <- assign(paste("a", i$secs, sep = ""), time_filter(a))
  out <- c(out, b)
}

a= seq(1, lenght(out), 3) # We are only interested in time, X and Y

lis <- a

for (i in lis) {
  write.csv(data.frame(out[i], out[i + 1], out[i +2])
            , file = paste0(i, ".csv"), )
} 




