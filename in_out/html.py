"""Classes for writing of data to HTML."""
from typing import Final, List, Tuple, Optional, Dict, Protocol
from core.image import ColorMatrix, Color
from core.symbols import SymbolMatrix
from copy import deepcopy


class PHtml(Protocol):
    def make_html(self) -> str:
        ...


class PCss(Protocol):
    def make_html_style_tag(self) -> str:
        ...


class HTML:
    def __init__(self, body_html: str, header_html: str = "") -> None:
        if len(body_html) == 0:
            raise ValueError("empty inner HTML")
        if header_html is None:
            raise ValueError("None is invalid for header html")

        self._inner_html: str = body_html
        self._header_html: str = header_html

    def make_html(self) -> str:
        html_content: List[str] = ["<!DOCTYPE html>", "<html>"]
        if self._header_html != "":
            html_content += ["<head>", self._header_html, "</head>"]

        html_content += ["<body>", self._inner_html, "</body>", "</html>"]
        return "\n".join(html_content)


class MatrixTableCSS:
    def __init__(self) -> None:
        self._pixel_size: Tuple[int, int] = (12, 12)
        self._show_grid: bool = True

    @property
    def pixel_size(self) -> Tuple[int, int]:
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, size: Tuple[int, int]) -> None:
        if len(size) != 2:
            raise ValueError(
                f"Invalid length of tuple size {len(size)}, required (width, height)"
            )
        self._pixel_size = size

    @property
    def show_grid(self) -> bool:
        return self._show_grid

    @show_grid.setter
    def show_grid(self, flag: bool) -> None:
        self._show_grid = flag

    def make_html_style_tag(self) -> str:
        html_content = ["<style>"]
        html_content += [
            "table {",
            "border-collapse: collapse;",
            "border-spacing: 0px;empty-cells: show;",
            "}",
            "table tr {",
            f"height: {self._pixel_size[1]}px;",
            "}",
            "table tr td {",
            f"width: {self._pixel_size[0]}px;",
            f"height: {self._pixel_size[1]}px;",
            "text-align: center;",
            "vertical-align: middle;",
            "padding: 0px;",
            "margin: 0px;",
            f"font-size: {min(self._pixel_size)}px;",
            "font-weight: bold;",
        ]
        if self._show_grid:
            html_content += [
                "border-style: solid; border-color: rgb(190,190,190); border-width:"
                " 1px;"
            ]
        html_content += [
            "}",
            "table tr td div {",
            "overflow: hidden;",
            f"line-height: {self._pixel_size[1]}px;",
            f"width: {self._pixel_size[0]}px;",
            f"height: {self._pixel_size[1]}px;",
            f"font-size: {min(self._pixel_size) - 1}px;",
            "margin: 0px;",
            "padding: 0px;",
            "font-weight: bold;",
            "}",
        ]
        html_content += ["</style>"]

        return "\n".join(html_content)


class MatrixHtmlTable:
    def __init__(
        self, color_matrix: ColorMatrix, symbol_matrix: Optional[SymbolMatrix] = None
    ):

        if color_matrix.is_empty:
            raise ValueError("Empty color matrix")
        if symbol_matrix is not None:
            if symbol_matrix.width != color_matrix.width:
                raise ValueError(
                    "Differing width for symbol and color matrix: "
                    f"{symbol_matrix.width} != {color_matrix.width}"
                )
            if symbol_matrix.height != color_matrix.height:
                raise ValueError(
                    "Differing height for symbol and color matrix: "
                    f"{symbol_matrix.height} != {color_matrix.height}"
                )

        self._color_matrix: ColorMatrix = deepcopy(color_matrix)
        self._symbol_matrix: Optional[SymbolMatrix] = (
            deepcopy(symbol_matrix) if symbol_matrix is not None else None
        )
        self._show_background_color: bool = True
        self._mark_center_cell: bool = True
        self._mark_center_cell_color: str = "limegreen"

    @staticmethod
    def _center_indexes(element_count: int) -> Tuple[int, int]:
        """Get (from, to) indexes (0-based)."""
        if element_count % 2 == 0:
            return (int(element_count / 2 - 1), int(element_count / 2))
        else:
            return (int(element_count / 2) - 1, int(element_count / 2) - 1)

    @property
    def show_background_color(self) -> bool:
        return self._show_background_color

    @show_background_color.setter
    def show_background_color(self, flag: bool) -> None:
        if self._symbol_matrix is None and not flag:
            raise ValueError("Undefined symbol matrix, cannot disable background color")
        self._show_background_color = flag

    @property
    def mark_center_cell(self) -> bool:
        return self._mark_center_cell

    @mark_center_cell.setter
    def mark_center_cell(self, flag: bool) -> None:
        self._mark_center_cell = flag

    @property
    def mark_center_cell_color(self) -> str:
        return self._mark_center_cell_color

    @mark_center_cell_color.setter
    def mark_center_cell_color(self, color: str) -> None:
        if len(color) == 0:
            raise ValueError("Empty color name")
        self._mark_center_cell_color = color

    @property
    def color_matrix(self) -> ColorMatrix:
        return self._color_matrix

    def make_html(self) -> str:

        center_cell_indexes_from_to: List[Tuple[int, int]] = [
            MatrixHtmlTable._center_indexes(self._color_matrix.width),
            MatrixHtmlTable._center_indexes(self._color_matrix.height),
        ]

        html_tags: List[str] = ["<table>", "<tbody>"]
        for row_idx, row in enumerate(self._color_matrix.matrix):
            html_tags += ["<tr>"]
            for col_idx, color in enumerate(row):
                if self._show_background_color:
                    html_tags += [
                        f'<td style="background-color: rgba({color.red}, {color.green},'
                        f' {color.blue}, {color.alpha});" ',
                        f">",
                    ]
                else:
                    html_tags += ["<td>"]

                if self._symbol_matrix is not None and not color.is_transparent:

                    open_div: str = "<div>"
                    if self._mark_center_cell and self._symbol_matrix is not None:
                        if (
                            col_idx in center_cell_indexes_from_to[0]
                            and row_idx in center_cell_indexes_from_to[1]
                        ):
                            open_div = (
                                '<div style="background-color:'
                                f' {self._mark_center_cell_color};">'
                            )

                    html_tags += [
                        open_div,
                        f"{self._symbol_matrix.matrix[row_idx][col_idx]}",
                        "</div>",
                    ]
                html_tags += ["</td>"]
            html_tags += ["</tr>"]

        html_tags += ["</tbody>", "</table>"]

        return "\n".join(html_tags)


class LegendHtmlTable:
    def __init__(self, legend: Dict[str, Color], ignore_transparent: bool = True):
        if len(legend) == 0:
            raise ValueError("Empty legend dictionary")

        self._legend = deepcopy(legend)
        self._legend_bar_width: int = 80
        self._legend_bar_height: int = 30
        self._ignore_transparent: bool = ignore_transparent

    def make_html(self) -> str:

        html_content: List[str] = [
            "<table>",
            "<tbody>",
        ]

        for k, c in self._legend.items():
            if self._ignore_transparent and c.is_transparent:
                continue
            html_content += ["<tr>"]
            html_content += [
                "<td>",
                k,
                "</td>",
                "<td>",
                f'<div style="width: {self._legend_bar_width}px; height:'
                f" {self._legend_bar_height}px; background-color: rgba({c.red},"
                f' {c.green}, {c.blue}, {c.alpha})">',
                "</div>",
                "</td>",
            ]
            html_content += ["</tr>"]

        html_content += ["</tbody>", "</table>"]

        return "\n".join(html_content)


class LegendCSS:
    def __init__(self) -> None:

        html: List[str] = ["<style>"]
        html += [
            "table {border-collapse: collapse;}",
            "table tr td {border-style: solid; border-color: black; border-width: 1px;"
            " padding: 2px;}",
        ]
        html += ["</style>"]

        self._html_style_tag: str = "\n".join(html)

    def make_html_style_tag(self) -> str:
        return self._html_style_tag
