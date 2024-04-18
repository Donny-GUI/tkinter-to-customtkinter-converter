# Tkinter to CustomTkinter Converter

![Python_logo_icon](https://user-images.githubusercontent.com/108424001/226063288-66da2f57-f5b7-49f1-bdd5-f465e963b125.png)





# tkinter-to-customtkinter-converter
Convert your tkinter scripts and guis to custom tkinter with this command line tool. Can determine programming paradigm and import structure to keep consistency across files

please, please, please if you experience a bug or bad operations please submit them to me so i can fix it immediatly. i dont have hundreds of guis to test this on.

# New Cmdline Application

```
tk2ctk   -  Tkinter to CustomTkinter

Description:  tkinter to customtkinter file converter.

Usage:        tk2ctk [file] [Options]
              tk2ctk -m [file] [file2] [file3] ...
              tk2ctk [file] -o [file]

Options:
    -h, --help           Show this help message and exit
    -o, --output         Define the output file
    -v, --verbose        Operate with higher verbosity level
    -l, --listboxes      Convert listboxes to custom listboxes
    -m, --multiple       Convert multiple target scripts
    -e, --examples       Show examples for flags and options
```

-o Flag is used to set the outfile


-l flag converts tk.Listbox to a custom version


-m is the multiple targets flag. Use this to target more then one tkinter script


-e shows example usages


![Screenshot 2024-02-13 195702](https://github.com/Donny-GUI/tkinter-to-customtkinter-converter/assets/108424001/796ab2eb-3edb-40fe-953e-0009b3aa8e42)


## Before

![before](https://github.com/Donny-GUI/tkinter-to-customtkinter-converter/assets/108424001/900c08c2-e364-4533-bf0d-227536aae7df)


## After

![after](https://github.com/Donny-GUI/tkinter-to-customtkinter-converter/assets/108424001/4a692be9-a57e-4b8a-9061-d32eebded834)


# New Source Converter Class
The SourceConverter class is a standalone class that can convert source to source.
That is that it can convert tkinter python source strings to customtkinter source strings.

### Usage

Case #1  from a string

```
from .converter import SourceConverter
sc = SourceConverter()
with open("myfile.py", "r) as f:
    content = f.read()
ctk_source = sc.from_string(content)
```

or

```
import .converter
sc = converter.SourceConverter()
with open("myfile.py", "r) as f:
    content = f.read()
ctk_source = sc.from_string(content)
```


Case #2  from a file

```
from .converter import SourceConverter
sc = SourceConverter()
ctk_source = sc.from_file(content)
```

or 

```
import .converter
sc = converter.SourceConverter()
ctk_source = sc.from_file(content)
```



# Update April 18 2024
- Added converter.py file
- Added SourceConverter class


# Update March 23 2024
- Now fixes textvariable -> variable function/class instance parameter names.
- Now fixes orient -> orientation function/class instance parameter names.
- tree.py file added to use the ast module to find function and class instances that use the parameters


# Update Feb 13 2024
- New command line interface
- now supports listboxes
  

# Update Feb 9 2024
- fixed base and meta class tkinter widgets to represent ctk ones
- fixed Checkbutton to CheckBox
- fixed Radiobutton to RadioButton
- No longer falsly import tk.Text
- uses CTkSlider for tk.Scale

# Updates April 14 2023

- Now supports ttk by default
- General syntax improvements in source code
- General performance improvements
- now converts all widget background_color to bg_color as specified in the property exception in customtkinter
- converts all widget foreground_color to fg_color as specified in the the property exception in customtkinter


# Coming Up Next

- tkinter.ListBox conversion to customtkinter class ScrollableFrame or "ScrollableFrameBox/ScrollableCheckBox/ScrollableSwitchBox/ScrollableLabelBox" 
- possible CTkMessageBox addition from Akascape

# Thank you!

Thank you Tom Schimansky for this wonderful and beautiful tkinter addition!
I am not associated with customtkinter in any way.

Please see https://github.com/TomSchimansky/CustomTkinter


# Getting Started

### Windows Users

```Powershell
git clone https://github.com/Donny-GUI/tkinter-to-customtkinter-converter.git
cd tkinter-to-customtkinter-converter
python tk_to_ctk.py <target> 
```

### Unix/Linux Users


```Bash
git clone https://github.com/Donny-GUI/tkinter-to-customtkinter-converter.git
cd tkinter-to-customtkinter-converter
python3 tk_to_ctk.py <target> 
```


# Files

## tkinter-to-customtkinter.util
Contains utility functions and constants
```Python3
get_operating_system()
# get the name of the operating system
pip_str
# Literal string for using pip aka pip or pip3
```

## tkinter-to-customtkinter.widget_replacer
Contains the WidgetReplacer class



