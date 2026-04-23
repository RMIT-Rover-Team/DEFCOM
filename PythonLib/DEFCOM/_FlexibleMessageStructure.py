import struct

class MessageStructure:
    def __init__(self, structureDict: dict[str, str]):
        self.indexStarts = {}
        self.indexEnds = {}
        self.objTypes = {}
        self.totalSize = 0
        self.myArray = bytearray()

        # Add Data definitions internally
        for key in structureDict:
            typev = structureDict[key]
            if typev[-1] == ']':
                typev, count = typev[:-1].split("[")
                count = int(count)
            else:
                count = 1

            self._addDatatype(key, typev, count)

    # Add a definition to the message and resize the buffer
    def _addDatatype(self, key: str, vtype: str, count: int):
        self.indexStarts[key] = self.totalSize
        self.objTypes[key] = vtype

        print("Adding Type {} Length {} for {} index {}".format(vtype, count, key, self.totalSize))

        if (vtype == "int"):
            self.totalSize += 4 * count
        elif (vtype == "float"):
            self.totalSize += 4 * count
        elif (vtype == "char"):
            self.totalSize += 1 * count
        elif (vtype == "long"):
            self.totalSize += 8 * count
        elif (vtype == "string"):
            self.totalSize += count 
        elif (vtype == "bytes"):
            self.totalSize += count

        self.myArray = bytearray(self.totalSize)
        self.indexEnds[key] = self.totalSize


    def _getIndexOfDatablock(self, key: str) -> tuple[int,int]:
        return (self.indexStarts[key], self.indexEnds[key])
    
    #Although python supports multiple types, we break this out for parity sake
    #In fact, python makes this real nasty as we can't share pointers

    #Setters
    def setDouble(self, key: str, value: float, index: int = 0) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 8 * index
        self.myArray[bufferIndex:endIndex] = struct.pack('d', value)

    def setFloat(self, key: str, value: float, index: int = 0) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 4 * index
        self.myArray[bufferIndex:endIndex] = struct.pack('f', value)

    def setInt(self, key: str, value: int, index: int = 0) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 4 * index
        self.myArray[bufferIndex:endIndex] = struct.pack('i', value)

    def setLong(self, key: str, value: int, index: int = 0) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 8 * index
        self.myArray[bufferIndex:endIndex] = struct.pack('q', value)

    def setChar(self, key: str, value: bytes, index: int = 0) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 1 * index
        self.myArray[bufferIndex:endIndex] = value[0]

    def setBytes(self, key: str, value: bytes) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key)
        self.myArray[bufferIndex:endIndex] = value

    def setString(self, key: str, value: str) -> None:
        bufferIndex, endIndex = self._getIndexOfDatablock(key)

        for char in value:
            self.myArray[bufferIndex:endIndex] = ord(char)

    #Getters
    def getDouble(self, key: str, index: int = 0) -> float:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 8 * index
        return struct.unpack('d', self.myArray[bufferIndex:endIndex])[0]

    def getFloat(self, key: str, index: int = 0) -> float:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 4 * index
        return struct.unpack('f', self.myArray[bufferIndex:endIndex])[0]
    
    def getInt(self, key: str, index: int = 0) -> int:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 4 * index
        return struct.unpack('i', self.myArray[bufferIndex:endIndex])[0]

    def getLong(self, key: str, index: int = 0) -> int:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 8 * index
        return struct.unpack('q', self.myArray[bufferIndex:endIndex])[0]
    
    def getChar(self, key: str, index: int = 0) -> bytes:
        bufferIndex, endIndex = self._getIndexOfDatablock(key) + 1 * index
        return self.myArray[bufferIndex:endIndex]
    
    def getBytes(self, key: str) -> bytes:
        bufferIndex, endIndex = self._getIndexOfDatablock(key)
        return self.myArray[bufferIndex:endIndex]

    def getString(self, key: str) -> str:
        bufferIndex, endIndex = self._getIndexOfDatablock(key)

        string = ""
        index = bufferIndex
        for i in range(bufferIndex, endIndex):
            if self.myArray[index] == 0:
                break
            string += self.myArray[index].decode()
            index += 1
        return string
       

    #For communications, please don't touch unless you know what you are doing
    def getDecodeBuffer(self) -> bytes:
        return bytes(self.myArray)
    
    def setDecodeBuffer(self, buffer: bytes) -> None:
        self.myArray = bytearray(buffer)


        

    