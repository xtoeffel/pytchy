# Executing Pytchy

This simple instruction gives you the basics how use the tool.
For the most part you will find your way through the command line help.
The GUI is very simple and should not require any instruction.

## The Command Line Interface

Open a shell or terminal on your system and navigate to the folder
where either the `pytchy.py` file or the executable `*.exe` is 
located (_Windows_ only).

The following chapters show you how to print the help screen 
in the shell.

### Windows Executable
Executables can be called directly (from Command line or _PowerShell_):
```powershell
pytchy.exe -h
```
This will print the help screen.
_Powershell_ requires to call `.\pytchy.exe`.

### Python Interpreter
Make sure to activate the environment if you use _conda_ by `conda activate pytchy`.
This applies to all all operating systems.

*Linux* or *MacOS* allow the script to be called directly (with or without file extension `.py`):
```powershell
./pytchy.py -h
./pytchy -h
```

_Windows_ does not support direct execution of *Python* scripts 
from a command line. 
On *Windows* use instead:
```powershell
python pytchy.py -h
```

## The GUI
### Windows Executable
Simply run the executable directly by double-click or from a shell or terminal.
The advantage of starting it from a shell is that more error messages are
available in case of bugs.

### Python Interpreter
For *Linux* or *MacOS* call from the shell either of:
```
./gui.py
./gui
```

On *Windows* do:
```powershell
python gui.py
```
