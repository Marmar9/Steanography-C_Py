#ifndef AUDIO_H
#define AUDIO_H
#include <pybind11/pybind11.h>
namespace py = pybind11;
enum AudioFileTypes {
    WAW
};

py::bytes encode_into_audio(py::bytes bytes, std::string text, AudioFileTypes file_type);

py::bytes decode_from_audio(py::bytes bytes, AudioFileTypes file_type);

#endif // DEBUG
