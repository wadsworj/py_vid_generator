import pygame
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

from src.config import config
from src.uilayer.elementview.keyframesview import KeyFramesView

padding = 100
x_offset = 120
y_offset = 120

label_width = 100


class ElementPropertiesView(UIWindow):
    def __init__(self, parent, element, screen, ui_manager):
        self.parent = parent
        self.ui_manager = ui_manager

        size_x = config.SCREEN_WIDTH / 2
        size_y = config.SCREEN_HEIGHT / 4
        self.position = [x_offset, y_offset]
        self.size = [size_x, size_y]

        if 'name' in element:
            title = element['name']
        elif 'text' in element:
            title = element['text']
        else:
            title = "property"

        super().__init__(pygame.Rect(self.position, self.size), self.ui_manager,
                         window_display_title=title,
                         object_id='#pong_window',
                         resizable=True)

        self.element = element
        self.screen = screen
        self.windows = []
        spacing = 0

        for key in self.element:
            if key == 'key_frames':
                self.add_key_frames_view()
                continue
            self.add_label(key, spacing)
            self.add_text_box(self.element[key], spacing, None)
            spacing += 30

    def add_label(self, text, spacing):
        position = pygame.Rect((int(0), int(0) + spacing), (label_width, -1))
        label = UILabel(position, text, self.ui_manager, container=self, anchors=config.ANCHOR_LEFT)

    def add_text_box(self, text, spacing, command):
        if not str(text):
            return
        position = pygame.Rect((int(0) + label_width + 10, int(0) + spacing), (400, -1))
        test_text_entry = UITextEntryLine(position,
                                               self.ui_manager,
                                               container=self)

        test_text_entry.set_text(str(text))

    def handle_events(self, events):
        for window in self.windows:
            window.handle_events(events)

    def update(self, time_delta):
        super().update(time_delta)
        for window in self.windows:
            window.update(time_delta)

    def render(self):
        for window in self.windows:
            window.render()

    def add_key_frames_view(self):
        key_frames = self.element['key_frames']
        position = list(self.position)
        position[1] = position[1] + self.size[1]

        size = list(self.size)
        size[0] = size[0] / 2
        key_frames_view = KeyFramesView(self, key_frames, self.screen, self.ui_manager, position, size)

        self.windows.append(key_frames_view)

    def kill_children(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

    def bubble_events_up(self, events):
        self.parent.bubble_events_up(events)

