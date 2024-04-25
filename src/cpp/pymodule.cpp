#include "pybind11/pytypes.h"
#include <pybind11/pybind11.h>
#include <string>
#include <stdio.h>

enum ImageFileTypes {
    WAW,
};

namespace py = pybind11;

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

PYBIND11_MODULE(steanography, m) {
    pybind11::enum_<ImageFileTypes>(m, "ImageFileTypes")
        .value("WAW", ImageFileTypes::WAW);

    m.doc() = "Module for encoding data inside images"; 
    
    m.def("encode_into_image", &encode_into_image, "A function that adds two numbers", py::arg("bytes"), py::arg("option"));
    m.def("decode_from_image", &decode_from_image, "A function that adds two numbers");
}
