#include "FlexibleMessageStructure.hpp"
#include <stdint.h>

MessageStructure::MessageStructure(const std::map<std::string, std::string>& structureDict) {
    size_t offset = 0;
    totalSize = 0;

    for (auto& [key, typeStr] : structureDict) {
        std::string baseType = typeStr;
        size_t count = 1;

        // Parse array syntax: "int[4]"
        if (typeStr.back() == ']') {
            size_t pos = typeStr.find('[');
            baseType = typeStr.substr(0, pos);
            count = std::stoi(typeStr.substr(pos + 1, typeStr.size() - pos - 2));
        }

        FType t = parseType(baseType);
        size_t size = typeSize(t, count);

        fields[key] = { t, offset, offset + size, count };
        offset += size;
        totalSize += size;
        //printf("Add size %i to running %i\n", size, totalSize);
    }

    buffer = (uint8_t*)malloc(totalSize * sizeof(uint8_t));

    /* Dump the structure buffer*/
    printf("DEFCOM Frame:\n");
    for (auto& [key, typeStr] : structureDict) {
        auto& field = fields[key];
        printf("\tName %s Type of %s, Starts at %i ends at %i number of %i\n", key.c_str(), typeStr.c_str(), field.start, field.end, field.count);
    }
    
}

//The Setters
void MessageStructure::setInt(const std::string& key, int value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(int)*index);
    printf("Offset is %i, start is %i and raw index is %i", calculatedOffset, fields[key].start, sizeof(int) * index);
    memcpy(buffer + calculatedOffset, &value, sizeof(int));
}

void MessageStructure::setFloat(const std::string& key, float value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(float)*index);
    memcpy(buffer + calculatedOffset, &value, sizeof(float));
}

void MessageStructure::setDouble(const std::string& key, double value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(double)*index);
    memcpy(buffer + calculatedOffset, &value, sizeof(double));
}

void MessageStructure::setLong(const std::string& key, long long value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(long long)*index);
    memcpy(buffer + calculatedOffset, &value, sizeof(long long));
}

void MessageStructure::setChar(const std::string& key, char value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(char)*index);
    memcpy(buffer + calculatedOffset, &value, sizeof(char));
}

void MessageStructure::setBytes(const std::string& key, uint8_t* data){
    // Length of the data
    size_t dataLength = fields[key].end - fields[key].start;
    memcpy(buffer + fields[key].start, data, dataLength);
}

void MessageStructure::setString(const std::string& key, const std::string& value) {
    // Length of the data
    size_t dataLength = fields[key].end - fields[key].start;
    memset(buffer + fields[key].start, 0, dataLength);
    strcpy((char*)buffer + fields[key].start, value.c_str());
}

// The getters
int MessageStructure::getInt(const std::string& key, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(int)*index);
    int v;
    memcpy(&v, buffer + calculatedOffset, sizeof(int));
    return v;
}

float MessageStructure::getFloat(const std::string& key, size_t index) {
    float v;
    int calculatedOffset = fields[key].start + (sizeof(float)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(float));
    return v;
}

double MessageStructure::getDouble(const std::string& key, size_t index) {
    double v;
    int calculatedOffset = fields[key].start + (sizeof(double)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(double));
    return v;
}

long long MessageStructure::getLong(const std::string& key, size_t index) {
    long long v;
    int calculatedOffset = fields[key].start + (sizeof(long long)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(long long));
    return v;
}

char MessageStructure::getChar(const std::string& key, size_t index) {
    char v;
    int calculatedOffset = fields[key].start + (sizeof(char)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(char));
    return v;
}

void MessageStructure::getBytes(const std::string& key, uint8_t* dataBuffer) {
    auto& f = fields[key];
    memcpy(dataBuffer, buffer + f.start, f.end - f.start);
}

std::string MessageStructure::getString(const std::string& key) {
    auto& f = fields[key];
    
    //Some funny string magic to scare Jonathan
    char* myRawData = (char*)buffer + f.start;

    std::string out = myRawData;
    return out;
}


// The Helpers
FType MessageStructure::parseType(const std::string& t) {
    if (t == "int") return FType::INT;
    if (t == "float") return FType::FLOAT;
    if (t == "double") return FType::DOUBLE;
    if (t == "char") return FType::CHAR;
    if (t == "long") return FType::LONG;
    if (t == "string") return FType::STRING;
    if (t == "bytes") return FType::BYTES;
    throw std::runtime_error("Unknown type: " + t);
}

size_t MessageStructure::typeSize(FType t, size_t count) {
    switch (t) {
        case FType::INT: return 4 * count;
        case FType::FLOAT: return 4 * count;
        case FType::DOUBLE: return 8 * count;
        case FType::CHAR: return 1 * count;
        case FType::LONG: return 8 * count;
        case FType::STRING: return count + 1;
        case FType::BYTES: return count;
    }
    return 0;
}

// Raw buffer access
uint8_t* MessageStructure::getDecodeBuffer() {
    return buffer;
}

void MessageStructure::setDecodeBuffer(uint8_t* data) {
    memcpy(buffer, data, totalSize);
}

//Destructor
MessageStructure::~MessageStructure() {
    free(buffer);
}