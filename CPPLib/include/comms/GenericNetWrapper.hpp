#pragma once

struct ConnInfo {
    long TotalSent = 0;
    long TotalRecv = 0;
    double InitTime = 0;
    double LastPacket = 0;
    bool Alive = true;
};


class GenericNetWrapper {
    public:
        void senddat(unsigned char* data, int bufsize = 1024);
        unsigned char* getdat(int bufsize = 1024);
        void close();
        bool isAlive();
        ConnInfo report();

    protected:
        ConnInfo info;
        char* buffer = nullptr;
}