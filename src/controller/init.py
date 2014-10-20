#!/usr/bin/env python3
"""
Created on Oct 4, 2014

@author: Zsolt Kovari

Install the necessary external modules.
"""
import os
import subprocess


full_path = os.path.realpath(__file__)
path = os.path.split(full_path)
os.chdir(path[0])
os.chdir("../../external/")
# contains all subfolders under /external 
folders = os.listdir()
for directory in folders:
    os.chdir(directory)
    subprocess.call(["sudo", "python3", "setup.py", "install"])
    

