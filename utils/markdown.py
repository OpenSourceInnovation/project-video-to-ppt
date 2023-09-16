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
    """Summary
    return markdown image syntax with marp options

    Args:
        url (str): image url (only online images)
        align (str, optional): image alignment (left, right, center)
        height (str, optional): image height (ex:"2in")
        size (str, optional): cover, contain, auto, fix, x%
        setAsBackground (bool, optional): set image as background
    Returns:
        _type_: _description_
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
