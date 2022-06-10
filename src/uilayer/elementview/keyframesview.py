import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

from src.config import config
from src.uilayer import customuieventtype
from src.uilayer.customuievent import CustomUIEvent
from src.uilayer.elementview.keyframeview import KeyFrameView


class KeyFramesView(UIWindow):
    def __init__(self, parent, key_frames, screen, ui_manager, position, size):
        self.parent = parent
        self.ui_manager = ui_manager
        self.key_frames = key_frames
        self.screen = screen
        self.key_frame_view = None
        self.position = position
        self.size = size
        self.windows = []
        self.selected_key_frame_view: UIWindow = None
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

    def handle_events(self, events):
        for window in self.windows:
            window.handle_events(events)

        for event in events:
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                self.add_key_frame_view(event.text)

    def update(self, time_delta):
        super().update(time_delta)

    def render(self):
        for window in self.windows:
            window.render()

    def add_key_frame_view(self, text):
        if self.selected_key_frame_view:
            self.selected_key_frame_view.kill()

        key_frame_found = [x for x in self.key_frames if text == str(x["second"])]

        if key_frame_found and len(key_frame_found) > 0:
            key_frame = key_frame_found[0]
        else:
            return

        if self.selected_key_frame_view:
            rect = self.selected_key_frame_view.rect
        else:
            position = list(self.position)
            position[0] = position[0] + (self.size[0])
            size = list(self.size)
            rect = pygame.Rect(position, size)

        self.selected_key_frame_view = KeyFrameView(self, key_frame, self.screen, self.ui_manager, rect)

        event = CustomUIEvent(customuieventtype.KEY_FRAME_CLICKED, key_frame)
        self.bubble_events_up([event])

        self.windows.append(self.selected_key_frame_view)

    def kill_children(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

    def bubble_events_up(self, events):
        self.parent.bubble_events_up(events)






