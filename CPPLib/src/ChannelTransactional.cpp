#include "comms/UnixWrapper.hpp"
#include "comms/GenericNetWrapper.hpp"
#include "comms/TCPWrapper.hpp"
#include "ChannelTransactional.hpp"

TXServerChannel::TXServerChannel(std::string defComFile, void (*handlerHook)(MessageStructure& request, MessageStructure& response)){
    //Load the comms definitions
    this->_definition = loadConfFile(defComFile);
    this->handlerHook = handlerHook;

    //Open the TCP server
    this->tcpServer = newTCPServer(this->_definition.ResolvedIP, this->_definition.NumericPort);

    //Open the Unix server
    this->unixServer = newUnixServer("/tmp/" + this->_definition.Name);
}

TXServerChannel::~TXServerChannel(){
    //Join all the threads
    //acceptorThreadTCP.join();
    //acceptorThreadUnix.join();

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
    std::thread clientThread(&TXServerChannel::clientProcess, this, client);
    clientThread.detach();


    //Release the acceptor mutex
    this->acceptMutex.unlock();

    
}

void TXServerChannel::start(){
    acceptorThreadTCP = std::thread(&TXServerChannel::acceptorTCP, this);
    acceptorThreadUnix = std::thread(&TXServerChannel::acceptorUnix, this);
    
}