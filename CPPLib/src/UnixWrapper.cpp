#include "comms/GenericNetWrapper.hpp"
#include "comms/UnixWrapper.hpp"

int newUnixServer(const std::string& path) {
    int server_fd = socket(AF_UNIX, SOCK_STREAM, 0);

    sockaddr_un addr{};
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path.c_str(), sizeof(addr.sun_path)-1);

    unlink(path.c_str());
    bind(server_fd, (sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);

    return server_fd;
}