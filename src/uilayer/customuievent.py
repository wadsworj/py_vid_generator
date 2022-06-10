import pygame


class CustomUIEvent:
    def __init__(self, event_type, data):
        self.data = data
        self.event_type = event_type
