import utils.markdown as md


class marp:
    """
    A class that provides methods to generate markdown slides using Marp.

    Attributes:
    path (str): The path to the file where the markdown slides will be written.
    f (file): The file object used to write the markdown slides.
    """

    def __init__(self, path):
        """
        Initializes a new instance of the marp class.

        Args:
        path (str): The path to the file where the markdown slides will be written.
        """
        self.path = path
        self.f = open(path, "w")
        self.f.truncate(0)  # clear the file

    def marp_write(self, text):
        """
        Writes the given text to the markdown file.

        Args:
        text (str): The text to be written to the markdown file.
        """
        self.f.write(text)

    def add_header(
        self,
        theme: str = "default",
        _class: str = "lead",
        paginate: bool = True,
        background: str = "",
        backgroundImage: str = None,
        extra_styles: str = None,
        config: dict = None
    ):
        """
        Adds a header to the markdown file.

        Args:
        theme (str): The theme to be used for the header.
        _class (str): The class to be used for the header.
        paginate (bool): Whether or not to paginate the header.
        background (str): The background color to be used for the header.
        backgroundImage (str): The background image to be used for the header.
        extra_styles (str): Any extra CSS styles to be applied to the header.
        config (dict): A dictionary containing the configuration options for the header.
        """
        # write the header
        # ---
        # theme: gaia
        # _class: lead
        # paginate: true
        # backgroundColor: #fff
        # backgroundImage: url('https://marp.app/assets/hero-background.svg')
        # ---

        if config is not None:
            theme = config["theme"]
            background = config["background"]
            _class = config["class"]

        self.marp_write("---\n")
        self.marp_write("marp: true\n")
        self.marp_write(f"theme: {theme}\n")
        self.marp_write(f"class: {_class}\n")
        if paginate:
            self.marp_write(f"paginate: true\n")
        else:
            self.marp_write(f"paginate: false\n")
        self.marp_write(f"backgroundColor: {background}\n")
        self.writeifNotNone(backgroundImage)
        self.marp_end()
        self.writeifNotNone(extra_styles)  # for extra css styles

    def writeifNotNone(self, var):
        """
        Writes the given variable to the markdown file if it is not None.

        Args:
        var: The variable to be written to the markdown file.
        """
        if var is not None:
            self.marp_write(var)

    def add_page(self,
                 title=None,
                 body=None,
                 directives: str = None
                 ):
        """
        Adds a new page to the markdown file.

        Args:
        title (str): The title of the page.
        body (str): The body of the page.
        directives (str): Any directives to be applied to the page.
        """
        self.writeifNotNone(f"<!-- {directives} -->\n")
        self.writeifNotNone(title)
        self.writeifNotNone(body)

    def add_directives(self, directives: str):
        """
        Adds the given directives to the markdown file.

        Args:
        directives (str): The directives to be added to the markdown file.
        """
        self.marp_write(f"<!-- {directives} -->\n")

    def add_body(self, body: str):
        """
        Adds the given body to the markdown file.

        Args:
        body (str): The body to be added to the markdown file.
        """
        self.marp_write(body)

    def marp_end(self):
        """
        Adds the end of a page to the markdown file.
        """
        self.marp_write("\n\n---\n\n")  # page end

    def close_file(self):
        """
        Closes the markdown file and flushes the buffer.
        """
        self.f.close()  # close the file and flush the buffer
