import argparse
import datetime
import os
import gradio as gr
from signal import SIGINT, signal
from utils.log import debug, info, logger, breakPoint as bc

import requests

from constants import *

CHUNK_SIZE  =   512
VIDEO_ID    =   ""
OUT_PPT_NAME=   PPTX_DEST
NO_IMAGES   =   False
QUESTIONS   =   5

def questionMode():
    from langchain.vectorstores import Chroma
    from langchain.embeddings import HuggingFaceInstructEmbeddings
    from langchain.chains import RetrievalQA
    from rich.progress import track
    
    from models.lamini import lamini as model, device
    from utils.subtitles import getSubsText
    from utils.chunk import LangChainChunker
    
    EMBEDS = HuggingFaceInstructEmbeddings(model_name=EMBEDDINGS, model_kwargs={"device": f"{device}"})
    subs = getSubsText(VIDEO_ID)
    chunker = LangChainChunker(subs)
    chunks = chunker.chunker(size=CHUNK_SIZE)
    
    info("Chunks size: " + str(len(chunks)))
    db   = Chroma.from_texts(chunks, EMBEDS)
    retriver = db.as_retriever(search_type="mmr")
    
    # initialize model
    llm_model = model
    llm = llm_model.load_model(
            max_length=400,
            temperature=0,
            top_p=0.95,
            repetition_penalty=1.15
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="map_reduce", retriever=retriver
    )
    
    def interface(msg, history):
        res = qa(msg)
        return str(res['result'])
    
    ui = gr.ChatInterface(
        fn=interface,
        examples=["What is the video about?", "key points of the video"],
        title=f"Question Mode - {VIDEO_ID}",
    )
    
    ui.launch()

def gradio_run(
    video_id, chunk_size: int,
    no_images: bool, no_chapters: bool, out_type="pdf"):
    
    VIDEO_ID = video_id
    CHUNK_SIZE = chunk_size
    NO_IMAGES = no_images
    NO_CHAPTERS = no_chapters
    OUT_PPT_NAME = f"{OUTDIR}/gradio-out{VIDEO_ID}.{out_type}"
    
    info("Loading modules..")
    from langchain.chains.summarize import load_summarize_chain
    from langchain.docstore.document import Document
    from rich.progress import track

    import utils.markdown as md
    from models.lamini import lamini as model
    from utils.marp_wrapper import marp
    from utils.ppt import generate_ppt
    from utils.subtitles import subs
    from utils.video import video
    from utils.chunk import ChunkByChapters
    
    # intialize marp
    out = marp(MD_DEST)
    out.add_header(config=MARP_GAIA)
    
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
    info(f"Getting subtitles {VIDEO_ID}..")
    raw_subs     = vid.getSubtitles()
    
    if raw_subs is None:
        logger.critical("No subtitles found, exiting..")
        exit()
    
    info(f"got {len(raw_subs)} length subtitles")
    
    
    if NO_CHAPTERS:
        chunker = subs(VIDEO_ID)
        chunks = chunker.getSubsList(size=CHUNK_SIZE)
        model_tmplts = llm_model.templates()
        summarizer = model_tmplts.summarize
        title_gen = model_tmplts.generate_title
        
        # title Photo
        first_pic = str(datetime.timedelta(seconds=chunks[0][1]))
        img_name = f"vid-{VIDEO_ID}_{first_pic}.png"
        img_path = f"{PNG_DEST}/{img_name}"
        vid.getframe(first_pic, img_path)
        out.add_page(md.h1(VIDEO_ID), md.image(url=img_name))
        out.marp_end()
        
        for chunk in track(chunks, description="(processing chunks) Summarizing.."):
            summary = summarizer(chunk[0])[0]["generated_text"].replace("-", "\n-")
            title = title_gen(chunk[0])[0]["generated_text"]
            
            heading = md.h2 if len(title) < 40 else md.h3
            out.add_page(heading(title), summary)
            
            if not NO_IMAGES and len(summary+title) < 270:
                timestamp = str(datetime.timedelta(seconds=chunk[1]))
                imgName = f"vid-{VIDEO_ID}_{timestamp}.png"
                imgPath = f"{PNG_DEST}/{imgName}"
                vid.getframe(timestamp, imgPath)
                out.add_body(md.image(imgName, align="left", setAsBackground=True))
                
            out.marp_end()
    else:
        raw_chapters = vid.getChapters(f"{YT_CHAPTER_ENDPOINT}{VIDEO_ID}")
        chunk_dict = ChunkByChapters(raw_chapters, raw_subs, CHUNK_SIZE)
        chain = load_summarize_chain(llm, chain_type="stuff")
            # TODO: ( use refine chain type to summarize all chapters )
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
    
    return os.path.abspath(OUT_PPT_NAME)

def gradio_Interface():
    app = gr.Interface(
        fn=gradio_run,
        inputs=[
            "text",
            gr.Slider(300, 2000, 1, label="Chunk Size", info="More chunk size = longer text & shorter numbber of slides"),
            gr.Checkbox(label="No Images", info="Don't keep images in output ( gives more spaces for larger text)"),
            gr.Checkbox(label="No Chapters", info="Don't use chapter based chunking"),
            gr.Dropdown(["pptx", "pdf", "html"], value="pptx" ,label="file format", info="which file format to generte.")
        ],
        outputs="file"
    )
    app.launch()
    
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
    # from models.lamini import lamini as model
    from models.gpt_3 import templates, Model
    from utils.marp_wrapper import marp
    from utils.ppt import generate_ppt
    from utils.subtitles import subs
    from utils.video import video
    from utils.chunk import ChunkByChapters
    
    # intialize marp
    out = marp(MD_DEST)
    out.add_header(config=MARP_GAIA)
    # out.add_body("<style> section { font-size: 1.5rem; } </style>")
    
    # initialize video
    vid = video(VIDEO_ID, f"{OUTDIR}/vid-{VIDEO_ID}")
    vid.download()
        
    # # initialize model (lamini)
    # llm_model = model
    # llm = llm_model.load_model(
    #         max_length=400,
    #         temperature=0,
    #         top_p=0.95,
    #         repetition_penalty=1.15
    # )
    
    # slice subtitle and chunk them 
    # to CHUNK_SIZE based on chapters
    info(f"Getting subtitles {VIDEO_ID}..")
    raw_subs     = vid.getSubtitles()
    
    if raw_subs is None:
        logger.critical("No subtitles found, exiting..")
        exit()
    
    info(f"got {len(raw_subs)} length subtitles")
    
    
    if NO_CHAPTERS:
        chunker = subs(VIDEO_ID)
        chunks = chunker.getSubsList(size=CHUNK_SIZE)
        # model_tmplts = llm_model.templates()
        model_tmplts = templates()
        summarizer = model_tmplts.ChunkSummarizer
        title_gen = model_tmplts.ChunkTitle
        
        for chunk in track(chunks, description="(processing chunks) Summarizing.."):
            summary = summarizer(chunk[0])
            title = title_gen(chunk[0])
            
            if not NO_IMAGES and len(summary+title) < 270:
                timestamp = str(datetime.timedelta(seconds=chunk[1]))
                imgPath = f"{PNG_DEST}/vid-{VIDEO_ID}_{timestamp}.png"
                vid.getframe(timestamp, imgPath)
                
            heading = md.h2 if len(title) < 40 else md.h3
            out.add_page(heading(title), summary)
            out.marp_end()
    else:
        raw_chapters = vid.getChapters(f"{YT_CHAPTER_ENDPOINT}{VIDEO_ID}")
        chunk_dict = ChunkByChapters(raw_chapters, raw_subs, CHUNK_SIZE)
        m = Model
        llm = m.model()
        chain = load_summarize_chain(llm, chain_type="stuff")
            # TODO: ( use refine chain type to summarize all chapters )
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
    optparser.add_argument("--questions-mode", dest="qm", action="store_true")
    optparser.add_argument("--gui-web", dest="gw", action="store_true")
    
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
    if opts.no_images is True:
        NO_IMAGES = True
    
    if opts.qm is True:
        questionMode()
        exit()
    
    if opts.gw is True:
        gradio_Interface()
        exit()
    
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
        os.mkdir(OUTEXTRA)
    
    if not os.path.exists(OUTEXTRA):
        os.mkdir(OUTEXTRA)
    
    run()
