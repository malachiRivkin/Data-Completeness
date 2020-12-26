# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:59:04 2020

@author: Malachi
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import os
from io import StringIO

#show heatmaps?
show = False


# specify the location of flight data
path = r'C:\Users\Colleen\ChilePythonEnvironment\testData'
os.chdir(path)

#file = 'testFile_0'
visuals = r'C:\Users\Colleen\ChilePythonEnvironment\visuals'     #location where selections from siftThroughUV are saved. This is also the location where do analysis looks for micro hodos to analysis



col_names = ['Time', 'P', 'T', 'Hu', 'Ws', 'Wd', 'Long.', 'Lat.', 'Alt', 'Geopot', 'MRI', 'RI', 'Dewp.', 'VirtTemp', 'Rs', 'Elevation', 'Az', 'Range', 'D']     #header titles

for file in os.listdir(path):
    r"""
    # Open and investigate the file
    contents = ""
    isProfile = False  # Check to see if this is a GRAWMET profile
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

    # perform calculations on data to prepare for hodograph
    # interpret flight data into usable array/dictionary/list (not sure which is preferable yet...)
    data = pd.read_csv(StringIO(contents), delim_whitespace=True)
    """
    #added for testing
    data = pd.read_csv(os.path.join(path, file), delim_whitespace=True)
    data = data.where(data > 50, np.nan)
    #end added for testing
    data = data.apply(pd.to_numeric, errors='coerce')

    data = data.where(data < 999999, np.nan)

    #print("Maximum Altitude: {}".format(max(data['Alt'])))

    #data = data[0 : np.where(data['Alt']== data['Alt'].max())[0][0]+1] 


    col_names = ['Time', 'P', 'T', 'Hu', 'Ws', 'Wd', 'Long.', 'Lat.', 'Alt', 'Geopot', 'MRI', 'RI', 'Dewp.', 'VirtTemp', 'Rs', 'Elevation', 'Az', 'Range', 'D']     #header titles
    #randomSet = pd.DataFrame(np.random.randint(0,100, size=(7000,19)), columns=col_names)
    #randomSet = randomSet.where(randomSet > 50, np.nan)
    #randomSet = randomSet.fillna(0)
    #randomSet[randomSet!= 0] = 1

    #fill nans with zeros, all else with ones
    data = data.fillna(0)
    data[data!= 0] = 1


    #create heatmap showing nans

    fig = plt.figure(file, figsize=(8.5, 11))
    #ax = fig.add_axes([0.25, 0.25, .75, .75])
    ax = fig.add_subplot()
    im = ax.imshow(data, aspect='auto', cmap='binary', interpolation='nearest')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(col_names)))
    #ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(col_names, fontname="STIXGeneral")
    ax.tick_params(labelbottom=False,labeltop=True)
    ax.set_ylabel("Indices (set truncated to maximum altitude)", fontsize=14, fontname="STIXGeneral")
    ax.set_xlabel("*White cells indicate missing data", fontsize=14, fontname="STIXGeneral")


    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="left",
            rotation_mode="anchor")
    ax.xaxis.set_ticks_position('top')


    ax.set_title("Data Sparsity \n {}".format(file), fontsize=14, fontname="STIXGeneral")
    #fig.tight_layout()
    if show:
        plt.show()
   

    fig.savefig(os.path.join(visuals, file) + '_dataCompleteness.jpg')
    print("Saved Figure For: {}".format(file))
    plt.close()



    """
    outputFiles = False
    name = 'testFile'
    if outputFiles:
        for i in range(48):
            randomSet = pd.DataFrame(np.random.randint(0,100, size=(7000,19)), columns=col_names)
            randomSet.to_csv(name + '_' + str(i), header=None, index=None, sep=' ', mode='a')

    print("finished")       
            
    """