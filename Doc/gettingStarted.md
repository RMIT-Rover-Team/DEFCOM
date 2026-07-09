# DEFCOM C++ API definition Version 1.0 (26/06/2026)
## Authors:
* Kaelan Grainger (MegaKG)

## Table of Contents:
- [DEFCOM C++ API definition Version 1.0 (26/06/2026)](#defcom-c-api-definition-version-10-26062026)
  - [Authors:](#authors)
  - [Table of Contents:](#table-of-contents)
  - [Quickstart Guide](#quickstart-guide)
    - [Key References:](#key-references)
    - [Installation:](#installation)
    - [The Toolchain](#the-toolchain)
    - [My First Node](#my-first-node)
    - [Building your nodes](#building-your-nodes)
    - [Launch Files and multi-node projects](#launch-files-and-multi-node-projects)


## Quickstart Guide

### Key References:
* [Architecture & DEFCOM File Format](architecture.md)
* [C++ API Definition](api_cpp.md)
* [Python API Definition](api_python.md)

### Installation:
Installation of DEFCOM is handled by the `install.sh` script.
This needs to be run with root privileges and installs to the /opt/ and /usr/sbin directories.

```bash
sudo bash install.sh
```


### The Toolchain

The DEFCOM toolchain consists of the following:
* `defcomtool` - Used for creating DEFCOM nodes and launch files in a directory.
* `defcombuild` - Used to build individual or all DEFCOM nodes in a directory. Also performs cleaning of build files.
* `defcomlaunch` - Used to launch DEFCOM nodes according to a launch file.
* `defcomdump` - A packet tracer and generator for debugging and testing DEFCOM nodes.

Each tool must be run in the parent directory of a DEFCOM project, containing all the nodes within.

A typical file structure would be as follows:
```
|
|--- Project Folder
    |--- Node1
    |   |--- Node Files & Folders
    |--- Node2
    |   |--- Node Files & Folders
    |--- launch.defcom
```

### My First Node

In the directory you wish to create a DEFCOM node:
```bash
# For Python Node
defcomtool newnode py MyNodeName

# For C++ Node
defcomtool newnode cpp MyNodeName
```

This will create a folder named `MyNodeName` within the current directory. 

A python node will contain the following:
* `COMFILES` - A folder containing DEFCOM files for your node.
* `pyenv` - The python virtual environment for the node.
* `requirements.txt` - The list of dependencies for the node to be installed by pip during building.
* `main.py` - The main python file for your code. 
* `MyNodeName` - Will vary depending on your node name, is an executable file that will launch the node. You can run this to debug your code.


Similarly, a C++ node will contain the following:
* `COMFILES` - A folder containing DEFCOM files for your node.
* `CMakeLists.txt` - The cmake configuration file for your node - includes c++ compile arguments etc...
* `src/main.cpp` - The main c++ file for your code.
* `include/` - The header files for your code.
* `external/` - Contains DEFCOM and any other external libraries you wish to use
* `MyNodeName` - Will vary depending on your node name, is an executable file that will launch the node. You can run this to debug your code.

### Building your nodes

Nodes are designed to allow either independent or multi-node projects.

By default, the file of the same name as the node can be executed to launch the node.
C++ nodes can be manually built as follows to produce this file:
```bash
cd MyNodeName
cmake .
make
./MyNodeName
```

A **much easier** solution is to use the `defcombuild` tool.

To build a specific node:
```bash
defcombuild node MyNodeName
```

To build all nodes:
```bash
defcombuild all
```

Similarly, to clean the build environment:

For single nodes:
```bash
defcombuild clean MyNodeName
```

For all nodes:
```bash
defcombuild cleanall
```


### Launch Files and multi-node projects

`defcomtool` can also be used to create launch files for your nodes.

In the parent directory of a DEFCOM project, run:
```bash
defcomtool newlauncher
```

This will scan through the current directory for any nodes create a file called `launch.defcom` specifying the order and post delay of each node.
You will need to edit this file to adjust the order as required.

For file format, see the [launch file format](architecture.md#defcom-launch-files).

The `defcomlaunch` tool can be used to launch nodes in a directory.

In the parent directory of a DEFCOM project, run:
```bash
defcomlaunch
```

This will launch all nodes in the current directory according to the order and delay specified in the launch file.
Node STDOUT and STDERR will be labelled with a prefix containing the Node name and forwarded to the terminal.
