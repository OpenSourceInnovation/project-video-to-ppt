import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logging.disable('DEBUG')
logger = logging.getLogger("project-v-p")


def warn(msg):
    logger.warning(msg)


def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def breakPoint():
    """A quick function to pause the program for debug or analysis.

    This function takes user input Y/N. If Y, the program continues. If N, the program exits.

    Args:
        None

    Returns:
        None
    """

    print("Breakpoint: Press Y to continue, N to exit")
    user_input = input()
    if user_input.lower() == "y" or user_input == "":
        pass
    else:
        logger.info("Exiting...")
        exit()
