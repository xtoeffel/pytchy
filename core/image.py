"""Classes for reading of images and providing process objects."""
from typing import Final, List
from core.color import Color, ColorMatrix
from PIL import Image  # type: ignore
from pathlib import Path


class FileExtensionError(OSError):
    def __init__(self, msg: str, found_ext: str, expected_ext: str):
        super().__init__(msg)
        self.found_ext: Final[str] = found_ext
        self.expected_ext: Final[str] = expected_ext


class PngReader:
    def __init__(self):
        self._file_name: str = ""
        self.width_max: Final[int] = 500
        self.height_max: Final[int] = 500

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, name: str) -> None:
        if len(name) == 0:
            raise ValueError("Empty file name")
        self._file_name = name

    def read(self) -> ColorMatrix:
        path: Path = Path(self._file_name)
        if not path.exists():
            raise FileNotFoundError(self._file_name)
        if path.suffix.lower() != ".png":
            raise FileExtensionError(self.file_name, path.suffix, "[.png, .PNG]")

        img = Image.open(self.file_name).convert("RGBA")
        width, height = img.size
        if width > self.width_max:
            raise ValueError(
                f"Image is too wide: current {width}, maximum {self.width_max}"
            )
        if height > self.height_max:
            raise ValueError(
                f"Image is too high: current {height}, maximum {self.height_max}"
            )

        pixels = img.load()
        pixel_matrix: List[List[Color]] = [
            [Color(*pixels[x, y]) for x in range(0, width)] for y in range(0, height)
        ]
        return ColorMatrix(pixel_matrix)
