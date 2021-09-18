"""Color and related classes."""

from typing import List, Set, Any
from copy import deepcopy


class Color:
    """RGBA color"""

    @staticmethod
    def _check_color_value(value: int, color: str = '') -> None:
        if value < 0: 
            raise ValueError(f'Invalid color [{color}] value: {value} < 0')
        if value > 255:
            raise ValueError(f'Invalid color [{color}] value: {value} > 255')

    @staticmethod
    def invert(color: 'Color') -> 'Color':
        return Color(
            255 - color.red,
            255 - color.green,
            255 - color.blue,
            color.alpha
        )

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0, alpha: int = 0) -> None:
        Color._check_color_value(red, 'red')
        Color._check_color_value(green, 'green')
        Color._check_color_value(blue, 'blue')
        Color._check_color_value(alpha, 'alpha')
        self._red: int = red
        self._green: int = green
        self._blue: int = blue
        self._alpha: int = alpha

    @property
    def red(self) -> int:
        return self._red

    @red.setter
    def red(self, value: int) -> None:
        Color._check_color_value(value)
        self._red = value

    @property
    def green(self) -> int:
        return self._green

    @green.setter
    def green(self, value: int) -> None:
        Color._check_color_value(value)
        self._green = value

    @property
    def blue(self) -> int:
        return self._blue

    @blue.setter
    def blue(self, value: int) -> None:
        Color._check_color_value(value)
        self._blue = value

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        Color._check_color_value(value)
        self._alpha = value

    @property
    def is_transparent(self) -> bool:
        return self._alpha == 0

    def is_equal(self, other: 'Color') -> bool:
        return self.red == other.red \
            and self.green == other.green \
            and self.blue == other.blue \
            and self.alpha == other.alpha


class ColorMatrix:

    def __init__(self, pixel_matrix: List[List[Color]]) -> None:
        if len(pixel_matrix) == 0:
            raise ValueError('Empty pixel matrix')
        width: int = len(pixel_matrix[0])
        if any(width != len(row) for row in pixel_matrix[1:]):
            raise ValueError(f'Unequal number of pixels in rows detected: '
                              'expected all rows to have {width} pixels')

        self._colors: List[Color] = []
        # don't use set() as this comes with issues
        for pixel_row in pixel_matrix:
            for color in pixel_row:
                if not any(c.is_equal(color) for c in self._colors):
                    self._colors.append(color)
        list(set(deepcopy(col) for pixel_row in pixel_matrix for col in pixel_row))
        self._matrix: List[List[Color]] = deepcopy(pixel_matrix)

    @property
    def color_count(self) -> int:
        return len(self._colors)

    @property
    def distinct_colors(self) -> List[Color]:
        return deepcopy(self._colors)

    @property
    def matrix(self) -> List[List[Color]]:
        return deepcopy(self._matrix)

    @property
    def width(self) -> int:
        return len(self._matrix[0])

    @property
    def height(self) -> int:
        return len(self._matrix)

    @property
    def is_empty(self) -> bool:
        return len(self._matrix) == 0
