#!/bin/bash

# Set up Real-Time-Voice-Cloning
git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning
cd Real-Time-Voice-Cloning/
pip install -q -r requirements.txt
apt-get install -qq libportaudio2
gdown https://drive.google.com/uc?id=1-Vohg3oaS82c0y_tJQx-J8123oWnkkwf
unzip pretrained.zip
