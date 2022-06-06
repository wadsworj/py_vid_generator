import json
import os

import pygame.camera
from config import config

from corelayer.elements.elementBuilder import ElementBuilder
from sceneBuilder import SceneBuilder
from videoBuilder import VideoBuilder

pygame.init()
pygame.camera.init()
pygame.font.init()  # you have to call this at the start,

script_to_load = 'radix_sort_02.json'
data_file = os.path.join(config.RESOURCES_LOCATION, config.RESOURCES_SCRIPTS_LOCATION, script_to_load)
with open(data_file) as data_file:
    data = json.load(data_file)

video_builder = VideoBuilder()
video = video_builder.build(data)

scene_builder = SceneBuilder(ElementBuilder())

for data_scene in data["scenes"][data["start_scene"]:]:
    scene = scene_builder.build(data_scene)
    video.add_scene(scene)

video.render()
