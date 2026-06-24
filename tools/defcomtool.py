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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: defcomtool <py/cpp> <Node Name> <Flags>")
        print("Flags:")
        print("  -h, --help: Show this help")
        exit(1)

    #Check if it exists
    if os.path.exists(sys.argv[2]):
        print("Node already exists")
        exit(1)

    #Make sure it is a valid file name
    if not sys.argv[2].isidentifier():
        print("Invalid Node Name")
        exit(1)

    # Create the directory
    os.mkdir(sys.argv[2])
    os.mkdir(sys.argv[2] + '/COMFILES')

    # Copy a DEFCOM File template
    f = open(BASE_DIR + "/tools/template.defcom", "r")
    g = open(sys.argv[2] + '/COMFILES/template.defcom', "w")
    g.write(f.read()
            .replace("ServiceName", sys.argv[2])
            .replace("FullyQualifiedDomainName",socket.gethostname())
        )

    f.close()
    g.close()
    

    #Check if py or cpp
    if sys.argv[1] == "py":
        makePyProject(sys.argv[2])
    elif sys.argv[1] == "cpp":
        makeCPPProject(sys.argv[2])
    else:
        print("Unknown Language (Maybe in the future!)")

