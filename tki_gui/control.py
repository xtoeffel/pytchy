from typing import Optional, Any, List, Callable
from pathlib import Path
from tkinter import StringVar, IntVar, BooleanVar
from tkinter import Canvas, filedialog, messagebox, Text
from tkinter import NORMAL, DISABLED, END, CENTER
from tkinter import ttk
from PIL import Image, ImageTk  # type: ignore
from core.image import PngReader
from core.color import ColorMatrix
from tki_gui.variables import Variable
from core.symbols import HtmlSymbolProvider, HtmlFilledSymbolProvider
from core.symbols import CharProvider, SkinnySymbolProvider, PSymbolProvider
from tki_gui.generate import HtmlFileSet, HtmlOutput, init_html_file_set
from pytchy import version


def show_about_dialog() -> None:
    messagebox.showinfo(
        "About Pytchy", f"Version: {version}\n\nFree under GNU Public License"
    )


class ClearVar:
    def __init__(self, variable: StringVar):
        self._variable: StringVar = variable

    def clear(self, *args: Any) -> None:
        self._variable.set("")


class LoadPngCtrl:
    def __init__(self, png_file_name: StringVar, image_canvas: Canvas) -> None:
        self._png_file_name: StringVar = png_file_name
        self._image_canvas: Canvas = image_canvas

    def open_png(self) -> None:
        assert self._png_file_name is not None, "png file name undefined"
        assert self._image_canvas is not None, "image canvas undefined"

        initial_directory: Path
        if self._png_file_name.get() != "":
            initial_directory = Path(self._png_file_name.get()).parent

        else:
            initial_directory = Path.home()

        png_file_name: str = filedialog.askopenfilename(
            initialdir=str(initial_directory),
            title="Select PNG File",
            filetypes=(("PNG Files", "*.png"),),
        )
        if len(png_file_name) == 0:
            return

        try:
            png_image = ImageTk.PhotoImage(Image.open(png_file_name))
            self._image_canvas.create_image(
                self._image_canvas.winfo_width() / 2,
                self._image_canvas.winfo_height() / 2,
                anchor=CENTER,
                image=png_image,
            )
            self._image_canvas.image = png_image  # type: ignore
            self._png_file_name.set(png_file_name)

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    @property
    def png_file_name(self) -> StringVar:
        return self._png_file_name

    @property
    def image_canvas(self) -> Canvas:
        return self._image_canvas


class ToggleWidgetState:
    def __init__(self, widget: ttk.Widget, control_variable: BooleanVar) -> None:
        self._widget: ttk.Widget = widget
        self._control_variable: BooleanVar = control_variable

    def update(self, *args: Any) -> None:
        if self._control_variable.get():
            self._widget["state"] = NORMAL
        else:
            self._widget["state"] = DISABLED


class UpdateWidgetText:
    def __init__(
        self, text_var: StringVar, text_widget: Text, append_text: bool = False
    ) -> None:
        self._text_var: StringVar = text_var
        self._text_widget: Text = text_widget
        self._append_text: bool = False

    def update_text(self, *args) -> None:
        self._text_widget["state"] = NORMAL
        if not self._append_text:
            self._text_widget.delete(1.0, END)
        self._text_widget.insert(END, self._text_var.get())
        self._text_widget["state"] = DISABLED

    @property
    def text_var(self) -> StringVar:
        return self._text_var

    @property
    def text_widget(self) -> Text:
        return self._text_widget


class LoadColorMatrix:
    def __init__(self, png_file_name: StringVar, color_matrix: Variable) -> None:
        self._png_file_name: StringVar = png_file_name
        self._color_matrix: Variable = color_matrix

    def load(self, *args) -> None:
        assert self._png_file_name is not None, "undefined png file name"
        assert self._color_matrix is not None, "undefined color matrix"

        png_reader: PngReader = PngReader()
        png_reader.file_name = self._png_file_name.get()

        try:
            color_matrix: ColorMatrix = png_reader.read()
            self._color_matrix.value = color_matrix

        except Exception as ex:
            messagebox.showerror("Error Reading ColorMatrix", str(ex))

    @property
    def png_file_name(self) -> StringVar:
        assert self._png_file_name is not None, "png file name not set"
        return self._png_file_name


class UpdateMessageAndStatus:
    def __init__(self) -> None:
        self._png_file_name: Optional[StringVar] = None
        self._color_matrix: Optional[Variable] = None
        self._symbol_set_name: Optional[StringVar] = None
        self._generate_status: Optional[BooleanVar] = None
        self._message_text: Optional[StringVar] = None
        self._symbol_provider: Optional[Variable] = None
        self._overwrite_files: Optional[BooleanVar] = None

    def set_png_file_name(self, png_file_name: StringVar) -> None:
        self._png_file_name = png_file_name

    def set_color_matrix(self, color_matrix: Variable) -> None:
        self._color_matrix = color_matrix

    def set_generate_status(self, status: BooleanVar) -> None:
        self._generate_status = status

    def set_symbol_set_name(self, name: StringVar) -> None:
        self._symbol_set_name = name

    def set_message_text(self, msg_text: StringVar) -> None:
        self._message_text = msg_text

    def set_symbol_provider(self, provider: Variable) -> None:
        self._symbol_provider = provider

    def set_overwrite_files(self, overwrite: BooleanVar) -> None:
        self._overwrite_files = overwrite

    @property
    def png_file_name(self) -> StringVar:
        assert self._png_file_name is not None, "undefined png_file_name"
        return self._png_file_name

    @property
    def color_matrix(self) -> Variable:
        assert self._color_matrix is not None, "undefined color_matrix"
        return self._color_matrix

    @property
    def generate_status(self) -> BooleanVar:
        assert self._generate_status is not None, "undefined generate_status"
        return self._generate_status

    @property
    def symbol_set_name(self) -> StringVar:
        assert self._symbol_set_name is not None, "undefined symbol_set_name"
        return self._symbol_set_name

    @property
    def message_text(self) -> StringVar:
        assert self._message_text is not None, "undefined message_text"
        return self._message_text

    @property
    def symbol_provider(self) -> Variable:
        assert self._symbol_provider is not None, "undefined symbol_provider"
        return self._symbol_provider

    @property
    def overwrite_files(self) -> BooleanVar:
        assert self._overwrite_files is not None, "undefined overwrite_files"
        return self._overwrite_files

    def _write_message(self, msg_lines: List[str]):
        new_section: str = "\n".join(msg_lines)
        self.message_text.set(new_section)

    def _get_symbol_set(self) -> PSymbolProvider:
        symbol_set: PSymbolProvider
        if self.symbol_set_name.get().lower() == "default":
            symbol_set = HtmlSymbolProvider()
        elif self.symbol_set_name.get().lower() == "letters":
            symbol_set = CharProvider()
        elif self.symbol_set_name.get().lower() == "skinny":
            symbol_set = SkinnySymbolProvider()
        elif self.symbol_set_name.get().lower() == "filled":
            symbol_set = HtmlFilledSymbolProvider()
        else:
            raise ValueError(f'Invalid symbol set name "{self.symbol_set_name.get()}"')
        return symbol_set

    def update(self, *args: Any) -> None:
        if (
            self.color_matrix.value is None
            or self.symbol_set_name.get() is None
            or self.symbol_set_name.get() == ""
        ):
            return

        symbol_set: PSymbolProvider = self._get_symbol_set()
        color_matrix: ColorMatrix = self.color_matrix.value
        assert isinstance(
            color_matrix, ColorMatrix
        ), f"invalid type color matrix {color_matrix.__class__.__name__}"

        final_statement: str = "> OK"
        evaluate_statement: str = (
            f'Symbol set "{self.symbol_set_name.get()}" '
            f"supports max {symbol_set.max_number} colors."
        )
        if symbol_set.max_number < color_matrix.color_count:
            evaluate_statement = (
                f'! Symbol set "{self.symbol_set_name.get()}" '
                f"supports {symbol_set.max_number} colors "
                f"but PNG has {color_matrix.color_count}."
            )
            evaluate_statement += "\nSelect another symbol set or reduce PNG colors."
            final_statement = "> Unable to generate stitch pattern."

        file_statement: str = "New HTML files will be created."
        html_file_set: HtmlFileSet = init_html_file_set(self.png_file_name.get())
        if html_file_set.files_exist():
            if self.overwrite_files.get():
                file_statement = "* Existing HTML files will be overwritten."
            else:
                file_statement = "! HTML files exist, enable Overwrite or move files."
                final_statement = "> Unable to generate stitch pattern."

        png_file_path: Path = Path(self.png_file_name.get())

        self._write_message(
            [
                "Successfully loaded PNG file.",
                "",
                f"File: {png_file_path.name}",
                f"Size: {color_matrix.width} x {color_matrix.height}",
                f"Colors: {color_matrix.color_count}",
                "",
                evaluate_statement,
                "",
                file_statement,
                "",
                final_statement,
            ]
        )

        self.generate_status.set(final_statement == "> OK")
        if final_statement == "> OK":
            self.symbol_provider.value = symbol_set
