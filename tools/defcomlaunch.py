#!/usr/bin/env python3
import sys
import os
import subprocess
import io
import asyncio

#Load up a file
def _recursiveLoad(f: io.TextIOWrapper) -> dict[str, str]:
    LoadedData = {}

    while True:
        line = f.readline()
        
        #End of file
        if line == "":
            break

        #Strip the whitespace
        line = line.strip().replace(" ","").replace("\t","")

        #If the line is now empty, ignore it
        if line == "":
            continue

        #End of segment
        if line[-1] == "}":
            break
        
        #Ignore comments
        if line[0] == "#":
            continue

        #Start of recursive Segment
        if line[-1] == "{":
            LoadedData[line.replace("{","")] = _recursiveLoad(f)
            continue

        #Otherwise we split into key and value
        key, value = line.split(":")
        LoadedData[key] = value
    return LoadedData

async def readStream(stream, prefix, startcol):
    while True:
        line = await stream.readline()
        if not line:
            break
        print(startcol + f"{prefix} {line.decode().rstrip()}\033[0m")

async def runProcess(prefixname,cmdline):
    #print(os.listdir())
    proc = await asyncio.create_subprocess_exec(
        *cmdline,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd= os.getcwd() + '/' + cmdline[0] + '/'
    )

    await asyncio.gather(
        readStream(proc.stdout, f"[{prefixname}][stdout]", "\033[32m"),
        readStream(proc.stderr, f"[{prefixname}][stderr]", "\033[31m")
    )

    return await proc.wait()

async def launchNodes(NodeList):
    tasks = []

    #Start each node in order
    for orderID in sorted(list(NodeList.keys())):
        Name = NodeList[orderID][0]
        Delay = NodeList[orderID][1]
        Args = NodeList[orderID][2]
        print(orderID,':',"Starting",Name,'with args',Args)

        #Check if the node has been compiled
        if not os.path.exists(Name + '/' + Name):
            print("\t- \033[31m" + Name + " doesn't have an executable file of the same name, did you remember to compile it?" + "\033[0m")
        else:
            #Start the subprocess
            tasks.append(asyncio.create_task(runProcess(Name, ['./' + Name]+Args)))

            #delay between launches
            await asyncio.sleep(Delay)

        print()

    #Keep parent alive until children die
    await asyncio.gather(*tasks)

    


if __name__ == "__main__":
    #check if a launch file exists
    if not os.path.exists("launch.defcom"):
        print("No Launch File Found, try use \'defcomtool newlauncher\'")
        exit(1)


    #Load up the file
    LoadedData = None
    with open("launch.defcom", "r") as f:
        LoadedData = _recursiveLoad(f)

    if LoadedData == None:
        print("Empty or Invalid launch file")
        exit(1)

    #Check if Nodes is defined
    if "Nodes" not in LoadedData:
        print("No Nodes defined in launch file")
        exit(1)

    #Extract the nodes in order
    Nodes = {}
    for Node in LoadedData["Nodes"]:
        try:
            Nodes[int(LoadedData["Nodes"][Node]["Order"])] = (Node, float(LoadedData["Nodes"][Node]["PostDelay"]), LoadedData["Nodes"][Node]["Args"][1:-1].split(','))
        except Exception as E:
            print("Invalid data in " + Node + " - " + str(E))

    asyncio.run(launchNodes(Nodes))