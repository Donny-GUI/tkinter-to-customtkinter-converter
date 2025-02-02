import argparse


def get_parser():

    argument_parser = argparse.ArgumentParser(
        description="Convert Tkinter scripts to Customtkinter scripts",
        prog="tk2ctk",
        usage="tk2ctk [Target] [-h] [-o Output] [-l] [-v] [-m Target Target Target Target ... ]",
        add_help=False,
        exit_on_error=False,
    )
    argument_parser.add_argument(
        "Target",
        default=None,
        help="Input file path for Tkinter script",
        metavar="TARGET",
        nargs="?",
    )
    argument_parser.add_argument(
        "-h",
        "--help",
        default=False,
        dest="Help",
        action="store_true",
        help="Show this help message and exit",
    )
    argument_parser.add_argument(
        "-o",
        "--outfile",
        dest="Output",
        default=None,
        nargs="?",
        metavar="OUTFILE",
        const="",
        help="Specify output file",
    )
    argument_parser.add_argument(
        "-v",
        "--verbose",
        dest="Verbose",
        default=False,
        action="store_true",
        help="Operate with verbosity",
    )
    argument_parser.add_argument(
        "-l",
        "--listboxes",
        default=False,
        dest="Listboxes",
        action="store_true",
        help="Convert listboxes to custom listboxes",
    )
    argument_parser.add_argument(
        "-m",
        "--multiple",
        dest="Multiple",
        default=[],
        nargs="+",
        help="Specify multiple targets",
    )
    argument_parser.add_argument(
        "-e",
        "--examples",
        dest="Examples",
        default=False,
        action="store_true",
        help="Show examples for additional help",
    )
    return argument_parser
