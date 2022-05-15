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

video = Video("test", (1280, 720))

scene = Scene("test", 0)

#def __init__(self, name, text, position, bounding_box, duration):
text_element = TextElement("first", "text test", (50,50), (400, 700), 3)

scene.add_element(text_element)

video.add_scene(scene)

video.render()
