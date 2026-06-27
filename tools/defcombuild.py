#!/usr/bin/env python3

import os
import sys
import venv
import subprocess
from pathlib import Path
import shutil

#Get the file dir
BASE_DIR = str(Path(__file__).resolve().parent.parent)

def cleanNode(name):
    print("Cleaning ",name)
    def delIfThere(path):
        if os.path.exists(path):
            os.system("rm -rf " + path)

    #Remove the venv
    delIfThere(name + "/pyenv")
    delIfThere(name + "/CMakeCache.txt")
    delIfThere(name + "/CMakeFiles")
    delIfThere(name + "/cmake_install.cmake")
    delIfThere(name + "/Makefile")


def buildPyNode(name):
    print("Building Python Node", name)

    #Remove the venv
    print("Cleaning old Environment")
    os.system("rm -rf " + name + "/pyenv")

    #Make a new venv
    print("Creating new Environment")
    venv.create(name + '/pyenv', with_pip=True)

    #Install DEFCOM into the virtual environment
    #Get the system version
    sysVersion = sys.version_info
    versionName = "python{0}.{1}".format(sysVersion.major, sysVersion.minor)
    shutil.copytree(BASE_DIR + "/PythonLib/DEFCOM/", name + '/pyenv/lib/{}/site-packages/DEFCOM'.format(versionName))


    #Use the venv to install requirements
    print("Installing Requirements")
    subprocess.run([name + "/pyenv/bin/python", "-m", "pip", "install", "-r", name + "/requirements.txt"])

    print("Built Python Node", name)



def buildCNode(name):
    print("Building C++ Node", name)

    #Cmake the project
    subprocess.run(["cmake", "."], cwd=name)
    subprocess.run(["make"], cwd=name)
    print("Build C++ Node", name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: defcombuild <action> <value>")
        print("\nWhere action is one of [node, all, clean, cleanall]\n")
        print("Single Node:  defcombuild node <Node Name>")
        print("All Nodes:  defcombuild all")
        exit(1)

    if sys.argv[1] == "node":
        #Determine if it is a c or python node
        if os.path.exists(sys.argv[2] + "/CMakeLists.txt"):
            buildCNode(sys.argv[2])
        elif os.path.exists(sys.argv[2] + "/requirements.txt"):
            buildPyNode(sys.argv[2])
        else:
            print("Unknown Node Type")
            exit(1)

    elif sys.argv[1] == "all":
        for entry in os.listdir('.'):
            if os.path.isdir(entry):
                if os.path.exists(entry + "/CMakeLists.txt"):
                    buildCNode(entry)
                elif os.path.exists(entry + "/requirements.txt"):
                    buildPyNode(entry)

    elif sys.argv[1] == "clean":
        cleanNode(sys.argv[2])

    elif sys.argv[1] == "cleanall":
        for entry in os.listdir('.'):
            if os.path.isdir(entry):
                cleanNode(entry)


    else:
        print("Unknown Action")