# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:59:04 2020

@author: Malachi
"""


import pandas as pd
import numpy as np
import missingno as msno
import matplotlib as plt

import os
from io import StringIO

# specify the location of flight data
path = r'C:\Users\Malachi\OneDrive - University of Idaho\%SummerInternship2020\ChileData_12192020\Tolten'
os.chdir(path)

file = 'T1_1600_121320_ACE.txt'
visuals = r'C:\Users\Malachi\OneDrive - University of Idaho\%SummerInternship2020\CHileDataCompleteness\visuals'     #location where selections from siftThroughUV are saved. This is also the location where do analysis looks for micro hodos to analysis


col_names = ['Time', 'P', 'T', 'Hu', 'Ws', 'Wd', 'Long.', 'Lat.', 'Alt', 'Geopot', 'MRI', 'RI', 'Dewp.', 'VirtTemp', 'Rs', 'Elevation', 'Az', 'Range', 'D']     #header titles

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

data = data.apply(pd.to_numeric, errors='coerce')

data = data.where(data < 999999, np.nan)

print("Maximum Altitude: {}".format(max(data['Alt'])))

data = data[0 : np.where(data['Alt']== data['Alt'].max())[0][0]+1]
  
vis = msno.matrix(data, inline=False)
vis.title("Data Completeness")
#vis.title("Data Completeness")