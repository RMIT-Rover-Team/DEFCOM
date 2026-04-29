import threading
from ._FlexibleMessageStructure import MessageStructure
from ._DefComParser import ConnectionSpecification as _ConnectionSpecification, loadConfFile as _loadConfFile
from ._TCPWrapper import clientTCPCon as _clientTCPCon, serverTCPCon as _serverTCPCon, newTCPServer as _newTCPServer
import time

class MulticastPublisher:
    #Initialise with the message structure definition (defcom file) and a function pointer
    #The function must be of the type:  void function(MessageStructure request, MessageStructure response)
    def __init__(self, defComFile: str):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        #A mutex for the sending thread
        self._sendMutex = threading.Lock()

        #Open the tcp server on the decoded port and address
        self._tcpServer = _newTCPServer(self._definition.ResolvedIP, self._definition.NumericPort)

        #The acceptor thread
        self._acceptorThread = threading.Thread(target=self._acceptor)

        #The client thread array
        self._clientThreads = []

        #Outgoing buffer
        self._outgoingQueues = {}

        self._acceptorThread.start()


    #Get a message to be filled in
    def getNewMessageObject(self) -> MessageStructure:
        return self._definition.RequestMessageFormat.clone()

    def publish(self,requestData: MessageStructure) -> MessageStructure:
        #Add the message to the outgoing queue
        with self._sendMutex:
            for key in self._outgoingQueues:
                self._outgoingQueues[key].append(requestData)

        

    # Internal thread that accepts client connections and spins off new threads for them
    def _acceptor(self):
        idCounter = 0
        while True:
            #Accept a client
            client = _serverTCPCon(self._tcpServer)
            print("Accepted Client {} on Port {}".format(client.info["Address"]["IP"], client.info["Address"]["Port"]))

            #Start a new thread to handle it
            clientNewThread = threading.Thread(target=self._clientProcess, args=(client,idCounter))
            clientNewThread.start()
            self._clientThreads.append(clientNewThread)
            idCounter += 1

            #Clean up dead clients
            ToCull = []
            for i in self._clientThreads:
                if not i.is_alive():
                    ToCull.append(i)
            for i in ToCull:
                self._clientThreads.remove(i)

            
            
    #The client handler thread
    def _clientProcess(self, con, myID):
        # Basically just wait for requests and provide responses
        Running = True
        with self._sendMutex:
            self._outgoingQueues[myID] = []

        while Running:
            if con.info["Alive"]:
                if len(self._outgoingQueues[myID]) > 0:
                    with self._sendMutex:
                        while len(self._outgoingQueues[myID]) > 0:
                            #Send the data
                            if not con.senddat(self._outgoingQueues[myID][0].getDecodeBuffer()):
                                Running = False

                            #Next message
                            self._outgoingQueues[myID] = self._outgoingQueues[myID][1:]
                else:
                    time.sleep(0.1)

        con.close()
        print("Client Disconnected {} port {}".format(con.info["Address"]["IP"], con.info["Address"]["Port"]))

        #Delete the queue
        with self._sendMutex:
            del self._outgoingQueues[myID]




class MulticastSubscriber:
    def __init__(self, defComFile: MessageStructure):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        #Connect to the server
        self._con = _clientTCPCon(self._definition.ResolvedIP, self._definition.NumericPort)
        print("Connected to {} port {}".format(self._definition.ResolvedIP, self._definition.NumericPort))

    def subscribe(self) -> MessageStructure:
        #Receive the response
        message = self._con.getdat(self._definition.RequestMessageFormat.totalSize)

        #Return the response
        response = self._definition.RequestMessageFormat.clone()
        
        if message:
            response.setDecodeBuffer(message)

        return response

    