#include "DefComParser.hpp"
#include <netdb.h>
#include <arpa/inet.h>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <string>

struct recursiveTreeEntry{
    std::string value;
    std::map<std::string, recursiveTreeEntry> children;   
}

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

std::string stripWhitespace(const std::string& str) {
    std::string result;
    for (char c : str) {
        if (!std::isspace(c)) {
            result += c;
        }
    }
    return result;
}

void recursiveLoad(std::map<std::string, recursiveTreeEntry>& configStub, std::ifstream& fileObj){
    std::string line;
    
    while (std::getline(file, line)) {
        // Trim leading whitespace
        line = stripWhitespace(line);
        if (line.empty()) {
            continue;
        }

        if (line.at(0) == '#') {
            continue;
        }

        //If the end of the line is a close bracket, then we're done
        if (line.at(line.size() - 1) == '}') {
            return;
        }

        //Otherwise if it is an opening brace, then we're going to recurse
        if (line.at(line.size() - 1) == '{') {
            //Extract the name
            
            configStub.emplace()
            recursiveLoad()
        }
    }

}


ConnectionSpecification loadConfFile(std::string filename){
    std::map<std::string, recursiveTreeEntry> FileConfig;

    //emplace

    // Open the file
    std::ifstream confFile(filename);
    if (!confFile.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }

    //Read the config
    recursiveLoad(FileConfig, confFile);

}