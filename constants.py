import os
from chromadb.config import Settings

# to store all the generated files (*.pdf, *pptx, *webm, *mp3)
OUTDIR="out"

# path extra out files
OUTEXTRA="out/extra"

# yt video nameformat and loacation 
YT_DEST=f"{OUTEXTRA}/vid-"

# name for genrated pptx
PPTX_DEST = f"{OUTDIR}/out.pptx"

# name for generated markdown summary file
MD_DEST = f"{OUTEXTRA}/summary.md"

# name for generated png files 
PNG_DEST = f"{OUTEXTRA}"

# name for generated ppt
PPT_DEST = f"{OUTDIR}/out.ppt"
 
## MARP CONFIGURATION
MARP_01 = {
    "theme": "uncover",
    "background": "",
    "class": "invert",
}

MARP_GAIA = {
    "theme": "gaia",
    "background": "",
    "class": "lead",
}

MARP_02 = {
    "theme": "marpit-theme",
    "background": "",
    "class": "",
}

# ChromaDB settings
EMBEDDINGS = "hkunlp/instructor-large"

# summarizer options
SUM_CHAIN_TYPE = "stuff"

YT_CHAPTER_ENDPOINT = "https://yt.lemnoslife.com/videos?part=chapters&id="

