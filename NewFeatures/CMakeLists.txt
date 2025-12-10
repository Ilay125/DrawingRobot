cmake_minimum_required(VERSION 3.10)

# Project name and language
project(qtest LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Automatically gather all .cpp files in the current directory
file(GLOB SOURCES "*.cpp")

# Create executable
add_executable(qtest ${SOURCES})
