import pygame

try:
    from src.corelayer.helpers.interpolator import Interpolator
except ModuleNotFoundError:
    from ..helpers.interpolator import Interpolator

class ShapeElement:
    def __init__(self):
        self.name = None
        self.count = 0
        self.key_frames = None
        self.data = None
        self.renderer = None