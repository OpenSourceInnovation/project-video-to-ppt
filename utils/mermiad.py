from utils.utils import Popen

def mermiadImage(mmdFile: str, out="out.svg"):
    """Convert a mermiad file to an image

    Args:
        mmdFile (str): The mermiad file
        out (str, optional): The output file. Defaults to "out.svg".
    """
    Popen(["mmdc", "-i", mmdFile, "-o", out])
