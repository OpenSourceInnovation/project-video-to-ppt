# Project `Video to PPT`

A project to convert a video data to a PPT/PPTX with different slides covering summary of the video.

## Getting Started

Project uses both Local LLM's and GPT 3.5 turbo api to generate the text from the target

> Its suggested to have a GPU for the project to run smoothly when using local LLMS

### Installation

```bash
apt install git -y
git clone https://github.com/SaicharanKandukuri/project-video-to-ppt
cd project-video-to-ppt
pip install -r requirements.txt
```

### Usage

For basic command line usage

```bash
python3 main.py -v <video_id> --no-chapers -o out.pdf
```

#### GUI

Project has integration with gradio to provide a GUI and clean interface to the project to startup.

```bash
python3 main.py -v <video_id> -o out.pdf --gui-web
```

```cmd
usage: video to ppt (dev) [-h] [-v VIDEO_ID] [--chunk-size CHUNK_SIZE] [-o OUT_PPT_NAME] [--no-images] [--no-chapters] [--questions-mode]
                          [--gui-web] [--use-model TARGET_MODEL]

Convert Youtube videos to PPT/pdf with large language models

options:
  -h, --help            show this help message and exit
  -v VIDEO_ID, --video VIDEO_ID
                        YouTube video ID
  --chunk-size CHUNK_SIZE
  -o OUT_PPT_NAME, --out OUT_PPT_NAME
  --no-images
  --no-chapters
  --questions-mode
  --gui-web
  --use-model TARGET_MODEL
                        Set model to use (gpt3, lamini, bart) default: lamini
```

## How it works

for any given video, the project will generate a summary of the video and will create a PPT/PPTX with different slides covering the summary of the video.

The video subtitles are fetched from youtube and fed to the LLM's to generate the summary of the video then the summary is used to create the PPT/PPTX with marp.

