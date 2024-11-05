#!/bin/bash

sudo apt update && apt upgrade

sudo apt install cups sqlite3 ngrok

sudo dtparam spi=on
pip install requirements.txt
