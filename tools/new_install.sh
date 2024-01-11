#!/bin/bash

sudo apt update && apt upgrade

sudo apt install cups

sudo dtparam spi=on
pip install requirements.txt
