#!/usr/bin/env python3

# Import your channel type(s)
from DEFCOM import ChannelTransactional
from DEFCOM import ChannelMulticast
from DEFCOM import ChannelLossyCast
from DEFCOM._FlexibleMessageStructure import MessageStructure
import time
import sys

sizes = {
    "int":4,
    "float":4,
    "char":1,
    "long":8
}

class defcomdumpapp:
    def __init__(self, path):
        self.path = path
        self.messageCounter = 0

    def _generateFakeMessage(self, messageIn: MessageStructure) -> MessageStructure:
        for key in messageIn._objTypes:
            kt = messageIn._objTypes[key]
            
            #Get the number of elements if it is an array
            elementTotalLength = messageIn._indexEnds[key] - messageIn._indexStarts[key]

            if kt in sizes:
                kn = elementTotalLength // sizes[kt]
            else:
                kn = elementTotalLength

            #Fill the message data
            if kt == 'int':
                for i in range(kn):
                    messageIn.setInt(key, (i+self.messageCounter), i)

            elif kt == 'float':
                for i in range(kn):
                    messageIn.setFloat(key, ((i+self.messageCounter))/1000, i)

            elif kt == 'char':
                for i in range(kn):
                    messageIn.setChar(key, chr(ord('a') + ((i + self.messageCounter) % kn)).encode(), i)

            elif kt == 'long':
                for i in range(kn):
                    messageIn.setLong(key, (i+self.messageCounter), i)

            elif kt == 'string':
                #Same as char, but fill the string
                st = ''
                for i in range(kn):
                    st += chr(ord('a') + ((i + self.messageCounter) % kn))
                st = st[:-1]
                messageIn.setString(key, st)

            elif kt == 'bytes':
                #Use bytearray
                b = bytearray()
                for i in range(kn):
                    b.append(((i + self.messageCounter) % kn) % 255)

                messageIn.setBytes(key, b)
        
        return messageIn


    #Subscribe to a Multicast Channel
    def startMulticast(self):
        print("Connecting to Multicast Session")

        con = ChannelMulticast.MulticastSubscriber(self.path)
        
        while True:
            message = con.subscribe()
            self._dumpMessage(message)


    def startTransactionalServer(self):
        def handler(messageIn, MessageOut):
            print("Received Request")
            self._dumpMessage(messageIn)

            MessageOut = self._generateFakeMessage(MessageOut)

        print("Hosting TX Server")
        con = ChannelTransactional.ServerChannel(self.path, handler)

        con.start()

        while True:
            time.sleep(1)

    def startTransactionalClient(self):
        print("Connecting to TX Server")
        con = ChannelTransactional.ClientChannel(self.path)

        while True:
            outgoing = self._generateFakeMessage(con.getNewRequestObject())
            result = con.request(outgoing)

            self._dumpMessage(result)

    #Subscribe to a LossyCast Channel
    def startLossyCast(self):
        print("Connecting to LossyCast Session")

        con = ChannelLossyCast.LossyCastSubscriber(self.path)
        
        while True:
            message = con.subscribe()
            self._dumpMessage(message)

    def _dumpMessage(self,message: MessageStructure):
        #Header with packet ID
        print("## FRAME ID: {}".format(self.messageCounter))

        #For each element in the message
        actionsArrayType = {
            "int":message.getInt,
            "float":message.getFloat,
            "char":message.getChar,
            "long":message.getLong
        }


        actionsStringType = {
            "string":message.getString,
            "bytes":message.getBytes
        }

        for key in message._objTypes:
            kt = message._objTypes[key]
            
            #Get the number of elements if it is an array
            elementTotalLength = message._indexEnds[key] - message._indexStarts[key]
            if kt in sizes:
                kn = elementTotalLength // sizes[kt]
            else:
                kn = elementTotalLength

            formatOut = ''

            #If it is a string, it is easy:
            if kt in actionsStringType:
                if (kt == 'bytes'):
                    #hexdump 
                    formatOut = "".join(["{:02x}".format(x) for x in actionsStringType[kt](key)])
                else:
                    formatOut = str(actionsStringType[kt](key))

            if kt in actionsArrayType:
                for i in range(kn):
                    if (kt == 'char'):
                        formatOut += "{:02x}".format(actionsArrayType[kt](key,i)[0]) + " "
                    else:
                        formatOut += str(actionsArrayType[kt](key,i)) + " "

            print(" [{:<6}]  {:<20}  {}".format(kt, key, formatOut))

        self.messageCounter += 1
        print()


if __name__ == "__main__":
    # Command requires a defcom file path to be provided
    if len(sys.argv) < 3:
        print("Usage: defcomdump <Mode> <defcomfile>")
        print("\nWhere Mode is one of [multicast, transactional, lossycast]\n")
        print("Transactional will default to a client sending fake data, however, you may specify either client or server as follows:")
        print("defcomdump transactional <defcomfile> <TXMode>")
        print("Where TXMode is either client or server")
        exit(1)

    #Create the app
    app = defcomdumpapp(sys.argv[2])

    if sys.argv[1] == "multicast":
        app.startMulticast()
    elif sys.argv[1] == "transactional":
        if len(sys.argv) == 4:
            if sys.argv[3] == "client":
                app.startTransactionalClient()
            elif sys.argv[3] == "server":
                app.startTransactionalServer()
        else:
            app.startTransactionalClient()

    elif sys.argv[1] == "lossycast":
        app.startLossyCast()

    