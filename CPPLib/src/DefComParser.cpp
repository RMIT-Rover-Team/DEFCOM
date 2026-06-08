#include "DefComParser.hpp"
#include "FlexibleMessageStructure.hpp"
#include <netdb.h>
#include <arpa/inet.h>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

struct recursiveTreeEntry{
    std::string value;
    std::map<std::string, recursiveTreeEntry> children;   
};

int nameToPort(const std::string& name) {
    unsigned long long count = 0;
    for (char c : name) {
        
        count = (count * 31 + static_cast<unsigned char>(c)) % ((1 << 16) - 1);
    }
    return 2000 + (count % 60000);
}

int is_integer(const std::string& s) {
    if (s.empty()) return false;

    size_t i = 0;

    if (s[0] == '-' || s[0] == '+') {
        if (s.size() == 1) return false; // just "+" or "-"
        i = 1;
    }

    for (; i < s.size(); i++) {
        if (!std::isdigit(s[i])) return false;
    }

    return true;
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
    size_t pos;
    
    while (std::getline(fileObj, line)) {
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
            //Create object
            struct recursiveTreeEntry newEntry;
            configStub.emplace(line.substr(0,line.size()-1), newEntry);

            std::cout << "Create Sublist " << line.substr(0,line.size()-1) << std::endl;

            recursiveLoad(configStub[line.substr(0,line.size()-1)].children, fileObj);
            continue;
        }

        //Otherwise it is a regular line
        pos = line.find(':');

        if (pos == std::string::npos){
            std::cerr << "Config line error " << line << std::endl;
            continue;
        }
        struct recursiveTreeEntry newValEntry;
        newValEntry.value = line.substr(pos+1);
        configStub.emplace(line.substr(0,pos), newValEntry);

        std::cout << "Inserted " << line.substr(0,pos) << " = " << line.substr(pos+1) << std::endl;




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

    // Close the file
    confFile.close();

    //Check if the FQDN is there
    if (FileConfig.find("Name") == FileConfig.end()){
        throw std::runtime_error("No Service Name Specified");
    }

    //Resolve the Service Name
    size_t pos = FileConfig["Name"].value.find('@');

    std::string ResolvedIP = resolveFQDN(FileConfig["Name"].value.substr(pos+1));

    int NumericPort;
    if (is_integer(FileConfig["Name"].value.substr(0,pos))){
        NumericPort = std::stoi(FileConfig["Name"].value.substr(0,pos));
    }
    else {
        std::cout << "Hashing port \"" << FileConfig["Name"].value.substr(0,pos) << "\"\n";

        NumericPort = nameToPort(FileConfig["Name"].value.substr(0,pos));
    } 
    std::cout << "Connection Specified: " << FileConfig["Name"].value << " Resolved IP: " << ResolvedIP << " Port: " << NumericPort << std::endl;

    struct ConnectionSpecification myCon;

    myCon.ResolvedIP = ResolvedIP;
    myCon.NumericPort = NumericPort;
    myCon.Name = FileConfig["Name"].value;

}