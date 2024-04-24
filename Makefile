# Define the compiler
CXX := g++

# Define compilation flags
CXXFLAGS := -Wall -Wextra -std=c++23 -shared -std=c++11 -fPIC  `python3 -m pybind11 --includes` # Change to desired C++ standard (e.g., c++11, c++14, c++17, c++20)

# Define the source files
SOURCES := $(wildcard src/c/*.cpp)


