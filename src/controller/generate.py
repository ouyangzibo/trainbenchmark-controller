#!/usr/bin/env python3
"""
Created on Oct 5, 2014

@author: Zsolt Kovari

This module generates the certain models.
"""
import subprocess
import os
import sys

import targets_source
import handler

def generate_models(format, scenario, allsize, xmx, maxpermsize):
    """Generates the models.
    """
    target = targets_source.get_generator_jar(format)
    models_path = targets_source.get_common_model_path()
    if(os.path.exists(models_path) == False):
        os.makedirs(models_path)
    for size in allsize:
        subprocess.call(["java", "-Xmx" + xmx, "-XX:MaxPermSize="\
                         + maxpermsize, "-jar", target, "-scenario",\
                         scenario, "-size",\
                         size, "-workspacePath", os.getcwd()])


# if this script is imported by an other module, 
# then the following lines will not be evaluated
if (__name__ == "__main__"):
    # Set the working directory to this script's folder.
    handler.set_working_directory()
    config_path = "../../config/config.json"
    schema_path = "../../config/config_schema.json"
    validation = handler.json_validate(config_path, schema_path)
    if (validation == False):
        sys.exit(1)
    config_json = handler.json_decode(config_path)
    if (config_json == None):
        sys.exit(2)
    format = config_json["format"]
    tools = config_json["tools"]
    scenarios = config_json["scenarios"]
    minsize = config_json["minSize"]
    maxsize = config_json["maxSize"]
    workspacepath = config_json["workspacePath"]
    java_xmx = config_json["JAVA_OPTS"]["xmx"]
    java_maxpermsize = config_json["JAVA_OPTS"]["maxPermSize"]
    
    # power of 2 numbers will be stored in all_size[] list as strings between 
    # minsize and maxsize
    all_size = handler.get_power_of_two(minsize, maxsize)
    if (len(all_size) == 0):
        print("Problem with min and maxsize. Too short the range between them.")
        sys.exit(4)
    # Jump back three folders.
    handler.set_working_directory("../../../")
    handler.set_working_directory(workspacepath)
    for scenario in scenarios:     
        generate_models(format, scenario, all_size, java_xmx, java_maxpermsize)
        