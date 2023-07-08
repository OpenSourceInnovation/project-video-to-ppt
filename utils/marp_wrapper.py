import utils.markdown as md

class marp:
    def __init__(self, path):
        self.path = path
        self.f = open(path, "w")
        self.f.truncate(0) # clear the file

    def marp_write(self, text):
        self.f.write(text)

    def add_header(
        self,
        _class: str = "lead",
        paginate: bool = True,
        background: str = "#fff",
        backgroundImage: str = None,
        extra_styles: str = None
    ):
        ## write the header
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
        self.writeifNotNone(backgroundImage)
        self.marp_end()
        self.writeifNotNone(extra_styles) # for extra css styles
    
    def writeifNotNone(self, var):
        if var is not None:
            self.marp_write(var)
    
    def add_page(self, 
                title=None,
                body=None,
                directives: str = None
    ):
        self.writeifNotNone(f"<!-- {directives} -->\n")
        self.writeifNotNone(title)
        self.writeifNotNone(body)
    
    def add_directives(self, directives: str):
        self.marp_write(f"<!-- {directives} -->\n")
    
    def add_body(self, body: str):
        self.marp_write(body)
    
    def marp_end(self):
        self.marp_write("\n\n---\n\n") # page end
    
    def close_file(self):
        self.f.close() # close the file and flush the buffer
