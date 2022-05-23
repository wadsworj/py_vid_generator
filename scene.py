import pygame


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

    def render(self, screen, start_seconds):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()

        scene_time = pygame.time.get_ticks() - self.start_time
        seconds = ((scene_time / 1000) % 60) + start_seconds

        for element in self.elements:
            element.render(screen, seconds)

        if self.duration <= seconds:
            self.finished = True
