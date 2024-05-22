from steanography import encode_into_image, ImageFileTypes, decode_from_audio, encode_into_audio, decode_from_image
import sys


with open("src/example.png", "rb") as f:
  response = encode_into_image(f.read(),"""
        test
  """.encode()  , ImageFileTypes.PNG)

with open("output.png", "wb") as f:
        f.write(response)

with open("output.png", "rb") as f:
    decoded = decode_from_image(f.read(), ImageFileTypes.PNG);
    print(decoded.decode())
