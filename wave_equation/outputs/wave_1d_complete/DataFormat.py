# This is a csv cutting program
# Read the whole csv file into memory
# Cut the csv file into pieces depends on the number of one row (time steps)

import csv
import numpy as np



# Create the data folder to store output csv files
data_folder = "data"

csv_file_name = "Output.csv"
csv_file = open(csv_file_name, "r")
csv_reader = csv.reader(csv_file)
csv_data = []
for row in csv_reader:
    csv_data.append(row)
csv_file.close()



# There are 6 columns in the csv data
# Transfer the data into a numpy array
csv_data = np.array(csv_data)




# The first row is the header which needs to be copied to each piece of the csv file
# Read the header and store it in a list
header = csv_data[0,1:]

# Cut the csv_data into pieces according to the number of time steps which is in the first column
# The first column is the number of time steps
# Store the pieces into a individual csv files in the data folder
# The name of the csv files are "OutputOne_a.csv" where a is the timestep number
# The first row of each csv file is the header
# Remove the first column of each csv file since it is the number of time steps
t = csv_data[1, 6]
i = int(0)
datapiece = np.empty((0, csv_data.shape[1]-1), dtype=object)
datapiece = np.append(datapiece, [header], axis=0)


for row in range(1,csv_data.shape[0]):
    if(csv_data[row, 6] == t):
        datapiece = np.append(datapiece, [csv_data[row, 1:]], axis=0)
    else:
        # set i to a string with 2 decimal places
        index = str(i)
        csv_file_name = data_folder + "/OutputOne_" + index + ".csv"
        csv_file = open(csv_file_name, "w")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(datapiece)
        csv_file.close()
        t = csv_data[row, 6]
        datapiece = np.empty((0, csv_data.shape[1]-1), dtype=object)
        datapiece = np.append(datapiece, [header], axis=0)
        datapiece = np.append(datapiece, [csv_data[row, 1:]], axis=0)
        i=i+1
        
index = str(i)
csv_file_name = data_folder + "/OutputOne_" + index + ".csv"
csv_file = open(csv_file_name, "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerows(datapiece)
csv_file.close()
        



