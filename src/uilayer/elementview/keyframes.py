import pygame
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

from src.config import config

class KeyFramesView(UIWindow):
    def __init__(self, key_frames, screen, ui_manager, position, size):
        self.ui_manager = ui_manager
        self.key_frames = key_frames
        self.screen = screen

        self.position = position
        self.size = size

        frames = []
        for keyframe in key_frames:
            frames.append(str(keyframe['second']))

        super().__init__(pygame.Rect(self.position, self.size), self.ui_manager,
                         window_display_title="Key Frames",
                         object_id='#key_frame_window',
                         resizable=True)

        self.test_drop_down_menu = UISelectionList(pygame.Rect(10, 10, self.size[0] - 10, self.size[1] - 10),
                                                 item_list=frames,
                                                 manager=self.ui_manager,
                                                 container=self)






