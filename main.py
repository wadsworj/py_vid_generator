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

pygame.init()
pygame.camera.init()
pygame.font.init()  # you have to call this at the start,


# scene = Scene("test", 0)

#def __init__(self, name, text, position, bounding_box, duration):
# text_element = TextElement("first", "text test", (50,50), (400, 700), 3)

# scene.add_element(text_element)

# video.add_scene(scene)

# video.render()

with open('videoScripts/rabinKarp.json') as data_file:
    data = json.load(data_file)

video = Video(data["name"], data["resolution"], data["audio"])

scene_builder = SceneBuilder(ElementBuilder())

for data_scene in data["scenes"]:
    scene = scene_builder.build(data_scene)
    video.add_scene(scene)

video.render()
