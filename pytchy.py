#!/usr/bin/env python


"""Main CLI."""
from argparse import ArgumentParser
from typing import Final, Dict
from core.symbols import HtmlSymbolProvider, SymbolMatrix, HtmlFilledSymbolProvider
from core.symbols import CharProvider, PSymbolProvider, SkinnySymbolProvider
from core.image import PngReader
from core.color import ColorMatrix
from in_out.html import (
    LegendCSS,
    LegendHtmlTable,
    HTML,
    MatrixTableCSS,
    MatrixHtmlTable,
)
from pathlib import Path


version: Final[str] = "1.0.0"


class Pytchy:
    def __init__(self) -> None:
        self._png_file: str = ""
        self._overwrite_existing_files: bool = False
        self._show_maximum_colors: bool = False
        self._mark_center_color: str = ""
        self._symbol_provider: PSymbolProvider = HtmlSymbolProvider()
        self._symbol_user_selection: str = ""

    def prepare(self) -> None:
        if self._symbol_user_selection == "default":
            self._symbol_provider = HtmlSymbolProvider()
        elif self._symbol_user_selection == "letters":
            self._symbol_provider = CharProvider()
        elif self._symbol_user_selection == "filled":
            self._symbol_provider = HtmlFilledSymbolProvider()
        elif self._symbol_user_selection == "skinny":
            self._symbol_provider = SkinnySymbolProvider()
        else:
            raise ValueError(f'Invalid symbol-set "{args.symbols}"')

    def _execute_show_maximum_colors(self) -> None:
        print(
            f"Maximum permitted number of colors is {self._symbol_provider.max_number}."
        )

    def _execute_generate_pattern_from_png(self) -> None:
        png_path: Path = Path(self._png_file)
        if not png_path.exists():
            raise FileNotFoundError(self._png_file)
        png_parent_folder: Path = png_path.parent

        html_files: Dict[str, Path] = {
            "color": png_parent_folder / (png_path.stem + "_color_pattern.html"),
            "stitch": png_parent_folder / (png_path.stem + "_stitch_pattern.html"),
            "legend": png_parent_folder / (png_path.stem + "_legend.html"),
        }
        if not self._overwrite_existing_files:
            for _, path in html_files.items():
                if path.exists():
                    raise FileExistsError(str(path))

        png_reader: PngReader = PngReader()
        png_reader.file_name = self._png_file
        color_matrix: ColorMatrix = png_reader.read()
        symbol_matrix: SymbolMatrix = SymbolMatrix(color_matrix, self._symbol_provider)

        symbol_matrix_html: MatrixHtmlTable = MatrixHtmlTable(
            color_matrix, symbol_matrix
        )
        symbol_matrix_html.show_background_color = False
        if self._mark_center_color != "":
            if self._mark_center_color.lower() == "none":
                symbol_matrix_html.mark_center_cell = False
            else:
                symbol_matrix_html.mark_center_cell = True
                symbol_matrix_html.mark_center_cell_color = self._mark_center_color

        color_matrix_html: MatrixHtmlTable = MatrixHtmlTable(color_matrix)

        matrix_css: MatrixTableCSS = MatrixTableCSS()

        legend_html: LegendHtmlTable = LegendHtmlTable(symbol_matrix.legend)
        legend_css: LegendCSS = LegendCSS()

        with open(str(html_files["color"]), "w") as html_file:
            print(f'Writing color pattern: "{str(html_files["color"])}"')
            html_file.write(
                HTML(
                    color_matrix_html.make_html(), matrix_css.make_html_style_tag()
                ).make_html()
            )
        with open(str(html_files["stitch"]), "w") as html_file:
            print(f'Writing stitch pattern: "{str(html_files["stitch"])}"')
            html_file.write(
                HTML(
                    symbol_matrix_html.make_html(), matrix_css.make_html_style_tag()
                ).make_html()
            )
        with open(str(html_files["legend"]), "w") as html_file:
            print(f'Writing legend: "{str(html_files["legend"])}"')
            html_file.write(
                HTML(
                    legend_html.make_html(), legend_css.make_html_style_tag()
                ).make_html()
            )

    def execute(self) -> None:
        if self._show_maximum_colors:
            self._execute_show_maximum_colors()

        elif self._png_file:
            self._execute_generate_pattern_from_png()


def _print_error_header():
    print()
    print("!An error occurred!")


if __name__ == "__main__":

    pytchy: Pytchy = Pytchy()

    parser: ArgumentParser = ArgumentParser(
        prog="Pytchy",
        description=(
            "Create cross-stitch patterns from PNG files. \n\n"
            "2020 -- licensed under GNU Public License"
        ),
        epilog=(
            "The tool reads a PNG file to generate a cross stitch pattern "
            "consisting of symbols and a symbol-to-color legend. "
            "Output files are written to HTML for viewing in web browsers."
        ),
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {version}"
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        required=False,
        dest="overwrite_existing_files",
        help="Overwrite existing files instead of raising an error.",
    )
    parser.add_argument(
        "-c",
        "--color-center",
        action="store",
        default="limegreen",
        type=str,
        required=False,
        metavar="<named-html-color>",
        dest="mark_center_color",
        help=(
            "Set the color to mark the center of the stitch pattern. Use 'none' to"
            " disable marking. Visit https://en.wikipedia.org/wiki/Web_colors for"
            " supported color names."
        ),
    )
    parser.add_argument(
        "-s",
        "--symbols",
        action="store",
        default="default",
        choices=["default", "letters", "filled", "skinny"],
        type=str,
        required=False,
        metavar="<symbol-set>",
        dest="symbols",
        help=(
            "Set the symbols to be used in the stitch pattern to represent colors."
            " Options are: default - filled and outlined symbols, letters - captital"
            " letters, filled - filled symbols, skinny - skinny symbols"
        ),
    )
    parser.add_argument(
        "-p",
        "--png",
        type=str,
        action="store",
        default="",
        metavar="<png_file>",
        required=False,
        dest="png_file",
        help=(
            "Path to PNG file to create cross-stitch pattern from. "
            "Three HTML files will be created in the folder of the PNG: "
            "color-matrix, symbol-matrix and symbol-to-color legend"
        ),
    )
    parser.add_argument(
        "-m",
        "--max-color",
        action="store_true",
        dest="show_max_colors",
        help="Show the maximum permitted number of colors in PNG input files.",
    )
    args = parser.parse_args()

    if "png_file" in args:
        pytchy._png_file = args.png_file
    if "overwrite_existing_files" in args:
        pytchy._overwrite_existing_files = args.overwrite_existing_files
    if "show_max_colors" in args:
        pytchy._show_maximum_colors = args.show_max_colors
    if "mark_center_color" in args:
        pytchy._mark_center_color = args.mark_center_color
    if "symbols" in args:
        pytchy._symbol_user_selection = args.symbols

    try:
        pytchy.prepare()
        pytchy.execute()

    except FileNotFoundError as err:
        _print_error_header()
        print("Following file does not exist")
        print(err)

    except FileExistsError as err:
        _print_error_header()
        print(f'Existing file: "{err}"')
        print("Use [-o, --overwrite] to overwrite existing files.")

    except ValueError as err:
        _print_error_header()
        print(err)

    else:
        print("Done!")
