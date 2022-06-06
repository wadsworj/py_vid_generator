import os

import pygame
from config import config
from src.corelayer.helpers.interpolator import Interpolator

class ImageElement:
    def __init__(self):
        self.name = None
        self.position = None
        self.grid_position = None
        self.duration = None
        self.count = 0
        self.start_time = None
        self.image_string = None
        self.image = None
        self.data = None