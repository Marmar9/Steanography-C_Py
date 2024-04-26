"""
Module from steanography
"""
from __future__ import annotations
import typing
__all__ = ['AudioFileTypes', 'ImageFileTypes', 'decode_from_audio', 'decode_from_image', 'encode_into_audio', 'encode_into_image']
class AudioFileTypes:
    """
    Members:
    
      WAW
    """
    WAW: typing.ClassVar[AudioFileTypes]  # value = <AudioFileTypes.WAW: 0>
    __members__: typing.ClassVar[dict[str, AudioFileTypes]]  # value = {'WAW': <AudioFileTypes.WAW: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ImageFileTypes:
    """
    Members:
    
      PNG
    """
    PNG: typing.ClassVar[ImageFileTypes]  # value = <ImageFileTypes.PNG: 0>
    __members__: typing.ClassVar[dict[str, ImageFileTypes]]  # value = {'PNG': <ImageFileTypes.PNG: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def decode_from_audio(audio: bytes, file_type: AudioFileTypes) -> bytes:
    """
    Decode text from audio
    """
def decode_from_image(image: bytes, file_type: ImageFileTypes) -> bytes:
    """
    Decode text from image
    """
def encode_into_audio(audio: bytes, text: str, file_type: AudioFileTypes) -> bytes:
    """
    Encode text into audio
    """
def encode_into_image(image: bytes, text: str, file_type: ImageFileTypes) -> bytes:
    """
    Encode text into image
    """
