#!/usr/bin/env python3
"""
Created on Oct 5, 2014

@author: Zsolt Kovari

Install gradle then clone/build neo4j-shell-tools and geoff.
"""
import os
import subprocess
import shutil

import handler


def install(path):
    """
    Install gradle then clone/build neo4j-shell-tools and geoff 
    under that folder which is given via path parameter.
    """
    # Jump back three folders.
    #handler.set_working_directory("../../..")
    if (os.path.exists("./trainbenchmark-neo4j/scripts/init-neo4j") == True):
        print("The Neo4j install is already initialized. If you encounter"\
             + "any problems, please delete the init-done file"\
             + "in the trainbenchmark_neo4j/scripts directory.")
        return
    if (os.path.exists("./deps") == True):
        shutil.rmtree("./deps") # delete it and every subfolder
    os.mkdir("./deps")
    # install_neo4j shell script
    handler.set_working_directory()
    subprocess.call(["../../shell-scripts/install_neo4j.sh", path])
    # Set the working directory to this script's folder.
    handler.set_working_directory(path)
    # create an empty file
    new_file = open("./trainbenchmark-neo4j/scripts/init-neo4j", "w")
    new_file.close()

