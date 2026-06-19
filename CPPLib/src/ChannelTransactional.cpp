#include "comms/UnixWrapper.hpp"
#include "comms/GenericNetWrapper.hpp"
#include "comms/TCPWrapper.hpp"
#include "ChannelTransactional.hpp"

TXServerChannel::TXServerChannel(std::string defComFile, void (*handlerHook)(MessageStructure& request, MessageStructure& response)){
    //Load the comms definitions
    this->_definition = loadConfFile(defComFile);
    this->handlerHook = handlerHook;

    
}