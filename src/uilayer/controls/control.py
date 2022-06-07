from typing import Tuple
from pygame import Surface


# https://github.com/dmfabritius/PygameControls/blob/main/control.py
class Control:

    def __init__(self):
        self.value: float = 0.0

    def move(self, position: Tuple[float, float]):
        pass  # controls can optionally overwrite this default move() method

    def update(self):
        pass  # controls can optionally overwrite this default update() method

    def draw(self, surface: Surface):
        raise Exception("All controls need to implement a draw() method")

    def get_event(self, events):
        pass