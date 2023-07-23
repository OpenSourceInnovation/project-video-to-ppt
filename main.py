import argparse, datetime
from signal import signal, SIGINT
import constants as c
import os

CHUNK_SIZE  =   512
VIDEO_ID    =   ""
OUT_PPT_NAME=   c.PPTX_DEST
NO_IMAGES   =   False

def run():
    from rich.progress import track
    from models.lamini import summarize
    from models.lamini import generate_title
    from utils.marp_wrapper import marp
    import utils.markdown as md
    from utils.subtitles import subs as chunker
    from utils.ppt import generate_ppt
    from utils.video import video
    
    # Intermediary Markdown file
    print("Creating Markdown file...")
    ppt = marp(c.MD_DEST)
    ppt.add_header(
        theme="uncover",
        background="",
        _class="invert",
    )
    
    # smaller font size (1.5rem)
    ppt.add_body("<style> section { font-size: 1.5rem; } </style>")
    
    # Generate video
    vid = video(f"https://youtu.be/{VIDEO_ID}", f"{c.OUTDIR}/vid-{VIDEO_ID}")
    vid.download()
    
    # Get the Subtitles from the YouTube video
    print("Getting subtitles...")
    
    chunker_init    = chunker(VIDEO_ID)
    chunks          = chunker_init.getSubsList(size=CHUNK_SIZE)
    chunk_len       = len(chunks)

    print(f"subtitles divided to {chunk_len} chunks")

    chunk_num = 1
    for chunk in track(chunks, description="Processing chunks"):
        print(f"processing Chunk: {chunk_num}/{chunk_len}")
        
        timestamp = str(datetime.timedelta(seconds=chunk[1]))
        img_path  = f"{c.PNG_DEST}/vid-{VIDEO_ID}_{timestamp}.png"
        
        summary = summarize(str(chunk[0]))[0]["generated_text"].replace("-", "\n-")
        title = generate_title(str(chunk[0]))[0]["generated_text"]
        
        # heading size control
        if len(title) < 40:
            heading = md.h2
        if len(title) > 50:
            heading = md.h3
        
        ppt.add_page( heading(title), summary )
        
        if not NO_IMAGES:
            vid.getframe(timestamp=timestamp, out=img_path)

        if os.path.exists(img_path):
            # if summary is long ignore images for better page and no clipping
            if len(summary+title) < 270:
                ppt.add_body(md.image( 
                                  img_path.replace(f"{c.OUTEXTRA}/", ""),
                                  align="left",
                                  setAsBackground=True, 
                                  size="contain"
                                  ))
            
        ppt.marp_end()
        chunk_num += 1

    print(f"Generating {OUT_PPT_NAME}..")
    ppt.close_file()
    generate_ppt(c.MD_DEST, OUT_PPT_NAME)

def exithandle(_signal, _frame):
    print(f"\nExiting... | {str(_signal)} | {str(_frame)}")
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
    
    if not os.path.exists(c.OUTDIR):
        os.mkdir(c.OUTDIR)
        os.mkdir(c.OUTEXTRA)
    
    if not os.path.exists(c.OUTEXTRA):
        os.mkdir(c.OUTEXTRA)
    run()
