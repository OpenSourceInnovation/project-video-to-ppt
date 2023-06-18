import markdown as md

class marp:
    def __init__(self, path):
        self.path = path
        self.f = open(path, "w")
        self.f.truncate(0) # clear the file

    def marp_write(self, text):
        self.f.write(text)

    def header(
        self,
        _class: str = "lead",
        paginate: bool = True,
        background: str = "#fff",
        backgroundImage: str = "",
    ):
        # ---
        # theme: gaia
        # _class: lead
        # paginate: true
        # backgroundColor: #fff
        # backgroundImage: url('https://marp.app/assets/hero-background.svg')
        # ---
        self.marp_write("---\n")
        self.marp_write(f"theme: gaia\n")
        self.marp_write(f"_class: {_class}\n")
        if paginate:
            self.marp_write(f"paginate: true\n")
        else:
            self.marp_write(f"paginate: false\n")
        self.marp_write(f"backgroundColor: {background}\n")
        self.marp_write(f"backgroundImage: {backgroundImage}\n")
        self.marp_write("---\n")
    
    def addpage(self, title, body):
        self.marp_write(md.h1(title))
        self.marp_write(body)
        self.marp_write("\n\n---\n\n")

