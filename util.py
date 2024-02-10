import platform

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

pip_str = "pip" if platform.system() == "Windows" else "pip3"
