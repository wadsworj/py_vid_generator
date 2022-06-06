import math
import os
from os.path import exists
from src.config import config
import pygame

from src.corelayer.renderers.pygame.textrenderer import TextRenderer

class TextElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.grid_position = None
        self.text = None
        self.duration = None
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None
        self.data = None

