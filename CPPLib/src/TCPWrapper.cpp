#include "comms/GenericNetWrapper.hpp"
#include "comms/TCPWrapper.hpp"

int newTCPServer(const std::string& Host, int Port) {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt));

    sockaddr_in serv{};
    serv.sin_family = AF_INET;
    serv.sin_port = htons(Port);
    inet_pton(AF_INET, Host.c_str(), &serv.sin_addr);

    bind(server_fd, (sockaddr*)&serv, sizeof(serv));
    listen(server_fd, 1);

    return server_fd;
}


TCPClient::TCPClient(const std::string& Host, int Port) {
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serv{};
    serv.sin_family = AF_INET;
    serv.sin_port = htons(Port);
    inet_pton(AF_INET, Host.c_str(), &serv.sin_addr);

    connect(sockfd, (sockaddr*)&serv, sizeof(serv));

    //Set up the statistics
    double now = time(nullptr);
    this->info.InitTime = now;
    this->info.LastPacket = now;
    this->info.IP = Host;
    this->info.Port = Port;
}

TCPClient::~TCPClient() {
    this->close(sockfd);
}