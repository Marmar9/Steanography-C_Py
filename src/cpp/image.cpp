#include "image.hpp"

#include <stdio.h>
#include <string>

void decode_from_image(pybind11::bytes bytes, ImageFileTypes option) {

    // Conversion to c natives
    std::string cpp_form = bytes.cast<std::string>();
    const char * valid_binary = cpp_form.c_str();
    // Main code begins 
    switch (option) {
        case WAW:
        printf("%s\n", valid_binary);
            break;
    }
    
}

void encode_into_image(pybind11::bytes bytes, ImageFileTypes option) {

    // Conversion to c natives
    std::string cpp_form = bytes.cast<std::string>();
    const char * valid_binary = cpp_form.c_str();

    // Main code begins 
    switch (option) {
        case WAW:
        printf("%s\n", valid_binary);
            break;
    }
}
