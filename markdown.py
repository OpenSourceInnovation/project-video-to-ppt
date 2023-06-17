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

def quote(text):
    return f"> {text}"

def bold(text):
    return f"**{text}**"

def italic(text):
    return f"*{text}*"
