cmake_minimum_required(VERSION 3.16)
project(CPPLib LANGUAGES CXX)

# Create the library from all .cpp files in src/
file(GLOB_RECURSE CPPLIB_SOURCES src/*.cpp)

add_library(CPPLib STATIC ${CPPLIB_SOURCES})

# Public include directory
target_include_directories(CPPLib
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# C++ standard
target_compile_features(CPPLib PUBLIC cxx_std_17)
