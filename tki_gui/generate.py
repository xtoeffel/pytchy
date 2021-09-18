"""Generation of HTML files."""
from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable
from pathlib import Path
from tkinter import StringVar, BooleanVar, messagebox
from in_out.html import HTML, PHtml, PCss
from in_out.html import MatrixHtmlTable, MatrixTableCSS
from in_out.html import LegendHtmlTable, LegendCSS
from core.color import ColorMatrix
from core.symbols import PSymbolProvider, SymbolMatrix
from tki_gui.variables import Variable


@dataclass
class HtmlOutput:

    file_path: Optional[Path]
    html: Optional[PHtml]
    css: Optional[PCss]

    def __init__(self):
        self.file_path = None
        self.html = None
        self.css = None


# TODO: move to in_out/html? redundant shared with pytchy.py
@dataclass
class HtmlFileSet:

    stitch_pattern: HtmlOutput
    color_plot: HtmlOutput
    legend: HtmlOutput

    def __init__(self):
        self.stitch_pattern = HtmlOutput()
        self.color_plot = HtmlOutput()
        self.legend = HtmlOutput()

    def files_exist(self) -> bool:
        assert self.stitch_pattern.file_path is not None
        assert self.color_plot.file_path is not None
        assert self.legend.file_path is not None
        return (
            self.stitch_pattern.file_path.exists()
            or self.color_plot.file_path.exists()
            or self.legend.file_path.exists()
        )


# TODO: move to HtmlFileSet.__init__()? & share with pytchy.py
def init_html_file_set(png_file_name: str) -> HtmlFileSet:
    if str is None:
        raise ValueError("Undefined PNG file name")

    path: Path = Path(png_file_name)
    parent: Path = path.parent

    hfs: HtmlFileSet = HtmlFileSet()
    hfs.stitch_pattern.file_path = parent / (path.stem + "_stitch_pattern.html")
    hfs.color_plot.file_path = parent / (path.stem + "_color_plot.html")
    hfs.legend.file_path = parent / (path.stem + "_legend.html")

    return hfs


class GeneratePatternFiles:
    def __init__(self) -> None:
        self._png_file_name: Optional[StringVar] = None
        self._color_matrix: Optional[Variable] = None
        self._symbol_provider: Optional[Variable] = None
        self._mark_center_color: Optional[StringVar] = None
        self._done_callback: Optional[Callable[[Any], None]] = None
        self._status_text: Optional[StringVar] = None

    def set_png_file_name(self, file_name: StringVar) -> None:
        self._png_file_name = file_name

    def set_color_matrix(self, color_matrix: Variable) -> None:
        self._color_matrix = color_matrix

    def set_symbol_provider(self, symbol_provider: Variable) -> None:
        self._symbol_provider = symbol_provider

    def set_mark_center_color(self, color: StringVar) -> None:
        self._mark_center_color = color

    def set_done_callback(self, callback: Callable[[Any], None]) -> None:
        self._done_callback = callback

    def set_status_text(self, text_var: StringVar) -> None:
        self._status_text = text_var

    @property
    def png_file_name(self) -> StringVar:
        assert self._png_file_name is not None, "undefined png_file_name"
        return self._png_file_name

    @property
    def color_matrix(self) -> ColorMatrix:
        assert self._color_matrix is not None, "undefined color_matrix"
        assert isinstance(self._color_matrix.value, ColorMatrix)
        return self._color_matrix.value

    @property
    def symbol_provider(self) -> PSymbolProvider:
        assert self._symbol_provider is not None, "undefined symbol_provider"
        assert isinstance(self._symbol_provider.value, PSymbolProvider)
        return self._symbol_provider.value

    @property
    def mark_center_color(self) -> StringVar:
        assert self._mark_center_color is not None, "undefined mark_center_color"
        return self._mark_center_color

    @property
    def status_text(self) -> StringVar:
        assert self._status_text is not None, "undefined status_text"
        return self._status_text

    def _write_html_file(self, html_output: HtmlOutput) -> None:
        assert html_output.html is not None
        assert html_output.css is not None

        with open(str(html_output.file_path), "w") as html_file:
            html_file.write(
                HTML(
                    html_output.html.make_html(), html_output.css.make_html_style_tag()
                ).make_html()
            )

    def generate(self, *args: Any) -> None:

        try:
            output_html_files: HtmlFileSet = init_html_file_set(
                self.png_file_name.get()
            )

            output_html_files.color_plot.html = MatrixHtmlTable(self.color_matrix)
            output_html_files.color_plot.css = MatrixTableCSS()

            symbol_matrix: SymbolMatrix = SymbolMatrix(
                self.color_matrix, self.symbol_provider
            )
            symbol_matrix_html: MatrixHtmlTable = MatrixHtmlTable(
                self.color_matrix, symbol_matrix
            )
            symbol_matrix_html.show_background_color = False
            symbol_matrix_html.mark_center_cell = True
            symbol_matrix_html.mark_center_cell_color = self.mark_center_color.get()
            output_html_files.stitch_pattern.html = symbol_matrix_html
            output_html_files.stitch_pattern.css = MatrixTableCSS()

            output_html_files.legend.html = LegendHtmlTable(symbol_matrix.legend)
            output_html_files.legend.css = LegendCSS()

            self._write_html_file(output_html_files.color_plot)
            self._write_html_file(output_html_files.stitch_pattern)
            self._write_html_file(output_html_files.legend)

            if self._done_callback is not None:
                self._done_callback()  # type: ignore

            self.status_text.set("Successfully wrote HTML files.")

        except Exception as ex:
            self.status_text.set("Error occurred!")
            messagebox.showerror(title="Error occurred", message=str(ex))
