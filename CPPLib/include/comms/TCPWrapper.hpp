#pragma once
#include "comms/GenericNetWrapper.hpp"
#include <iostream>
#include <string>
#include <cstring>
#include <ctime>
#include <unistd.h>
#include <arpa/inet.h>

class TCPClient : public GenericNetWrapper {
    public:
        TCPClient(const std::string& Host, int Port);
        ~TCPClient();

    private:
        int sockfd;
};