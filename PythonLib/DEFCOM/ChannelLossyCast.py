import threading
from ._FlexibleMessageStructure import MessageStructure
from ._DefComParser import ConnectionSpecification as _ConnectionSpecification, loadConfFile as _loadConfFile
from ._UDPWrapper import udpsend, udpget

import time
import os
import struct

class LossyCastPublisher:
    #Initialise with the message structure definition (defcom file) and a function pointer
    #The function must be of the type:  void function(MessageStructure request, MessageStructure response)
    def __init__(self, defComFile: str):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        if self._definition.RequestMessageFormat.totalSize > 1000:
            raise Exception('Message size too large for UDP')
        
        self._con = udpsend('224.0.0.1', self._definition.NumericPort, self._definition.RequestMessageFormat.totalSize + 8)

        self.sequence = 0

    #Get a message to be filled in
    def getNewMessageObject(self) -> MessageStructure:
        return self._definition.RequestMessageFormat.clone()

    def publish(self,requestData: MessageStructure):
        #Get the buffer
        buffer = requestData.getDecodeBuffer()
        buffer = struct.pack('Q',self.sequence) + buffer

        self._con.senddat(buffer)

        #Add a sequence header to it
        self.sequence += 1
        


    


class LossyCastSubscriber:
    def __init__(self, defComFile: str):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        if self._definition.RequestMessageFormat.totalSize > 1000:
            raise Exception('Message size too large for UDP')

        #Connect to the server
        self._con = udpget('224.0.0.1', self._definition.NumericPort, self._definition.RequestMessageFormat.totalSize + 8)

        self.lastSequence = 0
        

    def subscribe(self) -> MessageStructure:
        #Receive the response
        while True:
            message = self._con.getdat()

            #Get the sequence
            sequence = struct.unpack('Q',message[:8])[0]
            if sequence > self.lastSequence:
                self.lastSequence = sequence
                message = message[8:]
                break
            
        #Return the response
        response = self._definition.RequestMessageFormat.clone()
        
        if message:
            response.setDecodeBuffer(message)

        return response

    