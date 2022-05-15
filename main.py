import json

import pygame, sys, os
import pygame.camera
from pygame.locals import *

from elements.element import Element
from elements.textElement import TextElement
from scene import Scene
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

video = Video(data["name"], data["resolution"])

for data_scene in data["scenes"]:
    scene = Scene(data_scene["scene_name"], data_scene["scene_index"])
    for data_element in data_scene["elements"]:
        # def __init__(self, name, text, position, bounding_box, duration):
        element = TextElement(data_element["name"],
                              data_element["text"],
                              data_element["position"],
                              data_element["bounding_box"],
                              data_element["duration"],
                              data_element["font_size"],
                              data_element["font_type"])

        scene.add_element(element)

    video.add_scene(scene)

video.render()
