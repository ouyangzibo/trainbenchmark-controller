#Train Benchmark Controller

### Overview
Trainbenchmark-controller is responsible for building the actual projects, generating the models and also running the benchmark tests. The scripts are written in Python 3 programming language. Every process is executed on the base of the `config.json` file. To alter the default configuration of Train Benchmark, just modify `config.json` file. You can find more information about the configuration parameters [below](#Configuration).

### Requirements
Apart from the fundamental requirements that is also necessary to possess a Python 3 interpreter. All modules were written and tested on Linux operating system, so there is no guarantee yet that the scripts can be perfectly used on Windows.
For executing scripts, there are no restrictions for the actual working directories, which means you can run the modules from any path.
If any trainbenchmark projects have dependencies to each other, then they have to store a `dependencies.json` file under their `./dependencies/` subfolder.
A typical `dependencies.json` file looks like this:
  ```
  {
    "dependencies": {
      "url": "https://github.com/FTSRG/trainbenchmark-rdf.git",
      "branch": "master",
      "depth": "50",
      "folder": "trainbenchmark-rdf"
    }
  }
  ```
The example above shows the required dependency of trainbenchmark-sesame. Url means the remote repository's availability, branch and depth are git based parameters and the folder is the directory that will be created on our local space.

### Installation guide
At first, clone the trainbenchmark-controller repository to your local folder. It is advisable to clone to the same directory where you store the other trainbenchmark projects, since the controller searches them under the same parent folder. In the other case, if the controller did not find any of the certain projects, it would download them automatically. To clone the trainbenchmark-controller, execute the following command:
* `git clone https://github.com/FTSRG/trainbenchmark-controller.git`

Then it is necessary to install the required external modules for Python. Thus, run `init.py` script from the `trainbenchmark-controller/src/controller/` directory, like this:
 * `./init.py`
That will install every third-party libraries from `trainbenchmark-controller/external` folder. Be careful to modify nothing from this directory.
Note that root password is required for the successful deployment. Furthermore, do not execute `__init__.py` by accident instead.
After this step, you are able to [run the main scripts](#Usage).

### <a name="Configuration"></a>Configuration
Every configuration parameter which matters is stored in the `config.json` file. A typical structure of it can be seen here:
 
```
{
  "scenarios": [
    "User",
    "XForm"
  ],
  "MAVEN_OPTS": {
    "Xmx": "512m",
    "XX:MaxPermSize": "256m"
  },
  "JAVA_OPTS": {
    "xmx": "1g",
    "maxPermSize": "256m"
  },
  "minSize": 1,
  "maxSize": 4,
  "workspacePath": ".",
  "queries": [
    "PosLength",
    "RouteSensor",
    "SignalNeighbor",
    "SwitchSensor"
  ],
  "tools": [
    "sesame"
  ],
  "format": "rdf"
}
```
The parameters above can contain the following values:
 * scenarios: `Batch`, `User`, `XForm` or these combinations
 * the Xmx and maxPermSize attributes must match to this regular expression: `^[0-9]+[m,g]`. For example: 
  ```
  Correct values:
  128m
  1g
  1024m
  
  Invalid values:
  128M
  1G
  1024
  ```

 * minSize: cannot be less than 1
 * maxSize: must be higher than minSize  
   Additional condition with min- and maxSize: cannot be the range between them arbitrary: at least one power of 2 number must fit to the defined set. For example:

  ```
  Correct values:
  min:1 max:4
  min:2 max:2
  
  Invalid values:
  min:0 max:4
  min:9 max:15
  ```
 * workspacePath: shall be equal to a path of an existing directory. The "." value is also acceptable, which refers to the same level of hierarchy of directories where the trainbenchmark-controller is located. For example if this parameter was equal with `./example`, then an `example` folder should be exist next to the trainbenchmark-controller directory.
 * queries: must be equal at least one of these values:
  * `PosLength`
  * `RouteSensor`
  * `SignalNeighbor`
  * `SwitchSensor`
  * `SegmentLength`
  * `SwitchNodes`
  * `RouteEntry`
  * `RouteRouteDefinition`
  * `TrackElementSensor`  
   Note that every possible combination of the queries is permitted.
 * tools: the possible values of tools are depend on the given format. For instance:
  * format: `rdf`
    * tools:
      * `sesame`
      * `fourstore`  
       And these possible combinations.
  * format: `graph`
    * tools:
      * `neo4j`
  * format: `emf`
    * tools:
      * `drools`
      * `java`
      * `emfincquery`
      * `eclipseocl`  
       And these possible combinations.
  * format: `sql`
    * tools:
      * `mysql`  

   Note that you cannot use more than one format at the same time, that is only possible with tools. But you cannot mix tools which connect to different formats. For example:

   ```
   //correct configuration
   "tools": [
     "sesame",
     "fourstore"
   ],
   "format": "rdf"  

   //invalid configuration
   "tools": [
     "sesame",
     "neo4j"
   ],
   "format": "rdf", "graph"  
   ```

### Modules
The most important python modules of trainbenchmark-controller are the followings:
 * **build.py**: The module is responsible for resolving the dependencies between repositories, furthermore build the projects with maven. With the optional arguments, there is  an opportunity to generate the models and run the benchmark tests too.
  Arguments:
   * `-g`, `--generate`: generate the models too
   * `-b`, `--benchmark`: run benchmark test after build
   * `-t`, `--tools`: build the tools
   * `-f`, `--format`: build the format
   * `-c`, `--core`: build the core  
   Actually by executing `./build.py -tfc` script you got the same effect like running `./build.py`, since it builds everything basically.
 * **generate.py**: Generates the certain models, based on the `config.json` file.
 * **benchmark.py**: This module is responsible for running the benchmark tests.  

Important fact that all modules work with the certain tools and formats, which are given in `config.json`.

### <a name="Usage"></a>Usage
After the step of cloning the repository and install the required modules furthermore adjust the configuration file, you are able to build the projects by running the following script from the `trainbenchmark-controller/src/controller` directory, like this:
`./build.py`

This will clone the actual trainbenchmark repositories (if necessary) and run the maven build. But be careful, because some of the tools without the generated models cannot be built, as the JUNIT tests require for them (for example sesame). To avoid this conflict, it is worthwhile to execute the script at the first time like this:
 
```
./build.py --generate
//or the shorter version
./build.py -g
 ```
You are able to build only some parts of the Train Benchmark:

```
./build --tools

//OR
./build.py --tools --format
```
For more information read the module's help page: `./build.py -h`
There is another opportunity to generate models distinctly via the `generate.py` module. Execute it from the `trainbenchmark-controller/src/controller` folder:
```
./generate.py
```
The generated models will be created under the `trainbenchmark-models` directory next to the controller's folder.

Eventually you can run the benchmark tests:
```
./benchmark.py
```
 
In order to obtain exactly the same procedure by one script, run the `build.py` module with optional parameters:
```
./build.py --generate --benchmark
//OR
./build.py -g -b
//OR
./build.py -gb
```

### Additional Information

#### Other parts of the controller

 * `config_schema.json`: describes the `config.json` file's format. The latter must follow the defined rules by the schema.
 * `tools_source.json`: contains the remote repositories' url, folders, branches and depths of tools
 * `init.py`: install the external python modules
 * `handler.py`: a helper module which contains the most frequently used functions
 * `neo4j_installer.py`: install neo4j's dependencies 
 * `targets_source.py`:contains the paths of the certain tools' target .jar files and the used models by them.

If any possible changes appeared such as alteration of paths of the projects' repositories or the generated .jar files, then modify `tools_source.json`, `targets_source.py` or even the certain `dependencies.json` files if necessary.

#### Possible termination outputs
The python modules implement different exit status codes, if some errors occurred. Possible output numbers and their meanings are the followings:
* 1: `config.json` do not follows the defined rules, which described by the json schema
* 2: problem appeared with the opening of `config.json` file or during the decoding process from JSON to a python object
* 3: problem appeared with the opening of `tools_source.jso`n file or during the decoding process from JSON to a python object
* 4: too short the range between minSize and maxSize in the `config.json` file
