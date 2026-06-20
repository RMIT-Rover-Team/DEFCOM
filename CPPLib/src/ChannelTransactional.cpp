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

}

TXServerChannel::start(){
    
}