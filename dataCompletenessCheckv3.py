# -*- coding: utf-8 -*-
"""
This script visualizes missing data in flight profiles. 
entries considered nans: 999999.0, all values greater than 999999.0

Author: Malalchi
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from io import StringIO

#show heatmaps?
show = False
#save heatmaps?
Save = True

# specify the location of flight data 
path = ''

# specify location to save visuals
visualSavePath = ''
#################################End User Input###########################################################

#header titles
col_names = ['Time', 'P', 'T', 'Hu', 'Ws', 'Wd', 'Long.', 'Lat.', 'Alt', 'Geopot', 'MRI', 'RI', 'Dewp.', 'VirtTemp', 'Rs', 'Elevation', 'Az', 'Range', 'D']     

for file in os.listdir(path):
    #indicate which file is in progress
    print("Analyzing: {}".format(file))
    
    # Open file
    contents = ""
    isProfile = False  # Is this a graw file?
    f = open(os.path.join(path, file), 'r')
    print("\nOpening file "+file+":")
    for line in f:  # Iterate through file, line by line
        if line.rstrip() == "Profile Data:":
            isProfile = True  # We found the start of the real data in GRAWMET profile format
            contents = f.read()  # Read in rest of file, discarding header
            print("File contains GRAWMET profile data")
            break
    f.close()  # Need to close opened file


    # Read in the data and perform cleaning

    # Need to remove space so Virt. Temp reads as one column, not two
    contents = contents.replace("Virt. Temp", "Virt.Temp")
    # Break file apart into separate lines
    contents = contents.split("\n")
    contents.pop(1)  # Remove units so that we can read table
    index = -1  # Used to look for footer
    for i in range(0, len(contents)):  # Iterate through lines
        if contents[i].strip() == "Tropopauses:":
            index = i  # Record start of footer
    if index >= 0:  # Remove footer, if found
        contents = contents[:index]
    contents = "\n".join(contents)  # Reassemble string

    # format flight data in dataframe
    data = pd.read_csv(StringIO(contents), delim_whitespace=True)
    
    #turn strings into numeric data types
    data = data.apply(pd.to_numeric, errors='coerce') 

    # replace all numbers greater than 999999 with nans
    data = data.where(data < 999999, np.nan)    

    
    #truncate data at greatest alt
    data = data[0 : np.where(data['Alt']== data['Alt'].max())[0][0]+1]  
    print("Maximum Altitude: {}".format(max(data['Alt'])))

    #fill nans with zeros, all else with ones
    data = data.fillna(0)
    data[data!= 0] = 1

    #create heatmap showing nans
    fig = plt.figure(file, figsize=(8.5, 11))
    ax = fig.add_subplot()
    im = ax.imshow(data, aspect='auto', cmap='binary', interpolation='nearest')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(col_names))) 
    # ... and label them with the respective entries
    ax.set_xticklabels(col_names, fontname="STIXGeneral")
    ax.tick_params(labelbottom=False,labeltop=True)
    ax.set_xlabel("*White cells indicate missing data", fontsize=14, fontname="STIXGeneral")

    # We'll label the ylabels too
    ax.set_ylabel("Indices (set truncated at maximum altitude)", fontsize=14, fontname="STIXGeneral")


    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="left",
            rotation_mode="anchor")
    ax.xaxis.set_ticks_position('top')

    # .. and add a title
    ax.set_title("Data Sparsity \n {}".format(file), fontsize=14, fontname="STIXGeneral")
    
    # If saving and/or showing sparsity visualizations
    if show:
        plt.show()
   
    if Save:
        name = file.strip('.txt')
        fig.savefig(os.path.join(visualSavePath, name) + '_dataSparsity.jpg')
        print("Saved Figure For: {}".format(file))
        plt.close()


