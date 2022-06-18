import json
import os

import pygame.camera
from videoBuilder import VideoBuilder
from src.config import config

pygame.init()
pygame.camera.init()
pygame.font.init()  # you have to call this at the start,

script_to_load = 'radix_sort_02.json'
data_file = os.path.join(config.RESOURCES_LOCATION, config.RESOURCES_SCRIPTS_LOCATION, script_to_load)
output_data_file = os.path.join(config.OUTPUT_LOCATION, config.OUTPUT_DATA_LOCATION, script_to_load)

# test if previous output file exists
if os.path.exists(output_data_file):
    data_file = output_data_file

with open(data_file) as data_file:
    data = json.load(data_file)

video = VideoBuilder.build(data)

video.render(True)

video.save_data_file()
