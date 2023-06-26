import os

def generate_ppt(markdown_source, output_name, chromium_path="./chrome_sandbox") -> None:
    # check for marp
    if os.system("marp --version") != 0:
        raise Exception("Marp is not installed")
    
    # if user is root, then set CHROMIUM_PATH to chromium_path
    if os.getuid() == 0:
        os.environ["CHROMIUM_PATH"] = chromium_path
    
    # check for markdown source
    if not os.path.exists(markdown_source):
        raise Exception("Markdown source does not exist")
    
    # generate ppt
    os.system(f"marp {markdown_source} -o {output_name}")
