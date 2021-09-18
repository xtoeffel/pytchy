"""Generate symbols for a specific color."""
from typing import Tuple, List, Set, Protocol, Dict, runtime_checkable
from copy import deepcopy
from core.color import Color, ColorMatrix


@runtime_checkable
class PSymbolProvider(Protocol):
    @property
    def max_number(self) -> int:
        ...

    def get(self) -> str:
        ...


class CharProvider:
    def __init__(self) -> None:
        self._dec_symbol_codes: List[int] = [
            65,
            97,
            66,
            98,
            67,
            99,
            68,
            100,
            69,
            101,
            70,
            102,
            71,
            103,
            72,
            104,
            73,
            105,
            74,
            106,
            75,
            107,
            76,
            108,
            77,
            109,
            78,
            110,
            79,
            111,
            80,
            112,
            81,
            113,
            82,
            114,
            83,
            115,
            84,
            116,
            85,
            117,
            86,
            118,
            87,
            119,
            88,
            120,
            89,
            121,
            90,
            122,
        ]
        self._position: int = 0

    @property
    def max_number(self) -> int:
        return len(self._dec_symbol_codes)

    def get(self) -> str:
        if self._position == len(self._dec_symbol_codes):
            raise ValueError(
                f"Depleted html symbol provider, provided {self._position - 1} symbols"
            )

        html: str = f"&#{self._dec_symbol_codes[self._position]};"
        self._position += 1
        return html


class HtmlSymbolProvider:
    def __init__(self) -> None:
        self._dec_symbol_codes: List[int] = [
            9632,
            9633,
            9644,
            9645,
            9646,
            9647,
            9650,
            9651,
            9654,
            9655,
            9660,
            9664,
            9665,
            9670,
            9671,
            9674,
            9675,
            9677,
            9678,
            9679,
            9680,
            9681,
            9682,
            9683,
            9684,
            9685,
            9686,
            9687,
            9688,
            9696,
            9697,
            9698,
            9699,
            9700,
            9701,
            9703,
            9704,
            9705,
            9706,
            9707,
            9708,
            9709,
            9710,
            9716,
            9717,
            9718,
            9719,
            9720,
            9721,
            9722,
            9733,
            9752,
            9773,
            9824,
            9827,
            9829,
            9830,
            9874,
            9487,
            9491,
            9495,
            9499,
            9523,
            9531,
        ]
        self._position: int = 0

    @property
    def max_number(self) -> int:
        return len(self._dec_symbol_codes)

    def get(self) -> str:
        if self._position == len(self._dec_symbol_codes):
            raise ValueError(
                f"Depleted html symbol provider, provided {self._position - 1} symbols"
            )

        html: str = f"&#{self._dec_symbol_codes[self._position]};"
        self._position += 1
        return html


class HtmlFilledSymbolProvider:
    def __init__(self) -> None:
        self._dec_symbol_codes: List[int] = [
            9632,
            9650,
            9654,
            9679,
            9680,
            9681,
            9682,
            9683,
            9698,
            9699,
            9700,
            9701,
            9703,
            9704,
            9705,
            9706,
            9752,
            9773,
            9775,
            9818,
            9822,
            9824,
            9874,
            10085,
            9602,
            9616,
            9625,
            9627,
            9630,
            9631,
        ]
        self._position: int = 0

    @property
    def max_number(self) -> int:
        return len(self._dec_symbol_codes)

    def get(self) -> str:
        if self._position == len(self._dec_symbol_codes):
            raise ValueError(
                f"Depleted html symbol provider, provided {self._position - 1} symbols"
            )

        html: str = f"&#{self._dec_symbol_codes[self._position]};"
        self._position += 1
        return html


class SkinnySymbolProvider:
    def __init__(self) -> None:
        self._dec_symbol_codes: List[int] = [
            8722,
            8725,
            8726,
            8729,
            8739,
            8743,
            8746,
            8847,
            8866,
            8867,
            8880,
            8894,
            8895,
            8904,
            8907,
            8920,
            64,
            94,
            166,
            215,
            43,
            92,
            95,
            96,
            886,
            937,
            992,
            1046,
            1192,
            1300,
            8229,
            8267,
            8362,
            8498,
            8597,
            8635,
        ]
        self._position: int = 0

    @property
    def max_number(self) -> int:
        return len(self._dec_symbol_codes)

    def get(self) -> str:
        if self._position == len(self._dec_symbol_codes):
            raise ValueError(
                f"Depleted html symbol provider, provided {self._position - 1} symbols"
            )

        html: str = f"&#{self._dec_symbol_codes[self._position]};"
        self._position += 1
        return html


class SymbolMatrix:
    def __init__(
        self, color_matrix: ColorMatrix, symbol_provider: PSymbolProvider
    ) -> None:

        if color_matrix.is_empty:
            raise ValueError("Empty list of pixels")
        if color_matrix.color_count > symbol_provider.max_number:
            raise ValueError(
                f"Invalid number of colors {color_matrix.color_count}, "
                "allowed max is {symbol_provider.max_number}"
            )

        self._color_matrix: ColorMatrix = color_matrix

        # dict does not work, because of hash => use tuple(color, symbol)
        color_to_symbol: List[Tuple[Color, str]] = [
            (col, symbol_provider.get()) for col in self._color_matrix.distinct_colors
        ]
        self._matrix: List[List[str]] = [
            [
                [cts for cts in color_to_symbol if cts[0].is_equal(col)][0][1]
                for col in pixel_row
            ]
            for pixel_row in self._color_matrix.matrix
        ]
        self._legend: Dict[str, Color] = {cts[1]: cts[0] for cts in color_to_symbol}

    @property
    def color_matrix(self) -> ColorMatrix:
        return self._color_matrix

    @property
    def width(self) -> int:
        return len(self._matrix[0])

    @property
    def height(self) -> int:
        return len(self._matrix)

    @property
    def matrix(self) -> List[List[str]]:
        return self._matrix

    @property
    def legend(self) -> Dict[str, Color]:
        return self._legend
