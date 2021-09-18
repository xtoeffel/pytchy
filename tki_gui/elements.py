from tkinter import StringVar, Canvas, N, W, E, S, NORMAL, DISABLED, END, WORD
from tkinter import Text, Tk, Menu
from tkinter import ttk
from typing import Optional, Any, Callable


class MainMenu:
    def __init__(self, root: Tk) -> None:
        self._root: Tk = root
        self._menu: Optional[Menu] = None
        self._about_command: Optional[Callable[[], None]] = None

        self._build()

    def _build(self) -> None:
        self._menu = Menu(self._root)
        self._menu.add_command(label="About", command=self._about_command_delegate)

    def _about_command_delegate(self, *args: Any) -> None:
        if self._about_command is not None:
            self._about_command()

    def set_about_command(self, about_command: Callable[[], None]) -> None:
        self._about_command = about_command

    @property
    def menu(self) -> Menu:
        assert self._menu is not None, "undefined menu"
        return self._menu


class PictureFrame:
    def __init__(self, parent: ttk.Widget) -> None:
        self._parent: ttk.Widget = parent

        self._frame: Optional[ttk.Frame] = None
        self._image_canvas: Optional[Canvas] = None
        self._open_png_button: Optional[ttk.Button] = None

        self._build()

    def _build(self) -> None:
        self._frame = ttk.Frame(self._parent, padding="5 5 5 5")
        self._frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=5, pady=2)

        status_text: ttk.Label = ttk.Label(
            self._frame, text="Open PNG file to generate cross stitch pattern."
        )
        status_text.grid(column=0, row=1, sticky=(W, S), padx=5, pady=5)

        self._image_canvas = Canvas(self._frame, width=200, height=300)
        self._image_canvas.grid(column=0, row=0, sticky=(N, W, E, S), padx=5, pady=2)

        self._open_png_button = ttk.Button(self._frame, text="Open PNG")
        self._open_png_button.grid(column=0, row=2, sticky=(E, S), padx=5, pady=2)

        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._frame.rowconfigure(1, weight=0)

    @property
    def frame(self) -> ttk.Frame:
        assert self._frame is not None
        return self._frame

    @property
    def image_canvas(self) -> Canvas:
        assert self._image_canvas is not None
        return self._image_canvas

    @property
    def open_png_button(self) -> ttk.Button:
        assert self._open_png_button is not None
        return self._open_png_button


class GeneratePatternFrame:
    def __init__(self, parent: ttk.Widget) -> None:
        self.parent: ttk.Widget = parent

        self._frame: Optional[ttk.Frame] = None
        self._message_frame: Optional[ttk.LabelFrame] = None
        self._message_text_widget: Optional[Text] = None
        self._generate_button: Optional[ttk.Button] = None
        self._symbol_set_combobox: Optional[ttk.Combobox] = None
        self._center_color_combobox: Optional[ttk.Combobox] = None
        self._overwrite_checkbox: Optional[ttk.Checkbutton] = None
        self._status_label: Optional[ttk.Label] = None

        self._build()

    def _build(self) -> None:
        self._frame = ttk.Frame(self.parent, padding="5 5 5 5")
        self._frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.rowconfigure(0, weight=0)
        self._frame.rowconfigure(1, weight=0)
        self._frame.rowconfigure(2, weight=0)
        self._frame.rowconfigure(3, weight=1)
        self._frame.rowconfigure(4, weight=0)

        symbol_set_text: ttk.Label = ttk.Label(self._frame, text="Symbol Set")
        symbol_set_text.grid(column=0, row=0, sticky=(N, E), padx=5, pady=5)
        self._symbol_set_combobox = ttk.Combobox(
            self._frame,
            state="readonly",
            exportselection=0,
            values=["Default", "Letters", "Filled", "Skinny"],
        )
        self._symbol_set_combobox.current(0)
        self._symbol_set_combobox.grid(column=1, row=0, sticky=(N, W), padx=5, pady=5)

        center_color_text: ttk.Label = ttk.Label(self._frame, text="Center Color")
        center_color_text.grid(column=0, row=1, sticky=(N, E), padx=5, pady=5)
        self._center_color_combobox = ttk.Combobox(
            self._frame,
            state="readonly",
            exportselection=0,
            values=[
                "cyan",
                "green",
                "red",
                "blue",
                "magenta",
                "gray",
                "lightgray",
                "yellow",
                "purple",
            ],
        )
        self._center_color_combobox.current(0)
        self._center_color_combobox.grid(column=1, row=1, sticky=(N, W), padx=5, pady=5)

        self._overwrite_checkbox = ttk.Checkbutton(
            self._frame, text="Overwrite existing files"
        )
        self._overwrite_checkbox.grid(column=1, row=2, sticky=(N, W), padx=5, pady=5)

        self._message_frame = ttk.LabelFrame(
            self._frame, text="Messages", padding="5 5 5 5", height=100
        )
        self._message_frame.grid(
            column=0, row=3, columnspan=2, sticky=(N, E, W, S), padx=5, pady=5
        )

        self._message_text_widget = Text(self._message_frame, bg="#ececec", wrap=WORD)
        self._message_text_widget.pack(fill="both", expand=True)
        self._message_text_widget["state"] = DISABLED

        self._status_label = ttk.Label(self._frame, text="")
        self._status_label.grid(
            column=0, row=4, columnspan=2, sticky=(N, W), padx=5, pady=5
        )

        self._generate_button = ttk.Button(self._frame, text="Generate")
        self._generate_button.grid(column=1, row=4, sticky=(S, E), padx=5, pady=5)
        self._generate_button["state"] = DISABLED

    @property
    def frame(self) -> ttk.Frame:
        assert self._frame is not None
        return self._frame

    @property
    def generate_button(self) -> ttk.Button:
        assert self._generate_button is not None
        return self._generate_button

    @property
    def symbol_set_combobox(self) -> ttk.Combobox:
        assert self._symbol_set_combobox is not None
        return self._symbol_set_combobox

    @property
    def center_color_combobox(self) -> ttk.Combobox:
        assert self._center_color_combobox is not None
        return self._center_color_combobox

    @property
    def message_text_widget(self) -> Text:
        assert self._message_text_widget is not None
        return self._message_text_widget

    @property
    def overwrite_checkbutton(self) -> ttk.Checkbutton:
        assert self._overwrite_checkbox is not None
        return self._overwrite_checkbox

    @property
    def status_label(self) -> ttk.Label:
        assert self._status_label is not None
        return self._status_label
