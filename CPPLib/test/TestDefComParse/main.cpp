#include <iostream>
#include <map>
#include <iomanip>
#include "DefComParser.hpp"

using namespace std;

void hexDump(uint8_t* buffer, int size){
    for(int i = 0; i < size; i++){
        cout << std::hex << std::setw(2) << std::setfill('0') << (int)buffer[i] << " ";
        if (i % 16 == 15){
            cout << endl;
        }
    }
    cout << endl;
}

int main(int argc, char** argv) {
    cout << "Testing Parser" << endl;

    if (argc != 2){
        cout << "Usage: " << argv[0] << " <filename>" << endl;
        return 1;
    }

    cout << "Test Name2Port " << nameToPort("Test") << endl;
    cout << "Test FQDN DN" << resolveFQDN("localhost") << endl;
    cout << "Test FQDN IP" << resolveFQDN("127.0.0.1") << endl;

    cout << "Test Strip Whitespace " << stripWhitespace("the quick brown fox") << endl;

    loadConfFile(argv[1]);
    
    return 0;
}