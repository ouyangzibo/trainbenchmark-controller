"""
Created on Nov 25, 2014

@author: Zsolt Kovari

The module is responsible for providing valid Configuration objects.
"""
import sys

import validation
import handler
from config import Configuration, Repository

def get_configs_from_json():
    """
    Loads a config.json file and run a validation process. If the configurations 
    seem valid, returns a list with Configuration objects.
    In the case of invalid config.json file, returns None.
    """
    # paths relatively to this script's location
    config_path = "../../config/config.json"
    schema_path = "../../config/config_schema.json"
    tools_path = "../../config/tools_source.json"
    
    config_json = handler.json_decode(config_path)
    if (config_json is None):
        return None
    schema_json = handler.json_decode(schema_path)
    if (schema_json is None):
        return None
    tools_json = handler.json_decode(tools_path)
    if (tools_json is None):
        return None
    valid = validation.is_valid_json(config_json, schema_json)
    if (valid == False):
        return None
    
    configurations = list()
    sizes = handler.get_power_of_two(config_json["minSize"],\
                                     config_json["maxSize"])
    if (len(sizes) == 0):
        print("Problem with min and maxsize. Too short the range between them.")
        sys.exit(4)
    scenarios = config_json["scenarios"]
    format = config_json["format"]
    queries = config_json["queries"]
    path = config_json["workspacePath"]
    maven_xmx = config_json["MAVEN_OPTS"]["Xmx"]
    maven_maxpermsize = config_json["MAVEN_OPTS"]["XX:MaxPermSize"]
    java_xmx = config_json["JAVA_OPTS"]["xmx"]
    java_maxpermsize = config_json["JAVA_OPTS"]["maxPermSize"]
    
    # create a Configuration object for every tool
    for tool in config_json["tools"]:
        configurations.append(Configuration(scenarios, format, tool, sizes,\
                                            queries, path, maven_xmx,\
                                            maven_maxpermsize, java_xmx,\
                                            java_maxpermsize))
    
    for config in configurations:
        # add a new Repository object to every Configuration
        config.set_repository(Repository(tools_json[config.tool]["url"],\
                                         tools_json[config.tool]["folder"],\
                                         tools_json[config.tool]["branch"],\
                                         tools_json[config.tool]["depth"]))
    return configurations
