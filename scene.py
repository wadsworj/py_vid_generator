import pygame


class Scene:
    def __init__(self, name, scene_index):
        self.name = name
        self.elements = []
        self.scene_index = scene_index
        self.finished = False
        self.start_time = None

    def add_element(self, element):
        self.elements.append(element)

    def render(self, screen):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()

        scene_time = pygame.time.get_ticks() - self.start_time
        seconds = (scene_time / 1000) % 60

        for element in self.elements:
            element.render(screen, seconds)
