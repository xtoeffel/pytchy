from unittest import TestCase
from core.symbols import SymbolMatrix, CharProvider
from core.image import PngReader
from core.color import Color, ColorMatrix
from pathlib import Path


class TestColor(TestCase):

    def test_color_properties(self) -> None:
        """
        Test properties and setter for RGB color.
        Create color object, set properties and evaluate.
        """
        print(TestColor.test_color_properties.__doc__)

        color: Color = Color(123, 155, 201, 10)
        print(color)
        self.assertEqual(123, color.red)
        self.assertEqual(155, color.green)
        self.assertEqual(201, color.blue)
        self.assertEqual(10, color.alpha)

        color.green = 231
        print(color)
        self.assertEqual(123, color.red)
        self.assertEqual(231, color.green)
        self.assertEqual(201, color.blue)
        self.assertEqual(10, color.alpha)

        color.red = 4
        print(color)
        self.assertEqual(4, color.red)
        self.assertEqual(231, color.green)
        self.assertEqual(201, color.blue)
        self.assertEqual(10, color.alpha)

        color.blue = 94
        print(color)
        self.assertEqual(4, color.red)
        self.assertEqual(231, color.green)
        self.assertEqual(94, color.blue)
        self.assertEqual(10, color.alpha)

        color.alpha = 255
        print(color)
        self.assertEqual(4, color.red)
        self.assertEqual(231, color.green)
        self.assertEqual(94, color.blue)
        self.assertEqual(255, color.alpha)

        print('alpha=0 -> transparent')
        color.alpha = 0
        self.assertTrue(color.is_transparent, 'not transparent')

        print('> OK')


class TestReadPNG(TestCase):

    def test_read_png(self) -> None:
        """
        Read PNG file, test array of Color.
        """
        print(TestReadPNG.test_read_png.__doc__)

        path: Path = Path(__file__).parent.absolute() / '..' / 'img' / 'Pelican1.png'

        reader: PngReader = PngReader()
        reader.file_name = str(path)

        color_matrix: ColorMatrix = reader.read()
        print(f'width x height = 70 x 117')
        self.assertEqual(70, color_matrix.width, 'width not 70')
        self.assertEqual(117, color_matrix.height, 'height not 117')

        print('cell type')
        for row in color_matrix.matrix:
            for pixel in row:
                self.assertTrue(isinstance(pixel, Color), 'cell not Color instance')

        print(f'number of unique colors: {color_matrix.color_count}')
        self.assertEqual(16, color_matrix.color_count, 'number of unique colors not 16')

        print('> OK')


class TestSymbolMaker(TestCase):

    def test_make_symbols(self) -> None:
        """
        Test reading PNG file, generating ColorMatrix and Symbols.
        """
        print(TestSymbolMaker.test_make_symbols.__doc__)

        path: Path = Path(__file__).parent.absolute() / '..' / 'img' / 'Pelican1.png'

        reader: PngReader = PngReader()
        reader.file_name = str(path)

        color_matrix: ColorMatrix = reader.read()
        symbol_provider: CharProvider = CharProvider()

        symbol_matrix: SymbolMatrix = SymbolMatrix(color_matrix, symbol_provider)
        print(f'width x height = 70 x 117')
        self.assertEqual(70, symbol_matrix.width, 'width not 70')
        self.assertEqual(117, symbol_matrix.height, 'height not 117')
        
        print('> OK')
