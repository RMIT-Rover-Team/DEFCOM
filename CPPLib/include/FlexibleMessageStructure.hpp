#pragma once

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <cstring>

enum class FType {
        INT,
        FLOAT,
        DOUBLE,
        CHAR,
        LONG,
        STRING,
        BYTES
};

class MessageStructure {
public:
    MessageStructure(const std::unordered_map<std::string, std::string>& structureDict);

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

    std::vector<uint8_t> getBytes(const std::string& key) {
        auto& f = fields[key];
        return std::vector<uint8_t>(buffer.begin() + f.start, buffer.begin() + f.end);
    }

    std::string getString(const std::string& key) {
        auto& f = fields[key];
        std::string s;

        for (size_t i = f.start; i < f.end; i++) {
            if (buffer[i] == 0) break;
            s.push_back(static_cast<char>(buffer[i]));
        }
        return s;
    }

    // Raw buffer access
    uint8_t* getDecodeBuffer();

    void setDecodeBuffer(uint8_t* data);

private:
    std::unordered_map<std::string, FieldInfo> fields;
    uint8_t* buffer;
    size_t totalSize;

    // -------------------------
    // Helpers
    // -------------------------
    FType parseType(const std::string& t);

    size_t typeSize(FType t, size_t count);

    struct FieldInfo {
        FType type;
        size_t start;
        size_t end;
        size_t count;
    };
};
