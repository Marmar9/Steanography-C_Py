#ifndef IMAGE_H
#define IMAGE_H

#include <pybind11/pybind11.h>

namespace py = pybind11;

enum ImageFileTypes {
    PNG,
};

py::bytes encode_into_image(py::bytes image, std::string text, ImageFileTypes file_type);

py::bytes decode_from_image(py::bytes image, ImageFileTypes file_type);


#endif
