#pragma once
#include "GenericNetWrapper.hpp"
#include <string>
#include <iostream>
#include <string>
#include <cstring>
#include <ctime>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/un.h>
#include <sys/socket.h>


class UnixClientCon : public GenericNetWrapper {
    public:
        UnixClientCon(const std::string& path);
        ~UnixClientCon();
};

class UnixServerCon : public GenericNetWrapper {
    public:
        UnixServerCon(const std::string& path);
        ~UnixServerCon();
};