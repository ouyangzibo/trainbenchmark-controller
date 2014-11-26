#!/usr/bin/env python3
"""
Created on Sep 30, 2014

@author: Zsolt Kovari

This module is responsible for running the benchmark test.
"""
import subprocess
import sys
import os

import targets_source
import handler
import loader


def run_test(configuration):
    """Run the benchmark test after the configuration parameter.
    
    Parameters:
    @param configuration: a Configuration object
    """
    handler.set_working_directory()
    handler.set_working_directory("../../../")
    if (os.path.exists("./trainbenchmark-results") == False):
        os.mkdir("trainbenchmark-results")
    handler.set_working_directory(configuration.path)
    for scenario in configuration.scenarios:
        for size in configuration.sizes:
            target = targets_source.get_benchmark_jar(configuration.tool)
            format = configuration.format
            benchmark_artifact = targets_source.get_model_path(format,\
                                                               scenario,\
                                                               size)
            for query in configuration.queries:
                print(query)
                xmx = configuration.java_xmx
                maxpermsize = configuration.java_maxpermsize
                subprocess.call(["java", "-Xmx" + xmx, "-XX:MaxPermSize="\
                                 + maxpermsize, "-jar", target,\
                                 "-scenario", scenario,\
                                 "-benchmarkArtifact", benchmark_artifact,\
                                 "-workspacePath", configuration.path,\
                                 "-query", query, "-nMax", "1"])


# if this script is imported by an other module, 
# then the following lines will not be evaluated
if (__name__ == "__main__"):
    configurations = loader.get_configs_from_json()
    if (configurations is None):
        sys.exit(1)
    for config in configurations:
        run_test(config)

