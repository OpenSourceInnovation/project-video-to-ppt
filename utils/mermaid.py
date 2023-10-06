from utils.utils import Popen
import os

import os
from subprocess import Popen

def mermaidImage(mmdFile: str, out="out.svg"):
    """
    Convert a mermaid file to an image using the mermaid CLI tool.

    Args:
        mmdFile (str): The path to the mermaid file.
        out (str, optional): The output file path. Defaults to "out.svg".

    Returns:
        str: The absolute path to the output file.
    """
    Popen(["mmdc", "-i", mmdFile, "-o", out])
    return os.path.abspath(out)
