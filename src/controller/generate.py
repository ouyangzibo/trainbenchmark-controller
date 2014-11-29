#!/usr/bin/env python3
"""
Created on Oct 5, 2014

@author: Zsolt Kovari

This module generates the certain models.
"""
import subprocess
import os
import sys

import targets
import handler
import loader

def generate_models(configuration):
    """
    Generates the models after the configuration parameter.
    
    Parameters:
    @param configuration: a Configuration object
    """
    # change back working directory later, so store it now
    current_directory = os.getcwd() 
    # change working directory to this module's location
    handler.set_working_directory(configuration.path)
    target = targets.get_generator_jar(configuration.format)
    if (target is None):
        # log here
        pass
    models_path = targets.get_common_model_path()
    if(os.path.exists(models_path) == False):
        os.makedirs(models_path)
    for scenario in configuration.scenarios:
        for size in configuration.sizes:
            java_xmx = configuration.java_xmx
            java_maxpermsize = configuration.java_maxpermsize
            subprocess.call(["java", "-Xmx" + java_xmx,"-XX:MaxPermSize=" +\
                             java_maxpermsize, "-jar", target, "-scenario",\
                             scenario, "-size", size, "-workspacePath", \
                             configuration.path])
    handler.set_working_directory(current_directory)


# if this script is imported by an other module, 
# then the following lines will not be evaluated
if (__name__ == "__main__"):
    configurations = loader.get_configs_from_json()
    if (configurations is None):
        sys.exit(1)
    for config in configurations:
        generate_models(config)

        