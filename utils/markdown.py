def h1(text):
    return f"# {text}\n"


def h2(text):
    return f"## {text}\n"


def h3(text):
    return f"### {text}\n"


def backtick(text):
    return f"`{text}`"


def code(lang, text):
    return f"```{lang}\n{text}\n```"


def link(text, url):
    return f"[{text}]({url})"


def image(
    url,
    align=None,
    height=None,
    size=None,
    setAsBackground=False,
):
    """
    Return markdown image syntax with marp options.

    Args:
        url (str): Image url (only online images).
        align (str, optional): Image alignment (left, right, center).
        height (str, optional): Image height (ex:"2in").
        size (str, optional): Cover, contain, auto, fix, x%.
        setAsBackground (bool, optional): Set image as background.

    Returns:
        str: Markdown image syntax with marp options.
    """
    options = ""
    if align is not None:
        options += f"{align}"
    if height is not None:
        options += f" {height}"
    if size is not None:
        options += f" {size}"
    if setAsBackground:
        options += " bg"

    return f"![{options}]({url})"


def quote(text):
    return f"> {text}"


def bold(text):
    return f"**{text}**"


def italic(text):
    return f"*{text}*"
