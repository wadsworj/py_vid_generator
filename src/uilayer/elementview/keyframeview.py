import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

from src.config import config

class KeyFrameView(UIWindow):
    def __init__(self, key_frame, screen, ui_manager, rect):
        self.ui_manager = ui_manager
        self.key_frame = key_frame
        self.screen = screen
        self.windows = []

        frames = []
        # for keyframe in key_frame:
        #     frames.append(str(keyframe['second']))

        super().__init__(rect, self.ui_manager,
                         window_display_title= ("second: " + str(key_frame['second'])),
                         object_id='#key_frame_window',
                         resizable=True)

        # self.test_drop_down_menu = UISelectionList(pygame.Rect(10, 10, self.size[0] - 10, self.size[1] - 10),
        #                                          item_list=frames,
        #                                          manager=self.ui_manager,
        #                                          container=self)

    def handle_events(self, events):
        pass

    def update(self, time_delta):
        super().update(time_delta)
        # for event in pygame.event.get():
        #     if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
        #         self.running = False

    def render(self):
        for window in self.windows:
            window.render()
