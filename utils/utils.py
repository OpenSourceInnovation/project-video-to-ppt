import subprocess
import os


def Popen(cmd: list) -> str:
    """Run a command and return the output as a string

    - example: print(Popen(["ls", "-l"]))

    Args:
        cmd (list): The command to run

    Returns:
        str: The output of the command
    """
    return subprocess.Popen(
        cmd,
        shell=False,
        stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')


def getfilesR(path: str, sorted=False) -> list:
    """Get all files in a directory recursively

    Args:
        path (str): The path to the directory. "." for current directory
        sorted (bool, optional): Sort the files. Defaults to False.

    Returns:
        list: The list of files
    """

    files = []
    # include depth
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    if sorted:
        files.sort()

    return files
