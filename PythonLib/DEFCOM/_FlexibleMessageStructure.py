import struct

class MessageStructure:
    def __init__(self):
        self.indexStarts = {}
        self.objTypes = {}
        self.totalSize = 0
        self.myArray = bytearray()

    def addDatatype(self, key: str, vtype: str, count: int):
        self.indexStarts[key] = self.totalSize
        self.objTypes[key] = vtype

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

        self.myArray = bytearray(self.totalSize)


    def _getIndexOfDatablock(self, key: str) -> int:
        return self.indexStarts[key]
    
    #Although python supports multiple types, we break this out
    def setDouble(self, key: str, value: float, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 8 * index
        self.myArray[bufferIndex:bufferIndex+8] = struct.pack('d', value)

    def setFloat(self, key: str, value: float, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 4 * index
        self.myArray[bufferIndex:bufferIndex+4] = struct.pack('f', value)

    def setInt(self, key: str, value: int, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 4 * index
        self.myArray[bufferIndex:bufferIndex+4] = struct.pack('i', value)

    def setLong(self, key: str, value: int, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 8 * index
        self.myArray[bufferIndex:bufferIndex+8] = struct.pack('q', value)

    def setChar(self, key: str, value: str, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 1 * index
        self.myArray[bufferIndex:bufferIndex+1] = value

    def setString(self, key: str, value: str, index: int = 0) -> None:
        bufferIndex = self._getIndexOfDatablock(key) + 1 * index

        for char in value:
            self.myArray[bufferIndex:bufferIndex+1] = ord(char)

    


        

    