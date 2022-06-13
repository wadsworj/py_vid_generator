import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

from src.config import config

label_width = 120


class KeyFrameView(UIWindow):
    def __init__(self, parent, key_frame, screen, ui_manager, rect):
        self.parent = parent
        self.ui_manager = ui_manager
        self.key_frame = key_frame
        self.screen = screen
        self.windows = []

        super().__init__(rect, self.ui_manager,
                         window_display_title=("second: " + str(key_frame['second'])),
                         object_id='#key_frame_window',
                         resizable=True)

        spacing = 0
        for key in self.key_frame:
            self.add_label(key, spacing)
            self.add_text_box(self.key_frame[key], spacing, None)
            spacing += 30

    def handle_events(self, events):
        pass

    def update(self, time_delta):
        super().update(time_delta)

    def render(self):
        for window in self.windows:
            window.render()

    def add_text_box(self, text, spacing, command):
        if not str(text):
            return
        position = pygame.Rect((int(0) + label_width + 10, int(0) + spacing), (400, -1))

        test_text_entry = UILabel(position, str(text),
                                  self.ui_manager,
                                  container=self)

        # test_text_entry.text_horiz_alignment = "left"
        # test_text_entry.text_vert_alignment = "left"
        # test_text_entry.rebuild_from_changed_theme_data()

    def kill_children(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

    def add_label(self, text, spacing):
        position = pygame.Rect((int(0), int(0) + spacing), (label_width, -1))
        label = UILabel(position, text, self.ui_manager, container=self)

    def bubble_events_up(self, events):
        self.parent.bubble_events_up(events)

    def bubble_events_down(self, events):
        pass
