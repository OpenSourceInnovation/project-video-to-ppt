# Project `Video to PPT`

A project to experiment with LLM's generate to do tasks like

- slide creation
- Question Answer chatbot interface
- Diagram Generation

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

For basic command line usage to generate PPT

```bash
python3 main.py -v <video_id> --no-chapers
```

- `-v <video_id>` youtube video id ( in `https://youtu.be/PPZ0dQEIrTk?si=pRlTVjfTIzwqvChS` **PPZ0dQEIrTk** is the video id)
- `--no-chapters` is recommended cause not all videos have chapters

More options:

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

## GUI interfaces

All the task have a seperate GUI for this time being.

### Video To PPT

```bash
python3 main.py --gui-web
```

> Generates slides with video summary and convert to presentation or pdf

for any given video, the project will generate a summary of the video and will create a PPT/PPTX with different slides covering the summary of the video.

The video subtitles are fetched from youtube and fed to the LLM's to generate the summary of the video then the summary is used to create the PPT/PPTX with marp.

### Video TO Question-Answer interface

![Alt text](images/QAInterface.png)

```bash
python3 main.py -v VIDEO_ID --questions-mode
```

QA interface uses vectorstores to quickly search for the related data and fed to the LLM's to generate the answer for the question.

![Alt text](images/vector_stores.png)
> image source & refer about vector stores: [lanchain.com](https://python.langchain.com/docs/modules/data_connection/vectorstores/)

### Diagram generation

> Runs with GPT 3 for better reasoning capabilities

```bash
python3 main.py --diagram-gen
```

![Diagram Generation](images/diagram_interface.png)
