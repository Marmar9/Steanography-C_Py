#include "pybind11/pytypes.h"
#include <pybind11/pybind11.h>

#include "image.hpp"

namespace py = pybind11;

PYBIND11_MODULE(steanography, m) {
    pybind11::enum_<ImageFileTypes>(m, "ImageFileTypes")
        .value("WAW", ImageFileTypes::WAW);

    m.doc() = "Module for encoding data inside images"; 
    
    m.def("encode_into_image", &encode_into_image, "A function that adds two numbers", py::arg("bytes"), py::arg("option"));
    m.def("decode_from_image", &decode_from_image, "A function that adds two numbers");
}
