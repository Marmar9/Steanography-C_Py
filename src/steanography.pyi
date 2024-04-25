"""
Module for encoding data inside images
"""
from __future__ import annotations
import typing
__all__ = ['ImageFileTypes', 'decode_from_image', 'encode_into_image']
class ImageFileTypes:
    """
    Members:
    
      WAW
    """
    WAW: typing.ClassVar[ImageFileTypes]  # value = <ImageFileTypes.WAW: 0>
    __members__: typing.ClassVar[dict[str, ImageFileTypes]]  # value = {'WAW': <ImageFileTypes.WAW: 0>}
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
def decode_from_image(arg0: bytes, arg1: ImageFileTypes) -> None:
    """
    A function that adds two numbers
    """
def encode_into_image(bytes: bytes, option: ImageFileTypes) -> None:
    """
    A function that adds two numbers
    """
