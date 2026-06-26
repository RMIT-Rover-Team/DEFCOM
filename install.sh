#!/bin/sh
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo or as root."
    exit 1
fi

#copy the libraries
mkdir /opt/DEFCOM
cp -rv CPPLib PythonLib tools /opt/DEFCOM

# add the executables
cp -v tools/installed/* /usr/sbin
chmod +x /usr/sbin/defcomtool
chmod +x /usr/sbin/defcombuild
chmod +x /usr/sbin/defcomlaunch

echo "Installed DEFCOM!"