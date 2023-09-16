import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("project-v-p")


def warn(msg):
    logger.warning(msg)


def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


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
        logger.info("Exiting...")
        exit()
