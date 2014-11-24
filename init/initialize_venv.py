#!/usr/bin/env python3
import venv
import os
import subprocess

full_path = os.path.realpath(__file__)
path = os.path.split(full_path)
os.chdir(path[0])
os.chdir("..")
env = venv.EnvBuilder(system_site_packages=False,clear=True,symlinks=True)
env.create("./tb-env/")
subprocess.call(["./init/install_pip_to_venv.sh"])
