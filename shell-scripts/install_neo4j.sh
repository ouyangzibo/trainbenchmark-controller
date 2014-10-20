#!/bin/bash

cd "$1"/deps

sudo add-apt-repository ppa:cwchien/gradle -y
sudo apt-get update
sudo apt-get install -y gradle
gradle -v

git clone --depth 1 https://github.com/nigelsmall/geoff.git
cd geoff
gradle install
cd ..	

git clone --depth 1 https://github.com/jexp/neo4j-shell-tools
cd neo4j-shell-tools
mvn clean install -DskipTests
