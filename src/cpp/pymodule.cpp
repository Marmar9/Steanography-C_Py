#include "pybind11/pytypes.h"
#include <pybind11/pybind11.h>

#include "image.hpp"
#include "audio.h"

namespace py = pybind11;

PYBIND11_MODULE(steanography, m) {
    pybind11::enum_<ImageFileTypes>(m, "ImageFileTypes")
        .value("PNG", ImageFileTypes::PNG);

    pybind11::enum_<AudioFileTypes>(m, "AudioFileTypes")
        .value("WAW", AudioFileTypes::WAW);


    m.doc() = "Module from steanography";

    m.def("encode_into_audio", &encode_into_audio, "Encode text into audio", py::arg("audio"), py::arg("text"), py::arg("file_type"));
    m.def("decode_from_audio", &decode_from_audio, "Decode text from audio", py::arg("audio"), py::arg("file_type"));

    m.def("encode_into_image", &encode_into_image, "Encode text into image", py::arg("image"), py::arg("text"), py::arg("file_type"));
    m.def("decode_from_image", &decode_from_image, "Decode text from image", py::arg("image"), py::arg("file_type"));
}
