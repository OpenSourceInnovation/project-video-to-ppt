import argparse, datetime
from signal import signal, SIGINT

CHUNK_SIZE  =   512
VIDEO_ID    =   ""
OUT_PPT_NAME=   "out.pptx"

def run():
    from rich.progress import track
    from utils.subtitles import getSubsText
    from models.distilbart_cnn_12_6 import summarize
    from models.t5_small_medium_title_generation import t5model as generate_title
    from utils.marp_wrapper import marp
    import utils.markdown as md
    # from utils.chunk import LangChainChunker as chunker
    from utils.subtitles import subs as chunker
    from utils.ppt import generate_ppt
    from utils.video import video
    import os
    
    # Intermediary Markdown file
    print("Creating Markdown file...")
    ppt = marp("summary.md")
    ppt.add_header(
        theme="uncover",
        background="",
        _class="invert",
    )
    
    # smaller font size (1.5rem)
    ppt.add_body("<style> section { font-size: 1.5rem; } </style>")
    
    # Generate video
    vid = video(f"https://youtu.be/{VIDEO_ID}",
                f"out/vid-{VIDEO_ID}")
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
        # TODO: better file path
        img_path  = f"out/vid-{VIDEO_ID}_{timestamp}.png"
        
        summary = summarize(chunk[0])
        vid.getframe(timestamp)
        title = generate_title(summary)

        ppt.add_page( md.h2(title), summary )

        if os.path.exists(img_path):
            ppt.add_body(md.image( img_path,
            align="left", setAsBackground=True, size="contain"))
            
        ppt.marp_end()
        chunk_num += 1
        continue

    print(f"Generating {OUT_PPT_NAME}..")
    ppt.close_file()
    generate_ppt("summary.md", OUT_PPT_NAME)

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
    
    run()
