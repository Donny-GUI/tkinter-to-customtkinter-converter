import platform
import ast
import copy


def point(thing: any) -> any:
    """ Makes a reference to an object """
    ref = thing
    return ref

def interface(thing: any) -> any:
    """ Create a a copy of the object but reference nested objects """
    replica = copy.copy(thing)
    return replica

def clone(thing: any) -> any:
    """ Create a copy of an object not as a reference """
    newthing = copy.deepcopy(thing)
    return newthing

def parsetree(source: str) -> ast.AST:
    try:
        tree = ast.parse(source, type_comments=True)
    except:
        tree = ast.parse(source)
    finally:
        return tree

def get_operating_system() -> str:
    """
    Determine the operating system being used.

    Returns:
        str: A string indicating the operating system. Possible values are "Windows", "Linux", "macOS", or "Unknown".
    """
    system: str = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "macOS"
    else:
        return "Unknown"

pip_str = "pip" if get_operating_system() == "Windows" else "pip3"
python_str = "python" if get_operating_system() == "Windows" else "python3"


def classes_begin_index(lines: list[str]) -> int:

    # first try to put the CTkListBox as the first Class in the class area
    count = 0 
    for line in lines:
        if line.startswith("class "):
            return count
        count += 1
    
    # if there is no classes defined in the script. Find the first non import line
    count = 0
    for line in lines:
        if line.startswith("import ") or line.startswith("from "):
            count += 1
            continue
        else:
            return count
    
    return count

def get_listbox_source():
    with open("listbox.py", "r") as file:
        lines = file.readlines()[1:]
    return lines

def has_listbox(filepath: str) -> bool:
    with open(filepath, "r") as file:
        content = file.read()
    try:
        lbi = content.find("tk.Listbox(")
        return True
    except IndexError:
        return False
    
def print_warning(string: str) -> None:
    print("\033[35m[WARNING]\033[0m:\033[31m"+string+"\033[0m")

def print_update(string: str) -> None:
    if isinstance(string, list):
        string = "[" + ", ".join(string) + "]"
    print("\033[32m[UPDATE]\033[0m:\033[33m"+string+"\033[0m")
