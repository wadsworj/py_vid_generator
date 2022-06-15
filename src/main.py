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

with open(data_file) as data_file:
    data = json.load(data_file)

video_builder = VideoBuilder()
video = video_builder.build(data)

video.render(True)

video.save_data_file()
