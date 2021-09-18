from typing import Any, Optional
from tkinter import ttk
from tkinter import filedialog, messagebox, Tk, N, E, S, W, NORMAL
from tkinter import StringVar, BooleanVar
from tkinter import PhotoImage
from pathlib import Path
from tki_gui.elements import PictureFrame, GeneratePatternFrame, MainMenu
from tki_gui.control import LoadPngCtrl, ToggleWidgetState
from tki_gui.control import LoadColorMatrix
from tki_gui.control import UpdateWidgetText, UpdateMessageAndStatus
from tki_gui.control import ClearVar, show_about_dialog
from tki_gui.variables import Variable
from tki_gui.generate import GeneratePatternFiles


class GUI:
    def __init__(self):
        self._root: Optional[Tk] = None
        self._picture_tab: Optional[PictureFrame] = None
        self._gen_pattern_tab: Optional[GeneratePatternFrame] = None

        self._png_file_name: Optional[StringVar] = None
        self._message_text: Optional[StringVar] = None
        self._generate_status: Optional[BooleanVar] = None
        self._symbol_set_name: Optional[StringVar] = None
        self._overwrite_files: Optional[BooleanVar] = None
        self._color_matrix_variable: Optional[Variable] = None
        self._symbol_provider: Optional[Variable] = None
        self._center_color: Optional[StringVar] = None
        self._status_text: StringVar = None

        self._build()
        self._init_data()
        self._link_controller()

    def _init_data(self) -> None:
        self._png_file_name = StringVar()
        self._message_text = StringVar()
        self._generate_status = BooleanVar()
        self._symbol_set_name = StringVar(value="Default")
        self._overwrite_files = BooleanVar(value=False)
        self._color_matrix_variable = Variable()
        self._symbol_provider = Variable()
        self._center_color = StringVar(value="cyan")
        self._status_text = StringVar(value="")

    def _build(self) -> None:
        self._root = Tk()
        self._root.geometry("400x450")
        self._root.resizable(0, 0)
        self._root.title("Pytchy")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        main_menu: MainMenu = MainMenu(self._root)
        main_menu.set_about_command(show_about_dialog)
        self._root.config(menu=main_menu.menu)

        icon_path: Path = Path(__file__).parent / "icons" / "pytchy.png"
        icon: PhotoImage = PhotoImage(file=str(icon_path))
        self._root.iconphoto(True, icon)

        note_book = ttk.Notebook(self._root, padding="5 5 5 5")
        note_book.grid(column=0, row=0, sticky=(N, E, S, W))

        self._picture_tab = PictureFrame(note_book)
        note_book.add(self._picture_tab.frame, text="Picture")

        self._gen_pattern_tab = GeneratePatternFrame(note_book)
        note_book.add(self._gen_pattern_tab.frame, text="Generate Pattern")

    def _link_controller(self) -> None:
        assert self._png_file_name is not None
        assert self._message_text is not None
        assert self._generate_status is not None
        assert self._symbol_set_name is not None
        assert self._overwrite_files is not None
        assert self._color_matrix_variable is not None
        assert self._symbol_provider is not None
        assert self._center_color is not None
        assert self._status_text is not None
        assert self._gen_pattern_tab is not None
        assert self._picture_tab is not None

        self._gen_pattern_tab.symbol_set_combobox[
            "textvariable"
        ] = self._symbol_set_name
        self._gen_pattern_tab.overwrite_checkbutton["variable"] = self._overwrite_files
        self._gen_pattern_tab.center_color_combobox["textvariable"] = self._center_color
        self._gen_pattern_tab.status_label["textvariable"] = self._status_text

        clear_status_text: ClearVar = ClearVar(self._status_text)
        self._center_color.trace_add("write", clear_status_text.clear)
        self._symbol_set_name.trace_add("write", clear_status_text.clear)
        self._overwrite_files.trace_add("write", clear_status_text.clear)
        self._png_file_name.trace_add("write", clear_status_text.clear)

        load_png: LoadPngCtrl = LoadPngCtrl(
            self._png_file_name, self._picture_tab.image_canvas
        )
        self._picture_tab.open_png_button["command"] = load_png.open_png

        load_color_matrix: LoadColorMatrix = LoadColorMatrix(
            self._png_file_name, self._color_matrix_variable
        )
        self._png_file_name.trace("w", load_color_matrix.load)

        toggle_generate_button: ToggleWidgetState = ToggleWidgetState(
            self._gen_pattern_tab.generate_button, self._generate_status
        )
        self._generate_status.trace("w", toggle_generate_button.update)

        update_msg_text: UpdateWidgetText = UpdateWidgetText(
            self._message_text, self._gen_pattern_tab.message_text_widget
        )
        self._message_text.trace("w", update_msg_text.update_text)
        self._message_text.set("Open PNG file to enable generation.")

        update_msg_and_status: UpdateMessageAndStatus = UpdateMessageAndStatus()
        update_msg_and_status.set_png_file_name(self._png_file_name)
        update_msg_and_status.set_color_matrix(self._color_matrix_variable)
        update_msg_and_status.set_symbol_set_name(self._symbol_set_name)
        update_msg_and_status.set_generate_status(self._generate_status)
        update_msg_and_status.set_message_text(self._message_text)
        update_msg_and_status.set_overwrite_files(self._overwrite_files)
        update_msg_and_status.set_symbol_provider(self._symbol_provider)
        self._color_matrix_variable.add_event_callback(update_msg_and_status.update)
        self._symbol_set_name.trace("w", update_msg_and_status.update)
        self._overwrite_files.trace("w", update_msg_and_status.update)

        generate_stitch_pattern: GeneratePatternFiles = GeneratePatternFiles()
        generate_stitch_pattern.set_color_matrix(self._color_matrix_variable)
        generate_stitch_pattern.set_symbol_provider(self._symbol_provider)
        generate_stitch_pattern.set_png_file_name(self._png_file_name)
        generate_stitch_pattern.set_mark_center_color(self._center_color)
        generate_stitch_pattern.set_done_callback(update_msg_and_status.update)
        generate_stitch_pattern.set_status_text(self._status_text)
        self._gen_pattern_tab.generate_button[
            "command"
        ] = generate_stitch_pattern.generate

    def show(self) -> None:
        assert self._root is not None

        self._root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.show()
