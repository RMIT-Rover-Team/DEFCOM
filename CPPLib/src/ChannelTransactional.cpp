#include "comms/UnixWrapper.hpp"
#include "comms/GenericNetWrapper.hpp"
#include "comms/TCPWrapper.hpp"
#include "ChannelTransactional.hpp"

TXServerChannel::TXServerChannel(std::string defComFile, void (*handlerHook)(MessageStructure* request, MessageStructure* response)){
    //Load the comms definitions
    this->definition = loadConfFile(defComFile);
    this->handlerHook = handlerHook;

    //Open the TCP server
    this->tcpServer = newTCPServer(this->definition.ResolvedIP, this->definition.NumericPort);

    //Open the Unix server
    this->unixServer = newUnixServer("/tmp/" + this->definition.Name);
}

TXServerChannel::~TXServerChannel(){
    //Join all the threads
    //acceptorThreadTCP.join();
    //acceptorThreadUnix.join();

    //Clean up dangling connections
    std::cout << "Shutting Down" << std::endl;
    for (size_t i = 0; i < clientConnections.size(); ) {
        delete clientConnections[i];
    }
    std::cout << "Destroy Clients" << std::endl;

}

void TXServerChannel::acceptorTCP(){
    while(true){
        //Accept the connection
        TCPServerCon* client = new TCPServerCon(this->tcpServer);

        //Log the connection
        std::cout << "Accepted TCP connection" << std::endl;

        this->spawnClient(client);
    }
}

void TXServerChannel::acceptorUnix(){
    while(true){
        //Accept the connection
        UnixServerCon* client = new UnixServerCon(this->unixServer);

        //Log the connection
        std::cout << "Accepted Unix connection" << std::endl;

        this->spawnClient(client);
    }
}

void TXServerChannel::spawnClient(GenericNetWrapper* client){
    //Lock the acceptor mutex
    this->acceptMutex.lock();

    //Spawn the client
    clientConnections.push_back(client);
    clientThreads.emplace_back(&TXServerChannel::clientProcess, this, client);

    //Clean up dead threads
    for (size_t i = 0; i < clientConnections.size(); ) {
        if (!clientConnections[i]->report().Alive) {
            //Free the client
            std::cout << "Del Client" << std::endl;
            delete clientConnections[i];

            //Join the thread
            std::cout << "Join Client" << std::endl;
            clientThreads[i].join();

            //erase both at the same index
            std::cout << "Err Client" << std::endl;
            clientConnections.erase(clientConnections.begin() + i);
            std::cout << "Err Client Th" << std::endl;
            clientThreads.erase(clientThreads.begin() + i);
            std::cout << "Done Del Client" << std::endl;

        } else {
            ++i;
        }
    }

    //Release the acceptor mutex
    this->acceptMutex.unlock();    
}

void TXServerChannel::clientProcess(GenericNetWrapper* client){
    while (client->report().Alive){
        //Get a message
        unsigned char* inbuffer = client->getdat(this->definition.RequestMessageFormat.totalSize);
        
        if (inbuffer == nullptr){ // Null message is end of stream
            break;
        }

        //Make local copies of the messages
        MessageStructure LocalRequest(this->definition.RequestMessageFormat);
        MessageStructure LocalResponse(this->definition.ResponseMessageFormat);

        //Copy the input buffer into the request
        LocalRequest.setDecodeBuffer(inbuffer);

        //Zero the output buffer
        memset(LocalResponse.getDecodeBuffer(), 0, LocalResponse.totalSize);

        //Lock the mutex
        this->hookMutex.lock();
        //Call the handler
        this->handlerHook(&LocalRequest, &LocalResponse);
        //Unlock the mutex
        this->hookMutex.unlock();

        //Reply with the response
        if (!client->senddat(LocalResponse.getDecodeBuffer(), LocalResponse.totalSize)){
            break;
        }

    }
    client->closeCon();
    std::cout << "Client closed" << std::endl;

}

void TXServerChannel::start(){
    acceptorThreadTCP = std::thread(&TXServerChannel::acceptorTCP, this);
    acceptorThreadUnix = std::thread(&TXServerChannel::acceptorUnix, this);
    
}