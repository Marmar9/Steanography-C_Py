#include "image.hpp"

#include <stdio.h>
#include <string>

namespace py = pybind11;

py::bytes encode_into_image(py::bytes image, std::string text,  ImageFileTypes file_type) {

    // Probably unsafe 
    // const char * valid_binary = (new std::string(image.cast<std::string>()))->c_str();
    
   //  Main code begins 
     switch (file_type) {
         case PNG:
             // Conversion to c natives
             std::string cpp_string = image.cast<std::string>();

             const char * png_image = cpp_string.c_str();
             const char * text_pointer = text.c_str(); 

             printf("%s\n", png_image);
             printf("%s\n", text_pointer);

             break;
     }

   return image;
}

py::bytes decode_from_image(py::bytes image, ImageFileTypes file_type) {

    switch (file_type) {
        case PNG:
            std::string cpp_string= image.cast<std::string>();
            const char * png_image = cpp_string.c_str();

        printf("%s\n", png_image);
            break;
    }

    std::string abc = std::string("asdasd");

    return py::bytes(abc); 
}
