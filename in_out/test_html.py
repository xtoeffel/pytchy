from unittest import TestCase
from in_out.html import MatrixHtmlTable, MatrixTableCSS, HTML, LegendHtmlTable, LegendCSS
from core.image import PngReader
from core.color import ColorMatrix
from core.symbols import SymbolMatrix, HtmlSymbolProvider
from pathlib import Path


class TestColorMatrixHtmlTable(TestCase):

    def test_html(self) -> None:
        """
        Read PNG from file and generate color HTML table.
        """
        TestColorMatrixHtmlTable.test_html.__doc__

        path: Path = Path(__file__).parent.absolute() / '..' / 'img' / 'Pelican1.png'

        reader: PngReader = PngReader()
        reader.file_name = str(path)

        color_matrix: ColorMatrix = reader.read()

        html_table: MatrixHtmlTable = MatrixHtmlTable(color_matrix)
        
        html: str = html_table.make_html()
        print('HTML - test printout ')

        print('- open -')
        print(html[:40])
        print('- close -')
        print(html[-40:])

        self.assertTrue(len(html) > 0, 'html string empty')

        print('> OK')


class TestHTMLandCSS(TestCase):

    def test_html_and_css(self) -> None:
        """
        Read PNG file, generate full HTML with color table.
        Generate one file without symbols in table cells, the other with.
        """
        print(TestHTMLandCSS.test_html_and_css.__doc__)

        path: Path = Path(__file__).parent.absolute() / '..' / 'img' / 'Pelican1.png'

        reader: PngReader = PngReader()
        reader.file_name = str(path)

        color_matrix: ColorMatrix = reader.read()

        html_table: MatrixHtmlTable = MatrixHtmlTable(color_matrix)
        css: MatrixTableCSS = MatrixTableCSS()
        html: HTML = HTML(html_table.make_html(), header_html=css.make_html_style_tag())
        
        html_graphics_str: str = html.make_html()
        print('- open -')
        print(html_graphics_str[:25])
        print('- close -')
        print(html_graphics_str[-25:])

        out_path: Path = Path(__file__).parent.absolute() / 'test_out_nosymbols_pelican1.html'
        print(f'write html to "{str(out_path)}"')
        with open(str(out_path), 'w') as html_file:
            html_file.write(html_graphics_str)

        print('HTML - include symbols')
        out_path1: Path = Path(__file__).parent.absolute() / 'test_out_symbols_pelican1.html'
        out_path1_legend: Path = Path(__file__).parent.absolute() / 'test_out_legend_pelican1.html'

        symbol_provider: HtmlSymbolProvider = HtmlSymbolProvider()
        symbol_matrix: SymbolMatrix = SymbolMatrix(color_matrix, symbol_provider)
        html_table = MatrixHtmlTable(color_matrix, symbol_matrix)
        html_table.show_background_color = False
        html_graphics_str = HTML(html_table.make_html(), header_html=css.make_html_style_tag()).make_html()

        legend_html = LegendHtmlTable(symbol_matrix.legend)
        html_legend_str = HTML(legend_html.make_html(), LegendCSS().make_html_style_tag()).make_html()

        print(f'write html to "{str(out_path1)}"')
        with open(str(out_path1), 'w') as html_file:
            html_file.write(html_graphics_str)

        print(f'write legend to "{str(out_path1_legend)}"')
        with open(str(out_path1_legend), 'w') as html_file:
            html_file.write(html_legend_str)

        print('> OK')
