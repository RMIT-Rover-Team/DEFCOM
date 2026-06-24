cmake_minimum_required(VERSION 3.16)
project(MyNode LANGUAGES CXX)

# Add DEFCOM library from local folder
add_subdirectory(external/DEFCOM)

# Your executable
add_executable(PROJECT_NAME
    src/main.cpp
)

# Link against DEFCOM
target_link_libraries(PROJECT_NAME
    PRIVATE
        DEFCOM
)

# Include DEFCOM headers
target_include_directories(PROJECT_NAME
    PRIVATE
        external/DEFCOM/include
)

# C++ standard
target_compile_features(PROJECT_NAME PUBLIC cxx_std_17)
