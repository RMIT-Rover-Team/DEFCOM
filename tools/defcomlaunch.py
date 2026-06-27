#!/usr/bin/env python3
import sys
import os
import subprocess
import io
import asyncio
import pty

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



async def runProcess(prefixname, cmdline):
    # Create PTYs for stdout and stderr
    stdout_master, stdout_slave = pty.openpty()
    stderr_master, stderr_slave = pty.openpty()

    proc = await asyncio.create_subprocess_exec(
        *cmdline,
        stdin=asyncio.subprocess.DEVNULL,
        stdout=stdout_slave,
        stderr=stderr_slave,
        cwd=os.getcwd() + '/' + cmdline[0] + '/',
    )

    # Close slave ends in parent
    os.close(stdout_slave)
    os.close(stderr_slave)

    loop = asyncio.get_running_loop()

    async def pump(fd, color, label):
        while True:
            try:
                data = await loop.run_in_executor(None, os.read, fd, 1024)
                if not data:
                    break
                print(color + f"{label} {data.decode().rstrip()}\033[0m")
            except OSError:
                break

    stdout_task = asyncio.create_task(
        pump(stdout_master, "\033[32m", f"[{prefixname}][stdout]")
    )
    stderr_task = asyncio.create_task(
        pump(stderr_master, "\033[31m", f"[{prefixname}][stderr]")
    )

    try:
        await asyncio.gather(stdout_task, stderr_task)
    except asyncio.CancelledError:
        proc.kill()
        await proc.wait()
        raise
    finally:
        os.close(stdout_master)
        os.close(stderr_master)

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
    FILE = "launch.defcom"
    if len(sys.argv) == 2:
        print("Override default launch file to ",sys.argv[1])
        FILE = sys.argv[1]

    #check if a launch file exists
    if not os.path.exists(FILE):
        print("Launch File Not Found, try use \'defcomtool newlauncher\'")
        exit(1)


    #Load up the file
    LoadedData = None
    with open(FILE, "r") as f:
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