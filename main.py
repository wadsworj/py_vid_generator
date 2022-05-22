import json

import pygame, sys, os
import pygame.camera
from pygame.locals import *

from elements.element import Element
from elements.elementBuilder import ElementBuilder
from elements.textElement import TextElement
from scene import Scene
from sceneBuilder import SceneBuilder
from video import Video
from videoBuilder import VideoBuilder

pygame.init()
pygame.camera.init()
pygame.font.init()  # you have to call this at the start,

with open('videoScripts/rabinKarp.json') as data_file:
    data = json.load(data_file)

video_builder = VideoBuilder()
video = video_builder.build(data)

scene_builder = SceneBuilder(ElementBuilder())

for data_scene in data["scenes"][data["start_scene"]:]:
    scene = scene_builder.build(data_scene)
    video.add_scene(scene)

video.render()
