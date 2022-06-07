import pygame
import pygame_gui

from src.uilayer.controls.label import Label
from src.uilayer.controls.textbox import TextBox
from src.config import config

padding = 300
x_offset = 120
y_offset = 120

class ElementPropertiesView:
    def __init__(self, element, screen):
        self.element = element
        self.screen = screen
        self.controls = []
        spacing = 0

        for key in element:
            self.add_label(key, spacing)
            self.add_text_box(self.element[key], spacing, None)
            spacing += 30

    def add_label(self, text, spacing):
        # position: Tuple[float, float] = (0, 0), text: str = "label"):
        label = Label([x_offset + padding, y_offset + padding + spacing], text)
        self.controls.append(label)

    def add_text_box(self, text, spacing, command):
        text_box = TextBox([x_offset + padding + x_offset, y_offset + padding + spacing, 200, 30],
                           command=command,
                           active=False)

        text_box.buffer[:] = str(text)
        self.controls.append(text_box)

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYUP:  # Key pressed event
                    if event.key == pygame.K_ESCAPE:
                        return

                for control in self.controls:
                    control.get_event(event)

                self.render()
                pygame.display.update()

    def render(self):
        pygame.draw.rect(self.screen, config.WHITE,
                         [x_offset + padding, y_offset + padding, config.SCREEN_WIDTH - padding * 2 + x_offset,
                          config.SCREEN_HEIGHT - padding * 2 + y_offset])

        for control in self.controls:
            control.update()
            control.draw(self.screen)

