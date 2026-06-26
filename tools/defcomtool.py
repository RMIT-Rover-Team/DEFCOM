#!/usr/bin/env python3
import sys
import os
import venv
import shutil
from pathlib import Path
import socket

#Get the file dir
BASE_DIR = str(Path(__file__).resolve().parent.parent)

def makeCPPProject(name):
    #Make src and include directories
    os.mkdir(name + '/src')
    os.mkdir(name + '/include')
    os.mkdir(name + '/include/DEFCOM')

    #Copy the starter c++ file
    shutil.copy(BASE_DIR + "/tools/template.cpp", sys.argv[2] + '/src/main.cpp')

    #Copy DEFCOM into the node
    shutil.copytree(BASE_DIR + "/CPPLib/", name + '/external/DEFCOM')

    #Copy the starter cmake file
    f = open(BASE_DIR + "/tools/template.cmake", "r")
    g = open(sys.argv[2] + '/CMakeLists.txt', 'w')
    g.write(f.read().replace('PROJECT_NAME', name))
    g.close()
    f.close()

    print("Make C++ DEFCOM Project")

def makePyProject(name):
    # Create a virtual environment
    venv.create(name + '/pyenv', with_pip=True)

    # Create the pip requirements file
    open(name + "/requirements.txt", "a").close()

    #Get the system version
    sysVersion = sys.version_info
    versionName = "python{0}.{1}".format(sysVersion.major, sysVersion.minor)

    #Install DEFCOM into the virtual environment
    shutil.copytree(BASE_DIR + "/PythonLib/DEFCOM/", name + '/pyenv/lib/{}/site-packages/DEFCOM'.format(versionName))

    #Copy the starter python file
    shutil.copy(BASE_DIR + "/tools/template.py", name + '/main.py')

    #Copy the start script
    shutil.copy(BASE_DIR + "/tools/pystarttemplate.sh", name + '/' + name)
    os.chmod(name + '/' + name, 0o777)

    print("Make Python DEFCOM Project")

def makeNode():
    #Check if it exists
    if os.path.exists(sys.argv[3]):
        print("Node already exists")
        exit(1)

    #Make sure it is a valid file name
    if not sys.argv[3].isidentifier():
        print("Invalid Node Name")
        exit(1)

    # Create the directory
    os.mkdir(sys.argv[3])
    os.mkdir(sys.argv[3] + '/COMFILES')

    # Copy a DEFCOM File template
    f = open(BASE_DIR + "/tools/template.defcom", "r")
    g = open(sys.argv[3] + '/COMFILES/template.defcom', "w")
    g.write(f.read()
            .replace("ServiceName", sys.argv[3])
            .replace("FullyQualifiedDomainName",socket.gethostname())
        )

    f.close()
    g.close()
    

    #Check if py or cpp
    if sys.argv[2] == "py":
        makePyProject(sys.argv[3])
    elif sys.argv[2] == "cpp":
        makeCPPProject(sys.argv[3])
    else:
        print("Unknown Language (Maybe in the future!)")

def makeLauncher():
    #Check if it exists
    if os.path.exists('launch.defcom'):
        print("Launcher already exists")
        exit(1)

    #Find existing nodes
    Nodes = []
    for entry in os.listdir("."):
        if os.path.isdir(entry):
            #check if there is a COMFILES directory
            if os.path.exists(entry + "/COMFILES"):
                Nodes.append(entry)
                print("Found existing node: " + entry)

    #Enumerate over and add to the launch file
    f = open("launch.defcom","w")
    f.write("# Launch File - Specifies the order and delay after each node launch\n")
    f.write("Nodes {\n")
    for nid, Node in enumerate(Nodes):
        f.write("    " + Node + " {\n")
        f.write("        Order: {}\n".format(nid))
        f.write("        PostDelay: 0.1\n")
        f.write("        Args: []\n")
        f.write("    }\n")
    f.write("}\n")
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: defcomtool <action>")
        print("\nWhere action is one of [newnode, newlauncher]\n")
        print("New Node:  defcomtool newnode <py/cpp> <Node Name>")
        print("New Launcher:  defcomtool newlauncher")
        exit(1)

    if sys.argv[1] == "newnode":
        makeNode()
    elif sys.argv[1] == "newlauncher":
        makeLauncher()
    else:
        print("Unknown Action")

    

