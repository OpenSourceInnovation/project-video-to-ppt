#!/bin/bash

# setup python virtual environment
python3 -m venv proj
source proj/bin/activate
pip install -r requirements.txt

# install marp-cli
PACK_MGR=""
if command -v pnpm &> /dev/null
then
    PACK_MGR="pnpm"
elif command -v yarn &> /dev/null
then
    PACK_MGR="yarn"
elif command -v npm &> /dev/null
then
    PACK_MGR="npm"
else
    echo "No package manager found. Please install npm, yarn or pnpm."
    exit 1
fi

$PACK_MGR install -g @marp-team/marp-cli @mermaid-js/mermaid-cli

# check for chromie
if command -v google-chrome &> /dev/null
then
    echo "Google Chrome found."
else
    echo "Google Chrome not found. Please install it."
fi

