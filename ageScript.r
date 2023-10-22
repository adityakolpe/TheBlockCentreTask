myArgs <- commandArgs(trailingOnly = TRUE)
# Do some conversion/calculation here
library("lubridate") 
dob <- ymd(myArgs)
current_date <- Sys.Date()
age <- interval(dob, current_date) %/% years(1)
# Write the result to output stream
cat(age)