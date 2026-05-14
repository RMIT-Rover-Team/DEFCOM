#include "FlexibleMessageStructure.hpp"

MessageStructure::MessageStructure(const std::unordered_map<std::string, std::string>& structureDict) {
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
    }

    buffer = (uint8_t*)malloc(totalSize * sizeof(uint8_t));
    
}

//The Setters
void MessageStructure::setInt(const std::string& key, int value, size_t index) {
    int calculatedOffset = fields[key].start + (sizeof(int)*index);
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
    strcpy(buffer + fields[key].start, value.c_str());
}

// The getters
int MessageStructure::getInt(const std::string& key, size_t index = 0) {
    int calculatedOffset = fields[key].start + (sizeof(int)*index);
    int v;
    memcpy(&v, buffer + calculatedOffset, sizeof(int));
    return v;
}

float MessageStructure::getFloat(const std::string& key, size_t index = 0) {
    float v;
    int calculatedOffset = fields[key].start + (sizeof(float)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(float));
    return v;
}

double MessageStructure::getDouble(const std::string& key, size_t index = 0) {
    double v;
    int calculatedOffset = fields[key].start + (sizeof(double)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(double));
    return v;
}

long long MessageStructure::getLong(const std::string& key, size_t index = 0) {
    long long v;
    int calculatedOffset = fields[key].start + (sizeof(long long)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(long long));
    return v;
}

char MessageStructure::getChar(const std::string& key, size_t index = 0) {
    char v;
    int calculatedOffset = fields[key].start + (sizeof(char)*index);
    memcpy(&v, buffer + calculatedOffset, sizeof(char));
    return v;
}





// The Helpers
FType MessageStructure::parseType(const std::string& t) {
    if (t == "int") return Type::INT;
    if (t == "float") return Type::FLOAT;
    if (t == "double") return Type::DOUBLE;
    if (t == "char") return Type::CHAR;
    if (t == "long") return Type::LONG;
    if (t == "string") return Type::STRING;
    if (t == "bytes") return Type::BYTES;
    throw std::runtime_error("Unknown type: " + t);
}

size_t MessageStructure::typeSize(FType t, size_t count) {
    switch (t) {
        case Type::INT: return 4 * count;
        case Type::FLOAT: return 4 * count;
        case Type::DOUBLE: return 8 * count;
        case Type::CHAR: return 1 * count;
        case Type::LONG: return 8 * count;
        case Type::STRING: return count + 1;
        case Type::BYTES: return count;
    }
    return 0;
}

// Raw buffer access
uint8_t* MessageStructure::getDecodeBuffer() {
    return buffer;
}

void setDecodeBuffer(uint8_t* data) {
    memcpy(buffer, data, totalSize);
}
