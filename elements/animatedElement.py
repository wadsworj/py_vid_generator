import math

import pygame

import config


class AnimatedTextElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.text = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None

    def render(self, screen, scene_seconds):
        pass