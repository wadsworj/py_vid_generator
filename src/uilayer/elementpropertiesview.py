import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine

from src.uilayer.controls.label import Label
from src.uilayer.controls.textbox import TextBox
from src.config import config

padding = 300
x_offset = 120
y_offset = 120

class ElementPropertiesView(UIWindow):
    def __init__(self, element, screen, ui_manager):
        self.position = [x_offset + padding, y_offset + padding]
        self.size = [config.SCREEN_WIDTH - padding * 2 + x_offset, config.SCREEN_HEIGHT - padding * 2 + y_offset]

        super().__init__(pygame.Rect(self.position, (320, 240)), ui_manager,
                         window_display_title='Super Awesome Pong!',
                         object_id='#pong_window',
                         resizable=True)

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
        if not str(text):
            return
        # text_box = TextBox([x_offset + padding + x_offset, y_offset + padding + spacing, 200, 30],
        #                    command=command,
        #                    active=False)
        #
        # text_box.buffer[:] = str(text)
        # self.controls.append(text_box)

        self.test_text_entry = UITextEntryLine(pygame.Rect((int(0),
                                                            int(0) + spacing),
                                                           (200, -1)),
                                               self.ui_manager,
                                               container=self)
        self.test_text_entry.set_text(str(text))

    def update(self, time_delta):
        super().update(time_delta)

    # def update(self):
    #     pass
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return
        #         if event.type == pygame.KEYUP:  # Key pressed event
        #             if event.key == pygame.K_ESCAPE:
        #                 return
        #
        #         for control in self.controls:
        #             control.get_event(event)
        #
        #         self.render()
        #
        #         pygame.display.update()

    def render(self):
        pygame.draw.rect(self.screen, config.WHITE, [self.position, self.size])

        for control in self.controls:
            control.update()
            control.draw(self.screen)
