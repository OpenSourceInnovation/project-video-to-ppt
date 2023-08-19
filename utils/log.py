import logging
from rich.logging import RichHandler
from constants import DEBUG

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


def warn(msg):
    logging.warning(msg)

def info(msg):
    logging.info(msg)

def debug(msg):
    if DEBUG:
        logging.debug(msg)

def breakPoint():
    
    """ A quick function to pause the program for debug or analysis
    
    take user input Y/N
    if Y: break
    else: continue"""
    
    print("Breakpoint: Press Y to continue, N to exit")
    user_input = input()
    if user_input.lower() == "y" or user_input == "":
        pass
    else:
        logging.info("Exiting...")
        exit()
