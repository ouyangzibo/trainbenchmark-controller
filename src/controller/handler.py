"""
Created on Sep 28, 2014

@author: Zsolt Kovari

A helper module, which collects the most frequently used functions 
by the other modules.

Functions:
    set_working_directory: change the working directory
    get_power_of_two: creates a list of squared numbers
    json_validate: json schema validation
    json_decode: load json file to a python json object
"""
import json
import os

from jsonschema import validate, Draft4Validator
from jsonschema.exceptions import ValidationError, SchemaError, best_match


def set_working_directory(path = None):
    """
    Set the working directory to this script's folder or to the path
    optional parameter, if that is given.
    """
    if (path == None):
        full_path = os.path.realpath(__file__)
        path = os.path.split(full_path)
        os.chdir(path[0])
    else:
        if (os.path.exists(path) == True):
            os.chdir(path)
        else:
            print("The given parameter is not a valid directory:"+ path)


def get_power_of_two(minsize, maxsize):
    """
    Return power of two numbers between minsize and maxsize 
    in a list as strings.
    """
    all_size = []
    index = 1
    while (index <= maxsize):
        if (index >= minsize):
            size_string = str(index)
            all_size.append(size_string)
        index *= 2
    return all_size


def json_validate(instance, schema):
    """
    Open two files, which are provided by the arguments as paths 
    and check whether they are both valid .json files.
    Furthermore compare the instance json file to the schema,
    if that is acceptable by the definitions of the latter.
    According to the validation, the return value is True(schema based)
    or False(invalid).
    
    Arguments:
    instance -- path of a .json file, that will be validated by the schema
    schema -- path of the schema itself
    """
    # check the two received arguments' path
    if (os.path.exists(instance) == False):
        print(instance + " file does not exist!")
        return False
    if (os.path.exists(schema) == False):
        print(schema + " file does not exist!")
        return False
    
    try:
        with open(schema,"rt") as schema_file,\
                open(instance,"rt") as instance_file:
            instance_json = json.load(instance_file)
            schema_json = json.load(schema_file)
            validate(instance_json,schema_json)
            if (instance_json["minSize"] > instance_json["maxSize"]):
                print("Maxsize is lower than minsize. Change the "\
                      "config.json file")
                return False
            set_working_directory();
            set_working_directory("../../../")
            if (os.path.exists(instance_json["workspacePath"]) == False):
                print(instance_json["workspacePath"]\
                      + "is not a valid directory. Modify " + instance\
                      + " workspacePath parameter.")
                return False
            set_working_directory();
    except ValueError as value_error:
        print("Json file is not valid \n", value_error)
    except IOError:
        print("Cannot read the file")
    except ValidationError as validation_error:
        print("A problem has occurred during the validation, here:")
        for element in validation_error.absolute_schema_path:
            print(element, " -> ",end='')
        # determine the error's first place
        print(best_match(Draft4Validator(schema_json)\
                         .iter_errors(instance_json)).message)
    except SchemaError:
        print("The provided schema is malformed.")
    else:
        return True
    return False


def json_decode(json_path):
    """
    Open a .json file and return as a python json object.
    The json_path parameter is the path of the file.
    Return None if a problem has occurred.
    """
    try:
        with open(json_path) as file:
            json_object = json.load(file)
    except IOError:
        print("The file does not exist or cannot read.")
    except ValueError as value_error:
        print(json_path + " file is not valid \n", value_error)
    else:
        return json_object
    return None


