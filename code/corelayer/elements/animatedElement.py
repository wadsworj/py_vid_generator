from os.path import exists

import pygame
from code.config import config

try:
    from code.corelayer.helpers.interpolator import Interpolator
except ModuleNotFoundError:
    from ..helpers.interpolator import Interpolator


class AnimatedTextElement:
    def __init__(self):
        self.name = None
        self.text = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None
        self.key_frames = []
        self.data = None