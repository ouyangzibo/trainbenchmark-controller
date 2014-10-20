"""
Created on Oct 4, 2014

@author: Zsolt Kovari

The module contains the paths of the certain tools target 
.jar files and the used models by them.
"""


def get_generator_jar(format):
    """
    Return the generate's .jar file's path which belongs to the certain 
    format. The latter is provided by the format parameter.
    """
    return generatortargets.get(format)


def get_benchmark_jar(tool):
    """
    Return the benchmark's .jar file's path which belongs to the certain 
    tool. The latter is provided by the tool parameter.
    """
    return benchmarktargets.get(tool)

def get_model_path(format, scenario, size_str):
    """
    Return the used models' path by the certain format, scenario 
    and the actual size.
    """
    model = models[format]
    return model.format(SCENARIO=scenario.lower(),SIZE=size_str)


def get_common_model_path():
    """Return the folder's name where all of the models are stored.
    """
    return common_models_path
generatortargets = {
           'rdf':  "./trainbenchmark-rdf/"\
                 + "hu.bme.mit.trainbenchmark.generator.rdf/target/"\
                 + "hu.bme.mit.trainbenchmark.generator.rdf-1.0.0-SNAPSHOT.jar",
           'emf':  "./trainbenchmark-emf/"\
                 + "hu.bme.mit.trainbenchmark.generator.emf/target/"\
                 + "hu.bme.mit.trainbenchmark.generator.emf-1.0.0-SNAPSHOT.jar", 
           'graph':"./trainbenchmark-graph/"\
                 + "hu.bme.mit.trainbenchmark.generator.graph/target/"\
                 + "hu.bme.mit.trainbenchmark.generator."\
                 + "graph-1.0.0-SNAPSHOT.jar",
           'sql':  "./trainbenchmark-sql/"\
                 + "hu.bme.mit.trainbenchmark.generator.sql/target/"\
                 + "hu.bme.mit.trainbenchmark.generator.sql-1.0.0-SNAPSHOT.jar",   
           }
benchmarktargets = {
           'sesame': "./trainbenchmark-sesame/"\
                 + "hu.bme.mit.trainbenchmark.benchmark.sesame/target/"\
                 + "hu.bme.mit.trainbenchmark.benchmark"\
                 + ".sesame-1.0.0-SNAPSHOT.jar",
           'java': "./trainbenchmark-java/"\
                 + "hu.bme.mit.trainbenchmark.benchmark.java/"\
                 + "target/hu.bme.mit.trainbenchmark.benchmark."\
                 + "java-1.0.0-SNAPSHOT.jar",
           'neo4j':"./trainbenchmark-neo4j/"\
                 + "hu.bme.mit.trainbenchmark.benchmark.neo4j/target/"\
                 + "hu.bme.mit.trainbenchmark.benchmark."\
                 + "neo4j-1.0.0-SNAPSHOT.jar",
           'mysql':"./trainbenchmark-mysql/"\
                 + "hu.bme.mit.trainbenchmark.benchmark.mysql/target/"\
                 + "hu.bme.mit.trainbenchmark.benchmark."\
                 + "mysql-1.0.0-SNAPSHOT.jar"
           }
# {SCENARIO} and {SIZE} will be replaced
models = {
          'rdf': "./trainbenchmark-models/railway-{SCENARIO}-{SIZE}.ttl",
          'graph': "./trainbenchmark-models/railway-{SCENARIO}-{SIZE}.graphml",
          'emf': "./trainbenchmark-models/railway-{SCENARIO}-{SIZE}.concept",
          'sql': "./trainbenchmark-models/railway-{SCENARIO}-{SIZE}.sql"
          }
common_models_path = "./trainbenchmark-models"