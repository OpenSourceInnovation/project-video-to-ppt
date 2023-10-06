import os


import os

def generate_ppt(
        markdown_source: str,
        output_name: str,
        chromium_path: str = "./chrome_sandbox") -> None:
    """
    Generates a PowerPoint presentation from a markdown file using Marp.

    Args:
        markdown_source (str): The path to the markdown file to be converted.
        output_name (str): The desired name of the output PowerPoint file.
        chromium_path (str, optional): The path to the Chromium browser executable. Defaults to "./chrome_sandbox".

    Raises:
        Exception: If Marp is not installed or if the markdown source file does not exist.

    Returns:
        None
    """
    # check for marp
    if os.system("marp --version") != 0:
        raise Exception("Marp is not installed")

    # if user is root, then set CHROMIUM_PATH to chromium_path
    if os.getuid() == 0 and os.name == "posix":
        os.environ["CHROME_PATH"] = chromium_path

    # check for markdown source
    if not os.path.exists(markdown_source):
        raise Exception("Markdown source does not exist")

    # generate ppt
    os.system(f"marp {markdown_source} -o {output_name} --allow-local-files")
