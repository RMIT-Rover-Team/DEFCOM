#pragma once
#include <string>
#include "FlexibleMessageStructure.hpp"
#include "DefComParser.hpp"
#include <vector>
#include <thread>
#include <mutex>

class TXServerChannel {
    public:
        TXServerChannel(std::string defComFile, void (*handlerHook)(MessageStructure& request, MessageStructure& response));
        ~TXServerChannel();

    private:
        ConnectionSpecification _definition;

        //The hook
        void (*handlerHook)(MessageStructure& request, MessageStructure& response);

        //Hook mutex
        std::mutex hookMutex;

        //The File Descriptors for both the TCP and Unix sockets
        int tcpServer;
        int unixServer;

        //TCP Acceptor thread
        thread acceptorThreadTCP;

        //Unix Acceptor thread
        thread acceptorThreadUnix;

        //Vector of client threads
        std::vector<thread> clientThreads;



};