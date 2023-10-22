myArgs <- commandArgs(trailingOnly = TRUE)
# Do some conversion/calculation here
library("lubridate") 
dob <- ymd(myArgs)
day_of_week <- weekdays(dob)
cat(day_of_week)