#pragma once
#include "FlexibleMessageStructure.hpp"
#include <string>

struct ConnectionSpecification {
    std::string ResolvedIP;
    int NumericPort;
    std::string Name;

    MessageStructure RequestMessageFormat;
    MessageStructure ResponseMessageFormat;
};


