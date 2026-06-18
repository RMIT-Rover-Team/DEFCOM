#pragma once
#include "GenericNetWrapper.hpp"
#include <string>

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