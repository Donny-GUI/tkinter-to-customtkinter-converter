# Tkinter to CustomTkinter Converter

![Python_logo_icon](https://user-images.githubusercontent.com/108424001/226063288-66da2f57-f5b7-49f1-bdd5-f465e963b125.png)





# tkinter-to-customtkinter-converter
Convert your tkinter scripts and guis to custom tkinter with this command line tool. Can determine programming paradigm and import structure to keep consistency across files

please, please, please if you experience a bug or bad operations please submit them to me so i can fix it immediatly. i dont have hundreds of guis to test this on.


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
python tk_to_ctk.py <target> <target2> <target3> ....
```

### Unix/Linux Users


```Bash
git clone https://github.com/Donny-GUI/tkinter-to-customtkinter-converter.git
cd tkinter-to-customtkinter-converter
python3 tk_to_ctk.py <target> <target2> <target3> ....
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



