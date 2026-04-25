import threading
from ._FlexibleMessageStructure import MessageStructure
from ._DefComParser import ConnectionSpecification as _ConnectionSpecification, loadConfFile as _loadConfFile
from ._TCPWrapper import clientCon as _clientCon, serverCon as _serverCon, newServer as _newServer

class ServerChannel:
    #Initialise with the message structure definition (defcom file) and a function pointer
    #The function must be of the type:  void function(MessageStructure request, MessageStructure response)
    def __init__(self, defComFile: str, handlerHook: callable):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        #As I have no faith in people writing thread safe code, we mutex the hook
        self._hookMutex = threading.Lock()
        self._hook: callable = handlerHook

        #Open the tcp server on the decoded port and address
        self._tcpServer = _newServer(self._definition.ResolvedIP, self._definition.NumericPort)

        #The acceptor thread
        self._acceptorThread = threading.Thread(target=self._acceptor)

        #The client thread array
        self._clientThreads = []

    # Internal thread that accepts client connections and spins off new threads for them
    def _acceptor(self):
        
        while True:
            #Accept a client
            client = _serverCon(self._tcpServer)
            print("Accepted Client {} on Port {}".format(client.info["Address"]["IP"], client.info["Address"]["Port"]))

            #Start a new thread to handle it
            clientNewThread = threading.Thread(target=self._clientProcess, args=(client,))
            clientNewThread.start()
            self._clientThreads.append(clientNewThread)

            #Clean up dead clients
            ToCull = []
            for i in self._clientThreads:
                if not i.is_alive():
                    ToCull.append(i)
            for i in ToCull:
                self._clientThreads.remove(i)
            
    #The client handler thread
    def _clientProcess(self, con):
        # Basically just wait for requests and provide responses
        while True:
            if con.info["Alive"]:
                message = con.getdat(self._definition.RequestMessageFormat.totalSize)

                if not message: #Null message is broken connection
                    break

                #Copy the requets and reply objects so we can mess with them
                LocalRequest = self._definition.RequestMessageFormat.clone()
                LocalResponse = self._definition.ResponseMessageFormat.clone()

                #Copy the message into the buffer
                LocalRequest.setDecodeBuffer(message)

                #Zero the response buffer
                LocalResponse.setDecodeBuffer(bytes(self._definition.ResponseMessageFormat.totalSize))

                #Lock the hook mutex
                with self._hookMutex:
                    #Call the hook
                    self._hook(LocalRequest,LocalResponse)

                #Reply with the response
                if not con.senddat(LocalResponse.getDecodeBuffer()):
                    break #If the send fails we die
            else:
                break
        con.close()
        print("Client Disconnected {} port {}".format(con.info["Address"]["IP"], con.info["Address"]["Port"]))

    #Starts everything running explicitly - this may be redundant tbh
    def start(self):
        self._acceptorThread.start()



class ClientChannel:
    def __init__(self, defComFile: MessageStructure):
        self._definition: _ConnectionSpecification = _loadConfFile(defComFile)

        #Connect to the server
        self._con = _clientCon(self._definition.ResolvedIP, self._definition.NumericPort)
        print("Connected to {} port {}".format(self._definition.ResolvedIP, self._definition.NumericPort))

    #Get a request to be filled in
    def getNewRequestObject(self) -> MessageStructure:
        return self._definition.RequestMessageFormat.clone()

    def request(self,requestData: MessageStructure) -> MessageStructure:
        #Send the data
        self._con.senddat(requestData.getDecodeBuffer())

        #Receive the response
        message = self._con.getdat(self._definition.ResponseMessageFormat.totalSize)

        #Return the response
        response = self._definition.ResponseMessageFormat.clone()
        
        if message:
            response.setDecodeBuffer(message)

        return response