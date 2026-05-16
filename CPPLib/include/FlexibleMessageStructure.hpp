#pragma once

#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <cstring>
#include <stdint.h>

enum class FType {
        INT,
        FLOAT,
        DOUBLE,
        CHAR,
        LONG,
        STRING,
        BYTES
};

struct FieldInfo {
        FType type;
        size_t start;
        size_t end;
        size_t count;
};

class MessageStructure {
public:
    size_t totalSize;

    MessageStructure(const std::map<std::string, std::string>& structureDict);

    ~MessageStructure();
    // -------------------------
    // Setters
    // -------------------------
    void setInt(const std::string& key, int value, size_t index = 0);

    void setFloat(const std::string& key, float value, size_t index = 0);

    void setDouble(const std::string& key, double value, size_t index = 0);

    void setLong(const std::string& key, long long value, size_t index = 0);

    void setChar(const std::string& key, char value, size_t index = 0);

    void setBytes(const std::string& key, uint8_t* data);

    void setString(const std::string& key, const std::string& value);

    // -------------------------
    // Getters
    // -------------------------
    int getInt(const std::string& key, size_t index = 0);

    float getFloat(const std::string& key, size_t index = 0);

    double getDouble(const std::string& key, size_t index = 0);

    long long getLong(const std::string& key, size_t index = 0);

    char getChar(const std::string& key, size_t index = 0);

    void getBytes(const std::string& key, uint8_t* dataBuffer);

    std::string getString(const std::string& key);

    // Raw buffer access
    uint8_t* getDecodeBuffer();

    void setDecodeBuffer(uint8_t* data);

private:
    std::map<std::string, FieldInfo> fields;
    uint8_t* buffer;
    

    // -------------------------
    // Helpers
    // -------------------------
    FType parseType(const std::string& t);

    size_t typeSize(FType t, size_t count);

    
};
