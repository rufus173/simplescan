
# First time install

## Requirements

 - `libsane-dev`
 - `gcc`
 - `python3-pip`
 - `python3-venv`
 - `python3`

When this is first installed, it needs to be configured with `./configure.sh`

# How to use

Run using the `./run.sh` command in this directory

# Code explanation

We start by starting up SANE and getting a list of scanners for the user to pick from. (using the `ListboxDialogue` class)
Next is to instantiate the `SaneScanner` class with the device and pass it to the `ScannerUI` class.
This class provides a mode switcher and a frame for the selected mode 'module' to be displayed.
Mode modules are just classes that are provided a parent widget and a scanner, and that build an interface inside of it. When the mode is changed, all the `grid_slaves()` are destroyed and the new mode class is instantiated in its place.
