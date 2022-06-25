import pygame

from src.corelayer.helpers import elementsorter
from src.corelayer.helpers.frametoseconds import FrameToSeconds


class Scene:
    def __init__(self):
        self.name = None
        self.scene_index = None
        self.elements = []
        self.finished = False
        self.start_time = None
        self.duration = None

    def add_element(self, element):
        self.elements.append(element)

    def render(self, screen, frame, screen_objects):
        seconds = FrameToSeconds.convert_frame_to_seconds(frame)

        self.elements = sorted(self.elements, key=elementsorter.sort_by_key_elements, reverse=False)

        for element in self.elements:
            element.renderer.render(element, screen, seconds, screen_objects)

        if self.duration <= seconds:
            self.finished = True
