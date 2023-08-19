import argparse
import datetime
import json
import os
import textwrap
from signal import SIGINT, signal
from utils.log import debug, info, logger, breakPoint as bc

import requests

from constants import *

CHUNK_SIZE  =   512
VIDEO_ID    =   ""
OUT_PPT_NAME=   PPTX_DEST
NO_IMAGES   =   False
QUESTIONS   =   5

def run():
    info("Loading modules..")
    from langchain.chains.summarize import load_summarize_chain
    # from langchain.vectorstores import Chroma
    # from langchain.embeddings.huggingface import HuggingFaceEmbeddings
    # from langchain.chains import RetrievalQA
    # from langchain.llms import HuggingFacePipeline
    from langchain.docstore.document import Document
    from rich.progress import track

    import utils.markdown as md
    from models.lamini import lamini as model
    from utils.marp_wrapper import marp
    from utils.ppt import generate_ppt
    from utils.subtitles import subs
    from utils.video import video
    # intialize marp
    out = marp(MD_DEST)
    out.add_header(config=MARP_GAIA)
    # out.add_body("<style> section { font-size: 1.5rem; } </style>")
    
    # initialize video
    vid = video(VIDEO_ID, f"{OUTDIR}/vid-{VIDEO_ID}")
    vid.download()
        
    # initialize model
    llm_model = model
    llm = llm_model.load_model(
            max_length=400,
            temperature=0,
            top_p=0.95,
            repetition_penalty=1.15
    )
    
    # slice subtitle and chunk them 
    # to CHUNK_SIZE based on chapters
    info(f"Getting subtitles & chapters for video {VIDEO_ID}..")
    raw_chapters = vid.getChapters(f"{YT_CHAPTER_ENDPOINT}{VIDEO_ID}")
    raw_subs     = vid.getSubtitles()
    
    if raw_subs is None:
        logger.critical("No subtitles found, exiting..")
        exit()
    
    info(f"got {len(raw_subs)} length subtitles")

    # chunk processing
    chunks = []
    chunk_dict = {}
    if len(raw_chapters) != 0:
        chapters = [[chapter['title'], chapter['time']] for chapter in raw_chapters]
        # set timestamp to last second of chapter
        for c in range(len(chapters)-1):
            if c == len(chapters):
                break
            chapters[c][1] = chapters[c+1][1] - 1
        
        # chunking based on chapters
        for c in track(range(len(chapters)-1), description="Chunking.."):
            title    = chapters[c][0]
            start    = 0 if c == 0 else chapters[c-1][1]+1
            duration = chapters[c][1]
            
            current_chunk = ""
            
            for sublinedata in raw_subs:
                cstart: int = sublinedata['start']
                subline: str = sublinedata['text']
                
                # TODO: Optimise by slicing?
                if cstart < start:
                    continue
                if cstart >= duration:
                    break
                
                total_size = len(current_chunk) + len(subline)
                if total_size + 1 < CHUNK_SIZE:
                    current_chunk += subline
                else:
                    chunks.append(
                        [
                            [current_chunk.strip()],
                            [cstart],
                        ]
                    )
                    current_chunk = ""
            
            chunk_dict.update({title: chunks})
            chunks = []
    
    chain = load_summarize_chain(llm, chain_type="stuff")

    # TODO: Tommorow ( use refine chain type to summarize all chapters )
    img_hook = False
    for title, subchunks in track(chunk_dict.items(), description="(processing chunks) Summarizing.."):
        # Typecase subchunks to Document for every topic
        # get summary for every topic with stuff/refine chain
        # add to final summary
        
        debug(subchunks)
        docs = [ Document(page_content=t[0]) for t in subchunks[0] ]
        summary = chain.run(docs)
        
        if img_hook == False:
            ts = str(datetime.timedelta(seconds=subchunks[0][1][0]))
            img_path  = f"{PNG_DEST}/vid-{VIDEO_ID}_{ts}.png"
            vid.getframe(ts, img_path)
            if os.path.exists(img_path):
            # if summary is long ignore images for better page and no clipping
                if len(summary+title) < 270:
                    out.add_body(md.image( 
                                      img_path.replace(f"{OUTEXTRA}/", ""),
                                      align="left",
                                      setAsBackground=True
                              ))
        out.add_page(md.h2(title), summary)
        out.marp_end()

    info(f"Generating {OUT_PPT_NAME}..")
    out.close_file()
    generate_ppt(MD_DEST, OUT_PPT_NAME)
    print(f"Done! {OUT_PPT_NAME}")

def exithandle(_signal, _frame):
    logger.warning(f"Exiting... | {str(_signal)} | {str(_frame)}")
    exit()

if __name__ == "__main__":
    signal(SIGINT, exithandle)
    
    optparser = argparse.ArgumentParser(
        prog="video to ppt (dev)",
        description="Convert Youtube videos to PPT/pdf with large language models"
    )
    optparser.add_argument("-v", "--video", dest="video_id", help="YouTube video ID")
    optparser.add_argument("--chunk-size", dest="chunk_size", type=int)
    optparser.add_argument( "-o", "--out", dest="out_ppt_name")
    optparser.add_argument("--no-images", dest="no_images", action="store_true")
    optparser.add_argument("--no-chapters", dest="no_chapters", action="store_true")
    
    opts = optparser.parse_args()
    
    if opts.video_id is None:
        print("Please provide a YouTube video ID")
        exit()
    else:
        VIDEO_ID = opts.video_id
    
    if opts.chunk_size is not None:
        CHUNK_SIZE = int(opts.chunk_size)
    
    if opts.out_ppt_name is not None:
        OUT_PPT_NAME = opts.out_ppt_name
    
    if opts.no_chapters is True:
        NO_CHAPTERS = True
    
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
        os.mkdir(OUTEXTRA)
    
    if not os.path.exists(OUTEXTRA):
        os.mkdir(OUTEXTRA)
    
    run()
