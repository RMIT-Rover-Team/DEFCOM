# DEFCOM
DEFCOM is a lightweight communication framework designed to replace ROS/ROS2 in robotics deployments.  It facilitate seamless interaction between nodes using a variety of communication patterns, including Publisher/Subscriber, Lossy Multicast, and Transactional (Request/Response) channels
It supports both C++ and Python environments, providing a unified toolchain for building, managing, and launching multi-node projects

## Authors
-  Kaelan Grainger (MegaKG)

## Key Features
Multiple Channel Types:
* **Publisher / Subscriber**: Unidirectional, asynchronous broadcasting for data frames
* **Lossy Publisher / Subscriber**: UDP-based multicast (239.0.0.1) that ensures only the latest packet is processed, ideal for high-frequency data where latency is critical
* **Transactional**: Synchronous Request/Response pattern for traditional server-client interactions
* **Flexible Addressing**: Supports FQDN (resolved via DNS or /etc/hosts), direct IP addresses, and Unix sockets for local communication
* **Automatic Port Management**: Application names are automatically hashed into unique TCP ports, or can be manually specified
* **Standardized Message Objects**: All data is handled through a MessageStructure object supporting common c-types like int, float, string, bytes, char, and long


## Installation
To install the DEFCOM framework and its toolchain, run the provided installation script with root privileges:
sudo ./install.sh

## The DEFCOM Toolchain
DEFCOM provides three primary tools for managing projects:
- defcomtool: Used to create new nodes and generate launch files
- defcombuild: Handles building individual nodes or all nodes within a project directory, including environment cleaning
- defcomlaunch: Launches nodes according to the specifications in a launch.defcom file, forwarding output to a central terminal with node-specific prefixes
- defcomdump: A packet tracer and generator for debugging and testing DEFCOM nodes

## Getting Started
See the guide [here](Doc/gettingStarted.md)