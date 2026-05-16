#include "DefComParser.hpp"
#include <netdb.h>
#include <arpa/inet.h>
#include <stdexcept>

int nameToPort(const std::string& name) {
    long long count = 0;
    for (char c : name) {
        count = count * 31 + static_cast<unsigned char>(c);
    }
    return 2000 + (count % 60000);
}

std::string resolveFQDN(const std::string& fqdn) {
    // Check if it's already a valid IPv4 address
    sockaddr_in sa{};
    if (inet_pton(AF_INET, fqdn.c_str(), &(sa.sin_addr)) == 1) {
        return fqdn;  // Already an IP
    }

    // Otherwise try resolve as hostname
    addrinfo hints{}, *res = nullptr;

    hints.ai_family = AF_INET; // IPv4 only

    if (getaddrinfo(fqdn.c_str(), nullptr, &hints, &res) != 0) {
        throw std::runtime_error("Failed to resolve hostname: " + fqdn);
    }

    char ipStr[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &((sockaddr_in*)res->ai_addr)->sin_addr, ipStr, sizeof(ipStr));

    freeaddrinfo(res);
    return std::string(ipStr);
}
