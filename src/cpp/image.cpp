#include "image.hpp"
#include <cstdio>
#include <pybind11/functional.h>

#include <cstddef>
#include <string>

#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstdbool>
#include <cstring>
#include <cerrno>

namespace py = pybind11;

#define PNG_SIG_CAP 8
const uint8_t png_sig[PNG_SIG_CAP] = {137, 80, 78, 71, 13, 10, 26, 10};

#define read_bytes_or_panic(file, buf, buf_cap) read_bytes_or_panic_(file, buf, buf_cap, __FILE__, __LINE__)
void read_bytes_or_panic_(FILE *file, void *buf, size_t buf_cap, const char *source_file, int source_line)
{
    size_t n = fread(buf, buf_cap, 1, file);
    if (n != 1) {
        if (ferror(file)) {
            fprintf(stderr, "%s:%d: ERROR: could not read %zu bytes from file: %s\n",
                    source_file, source_line,
                    buf_cap, strerror(errno));
            exit(1);
        } else if (feof(file)) {
            fprintf(stderr, "%s:%d: ERROR: could not read %zu bytes from file: reached the end of file\n",
                    source_file, source_line,
                    buf_cap);
            exit(1);
        } else {
            assert(0 && "unreachable");
        }
    }
}

#define write_bytes_or_panic(file, buf, buf_cap) write_bytes_or_panic_(file, buf, buf_cap, __FILE__, __LINE__)
void write_bytes_or_panic_(FILE *file, void *buf, size_t buf_cap, const char *source_file, int source_line)
{
    size_t n = fwrite(buf, buf_cap, 1, file);
    if (n != 1) {
        if (ferror(file)) {
            fprintf(stderr, "%s:%d: ERROR: could not write %zu bytes to file: %s\n",
                    source_file, source_line,
                    buf_cap, strerror(errno));
            exit(1);
        } else {
            assert(0 && "unreachable");
        }
    }

}

void reverse_bytes(void *buf0, size_t buf_cap)
{
    uint8_t *buf = (uint8_t *)buf0;
    for (size_t i = 0; i < buf_cap/2; ++i) {
        uint8_t t = buf[i];
        buf[i] = buf[buf_cap - i - 1];
        buf[buf_cap - i - 1] = t;
    }
}


#define CHUNK_BUF_CAP (32 * 1024)
uint8_t chunk_buf[CHUNK_BUF_CAP];

py::bytes encode_into_image(py::bytes image, py::bytes payload,  ImageFileTypes file_type) {
    // Probably unsafe 
    // const char * valid_binary = (new std::string(image.cast<std::string>()))->c_str();
    std::string temp_input_file = image.cast<std::string>();
    const char * input_file_data = temp_input_file.c_str();
     

    std::string payload_temp = payload.cast<std::string>();
    const char * data_to_inject = payload_temp.c_str();

   //  Main code begins 
     switch (file_type) {
         case PNG:

                FILE *input_file = tmpfile();
                if (input_file == NULL) {
                    fprintf(stderr, "ERROR: could not create temporary file: %s\n", strerror(errno));
                    exit(1);
                }
                write_bytes_or_panic(input_file, (char *)input_file_data, temp_input_file.length());
                  // Seek to the beginning of the file
                fseek(input_file, 0, SEEK_SET);

                FILE *output_file= tmpfile();
                if (output_file == NULL) {
                    fprintf(stderr, "ERROR: could not create temporary file: %s\n",
                             strerror(errno));
                    exit(1);
                }

                uint8_t sig[PNG_SIG_CAP];
                read_bytes_or_panic(input_file, sig, PNG_SIG_CAP);
                write_bytes_or_panic(output_file, sig, PNG_SIG_CAP);

                if (memcmp(sig, png_sig, PNG_SIG_CAP) != 0) {
                    fprintf(stderr, "ERROR: Provided file does not appear to be a valid PNG image\n");
                    exit(1);
                }

                bool quit = false;
                while (!quit) {
                    uint32_t chunk_sz;
                    read_bytes_or_panic(input_file, &chunk_sz, sizeof(chunk_sz));
                    write_bytes_or_panic(output_file, &chunk_sz, sizeof(chunk_sz));
                    reverse_bytes(&chunk_sz, sizeof(chunk_sz));

                    uint8_t chunk_type[4];
                    read_bytes_or_panic(input_file, chunk_type, sizeof(chunk_type));
                    write_bytes_or_panic(output_file, chunk_type, sizeof(chunk_type));

                    if (*(uint32_t*)chunk_type == 0x444E4549) {
                        quit = true;
                    }

                    size_t n = chunk_sz;
                    while (n > 0) {
                        size_t m = n;
                        if (m > CHUNK_BUF_CAP) {
                            m = CHUNK_BUF_CAP;
                        }
                        read_bytes_or_panic(input_file, chunk_buf, m);
                        write_bytes_or_panic(output_file, chunk_buf, m);
                        n -= m;
                    }

                    uint32_t chunk_crc;
                    read_bytes_or_panic(input_file, &chunk_crc, sizeof(chunk_crc));
                    write_bytes_or_panic(output_file, &chunk_crc, sizeof(chunk_crc));

                    if (*(uint32_t*)chunk_type == 0x52444849) {
                        uint32_t injected_sz = payload_temp.length();
                        reverse_bytes(&injected_sz, sizeof(injected_sz));
                        write_bytes_or_panic(output_file, &injected_sz, sizeof(injected_sz));
                        reverse_bytes(&injected_sz, sizeof(injected_sz));

                        char *injected_type = (char *)"cuST";
                        write_bytes_or_panic(output_file, injected_type, 4);

                        write_bytes_or_panic(output_file, (char *)data_to_inject, injected_sz);

                        uint32_t injected_crc = 0; 
                        write_bytes_or_panic(output_file, &injected_crc, sizeof(injected_crc));
                    }
                }
                // Ucina kilkanaście bytów
                uint64_t output_size = ftell(output_file);
                
                fseek(output_file, 0, SEEK_END);

                // char * response = (char *)malloc(temp_input_file.size() + payload_temp.size());
                char * response = (char *)malloc(output_size);
                
                fseek(output_file, 0, SEEK_SET);

                // read_bytes_or_panic(output_file, response, temp_input_file.size() + payload_temp.size());
                read_bytes_or_panic(output_file, response, output_size);

                fseek(output_file, 0, SEEK_END);

                // Z jakiegoś nieznanego mi powodu są różne 
                printf("True file size: %lu, Computed file size: %lu\n", output_size, temp_input_file.size() + payload_temp.size());

                fclose(input_file);
                fclose(output_file);

               //  return py::bytes(response, temp_input_file.size() + payload_temp.size());
                return py::bytes(response,output_size);
     }
     return "";
}

py::bytes decode_from_image(py::bytes image, ImageFileTypes file_type) {
    // Probably unsafe 
    // const char * valid_binary = (new std::string(image.cast<std::string>()))->c_str();
    std::string temp_input_file = image.cast<std::string>();
    const char * input_file_data = temp_input_file.c_str();
     

   //  Main code begins 
     switch (file_type) {
         case PNG:
                FILE *input_file = tmpfile();
                if (input_file == NULL) {
                    fprintf(stderr, "ERROR: could not create temporary file: %s\n", strerror(errno));
                    exit(1);
                }
                write_bytes_or_panic(input_file, (char *)input_file_data, temp_input_file.length());
                  // Seek to the beginning of the file
                fseek(input_file, 0, SEEK_SET);


                uint8_t sig[PNG_SIG_CAP];
                read_bytes_or_panic(input_file, sig, PNG_SIG_CAP);

                if (memcmp(sig, png_sig, PNG_SIG_CAP) != 0) {
                    fprintf(stderr, "ERROR: Provided file does not appear to be a valid PNG image\n");
                    exit(1);
                }

                bool quit = false;
                while (!quit) {
                    uint32_t chunk_sz;
                    read_bytes_or_panic(input_file, &chunk_sz, sizeof(chunk_sz));
                    reverse_bytes(&chunk_sz, sizeof(chunk_sz));

                    uint8_t chunk_type[4];
                    read_bytes_or_panic(input_file, chunk_type, sizeof(chunk_type));

                    if (*(uint32_t*)chunk_type == 0x444E4549) {
                        quit = true;
                    }

                    if (*(uint32_t*)chunk_type == 0x54537563) {
                        char * chunk_data = (char *)malloc(chunk_sz);
                        read_bytes_or_panic(input_file, chunk_data, chunk_sz);

                        return py::bytes(chunk_data, chunk_sz);
                    } else {
                        // Skip chunk
                        fseek(input_file, chunk_sz, SEEK_CUR);
                    }
                    
                   
                    uint32_t chunk_crc;
                    read_bytes_or_panic(input_file, &chunk_crc, sizeof(chunk_crc));


                    
                }
     }
     return ""; 
}
