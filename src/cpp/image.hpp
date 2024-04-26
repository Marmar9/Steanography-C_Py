#ifndef IMAGE_H
#define IMAGE_H

#include <pybind11/pybind11.h>

enum ImageFileTypes {
    WAW,
};

void decode_from_image(pybind11::bytes bytes, ImageFileTypes option);

void encode_into_image(pybind11::bytes bytes, ImageFileTypes option);

#endif
