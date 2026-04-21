from dataclasses import dataclass
import socket
import io

@dataclass
class ConnectionSpecification:
    #Connection Orientation
    ResolvedIP: str
    NumericPort: int

    #The Request / Multicast message (main payload for Multicast)
    #Format - dictionary of [key: value] like ["VariableName":"VariableType"]
    RequestMessageFormat: dict[str, str]

    #The Response message for Transactional connections
    ResponseMessageFormat: dict[str, str]


#Hash string names into ports (to make naming easier)
def nameToPort(name: str) -> int:
    count = 0
    for c in name:
        count = count * 31 + ord(c)
    return 2000 + (count % 60000)

#Resolve a FQDN to an IP address
def resolveFQDN(fqdn: str) -> str:
    return socket.gethostbyname(fqdn)

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

def loadConfFile(filename: str) -> ConnectionSpecification:
    f = open(filename, "r")

    #The overall dictionary
    LoadedData = _recursiveLoad(f)

    f.close()

    #Decode the IP and port
    RawPort, RawFQDN = LoadedData["Name"].split("@")
    IP = resolveFQDN(RawFQDN)

    if RawPort.isdigit():
        PORT = int(RawPort)
    else:
        PORT = nameToPort(RawPort)

    print("Connection {} Specified on {} port {}".format(LoadedData["Name"],IP, PORT))
    return ConnectionSpecification(IP, PORT, LoadedData["RequestFormat"], LoadedData["ResponseFormat"])

    