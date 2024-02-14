help_template = f"""\
tk2ctk   -  Tkinter to CustomTkinter

Description:  \033[2m\033[3mtkinter to customtkinter file converter. \033[0m

Usage:        \033[2m\033[3mtk2ctk [file] [Options]  \033[0m
              \033[2m\033[3mtk2ctk -m [file] [file2] [file3] ... \033[0m
              \033[2m\033[3mtk2ctk [file] -o [file] \033[0m

Options:
    -h, --help           \033[2m\033[3mShow this help message and exit\033[0m
    -o, --output         \033[2m\033[3mDefine the output file\033[0m
    -v, --verbose        \033[2m\033[3mOperate with higher verbosity level\033[0m
    -l, --listboxes      \033[2m\033[3mConvert listboxes to custom listboxes\033[0m
    -m, --multiple       \033[2m\033[3mConvert multiple target scripts\033[0m
    -e, --examples       \033[2m\033[3mShow examples for flags and options\033[0m\n"""

examples_template = f"""\
┌───  Flag/Option   ───── Example Usage    ────────────────────────────┐
│    -h, --help       →   tk2ctk -h                                    │
│    -o, --output     →   tk2ctk target.py -o newfile.py               │
│    -v, --verbose    →   tk2ctk target.py -v                          │
│    -l, --listboxes  →   tk2ctk target.py -l                          │
│    -m, --multiple   →   tk2ctk -m target1.py file2.py pathway3.py    │
│    -e, --examples   →   tk2ctk -e                                    │
└──────────────────────────────────────────────────────────────────────┘\
    """


def print_examples() -> None:
    print(examples_template)

def print_help_screen() -> None:
    print(help_template)