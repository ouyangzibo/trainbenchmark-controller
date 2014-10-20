#!/usr/bin/env python3
"""
Created on Sep 28, 2014

@author: Zsolt Kovari

The module is responsible for resolving the dependencies between repositories,
furthermore build the projects with maven. With the optional arguments,
there is an opportunity to generate the models and run the benchmark tests.

Arguments:
    -g, --generate: generates models
    -b, --benchmark: run benchmark
    -c, --core: just build the core
    -f, --format: just build the format
    -t, --tools: just build the tools
    -
"""
import os
import subprocess
import sys
import argparse
import atexit

import handler
import benchmark
import generate
import neo4j_installer


def git_clone(url, branch = "master", depth = "50"):
    """
    Clone a remote repository by git.
    The necessary URL is provided by the url argument.
    """
    subprocess.call(["git", "clone", url, "--branch", branch, "--depth", depth])


def resolve_dependencies(repositories, folders, branches, depths):
    """
    Resolve the dependencies between repositories after the dependencies.json
    files. Every new url will be stored in repositories parameter and every
    new directory in folders too, just like branches and depths.
    """
    for repo,folder,branch,depth in \
            zip(repositories, folders, branches, depths):
        if (os.path.exists(os.getcwd() + "/" + folder) == False):
            git_clone(repo, branch, depth)     
        #delete later
        waiting = input("Waiting for .JSON file to be copied to the right place.")
        dependencies_path = "./" + folder + "/dependencies/dependencies.json"
        if(os.path.exists(dependencies_path) == True):
            dependencies_json = handler.json_decode(dependencies_path)
            if (dependencies_json["dependencies"]["url"] not in repositories):
                repositories.append(dependencies_json["dependencies"]["url"])
                folders.append(dependencies_json["dependencies"]["folder"])
                branches.append(dependencies_json["dependencies"]["branch"])
                depths.append(dependencies_json["dependencies"]["depth"])


def maven_build(param):
    """Build the projects.
    """
    subprocess.call(["mvn", "clean", "install", "-f",\
                     "./trainbenchmark-core/pom.xml", "-P",param,])

def test():
    print ("Running!")


atexit.register(test)
parser = argparse.ArgumentParser();
parser.add_argument("-g","--generate",
                    help="generate models too",
                    action="store_true")
parser.add_argument("-b","--benchmark",
                    help="run the benchmark tests too",
                    action="store_true")
parser.add_argument("-c","--core",
                    help="build the core",
                    action="store_true")
parser.add_argument("-f","--format",
                    help="build the format",
                    action="store_true")
parser.add_argument("-t","--tools",
                    help="build the tools",
                    action="store_true")

args = parser.parse_args()
# set working directory to this file's path
handler.set_working_directory()
config_path = "../../config/config.json"
schema_path = "../../config/config_schema.json"
tools_path = "../../config/tools_source.json"
build_all = True
if (args.core == True or args.format == True or args.tools == True):
    build_all = False
# remote repositories' url will be stored in repositories
repositories = list()
folders = list()
branches = list()
depths = list()
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
queries = config_json["queries"]
maven_opt = config_json["MAVEN_OPTS"]
java_xmx = config_json["JAVA_OPTS"]["xmx"]
java_maxpermsize = config_json["JAVA_OPTS"]["maxPermSize"]
subprocess.call(["../../shell-scripts/export_maven_opts.sh", maven_opt["Xmx"],\
                 maven_opt["XX:MaxPermSize"]])

tools_json = handler.json_decode(tools_path)
if(tools_json == None):
    sys.exit(3)
for tool in tools:
    repositories.append(tools_json[tool]["url"])
    folders.append(tools_json[tool]["folder"])
    branches.append(tools_json[tool]["branch"])
    depths.append(tools_json[tool]["depth"])
    

if (args.benchmark == True or args.generate == True):
    # power of the 2 numbers will be stored in all_size[] list as strings
    all_size = handler.get_power_of_two(minsize, maxsize)
    if (len(all_size) == 0):
        print("Problem with min and maxsize. Too short the range between them.")
        sys.exit(4)

#jump back three folders
handler.set_working_directory("../../..")
# change directory to the configuration workspacePath parameter
handler.set_working_directory(workspacepath)
resolve_dependencies(repositories, folders, branches, depths)

if (build_all == True or args.core == True):
    maven_build("core")

# neo4j has other external dependencies
if ("neo4j" in tools):
    neo4j_installer.install(os.getcwd())

if (build_all == True or args.format == True):
    maven_build(format)

if (args.generate == True):
    for scenario in scenarios:
        generate.generate_models(format, scenario, all_size,\
                                 java_xmx, java_maxpermsize)

if (build_all == True or args.tools == True):
    for tool in tools:
        maven_build(tool)
   
if (args.benchmark == True):
    for tool in tools:
        for scenario in scenarios:
            for size_str in all_size:
                benchmark.run_test(format, tool, scenario, queries, size_str,\
                                   java_xmx, java_maxpermsize)