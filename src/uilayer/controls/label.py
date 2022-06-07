from typing import Tuple

import pygame.font

from .control import Control
from src.config import config


# https://github.com/dmfabritius/PygameControls/blob/main/label.py
class Label(Control):
    def __init__(self, position: Tuple[float, float] = (0, 0), text: str = "label"):
        "A basic text label."
        super().__init__()
        self.position = position
        self.text = text
        self.font = pygame.font.SysFont("Calibri", 18)
        self.label = self.font.render(self.text, True, config.BLACK)

    def draw(self, surface):
        surface.blit(self.label, self.position)
