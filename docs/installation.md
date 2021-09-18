# Installation

The tool is available over different ways:

- For _Windows_:
    1. GUI version [pytchy_gui_1_0_0.zip](pytchy_gui_1_0_0.zip).
    2. Command line tool [pytchy_1_0_0.zip](pytchy_1_0_0.zip),

- any _Operating system_ that support _Python_:

    3. _github_ repo at [https://github.com/xtoeffel/pytchy](https://github.com/xtoeffel/pytchy) 

## Running over Python Interpreter
You must have the *Python* interpreter installed. Recommended
is to install [Anaconda](https://www.anaconda.com/products/individual) - Individual.

### Conda Environment
_Pytchy_ ships with an `environment.yml` file defining the
requirements for the *environment* to run the tool.

Create the environment by executing from the shell:
```
conda env create -f environment.yml
```

It is sufficient to [update](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#updating-an-environment) the environment in case
you downloaded a newer version of _Pytchy_ and only if `environment.yml` changed.

### Activate the Environment

The conda environment is named _Pytchy_ and must be
activated before running the tool over the _Python_ interpreter. 
To activate the environment call:
```
conda activate pytchy
```
