import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel, UIButton

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

        selection_list_size = [self.size[0] / 2, self.size[1] / 2]

        self.test_drop_down_menu = UISelectionList(pygame.Rect(10, 10, selection_list_size[0], selection_list_size[1]),
                                                   item_list=frames,
                                                   manager=self.ui_manager,
                                                   container=self)

        button_padding = 5
        button_spacing = 0
        button_height = 30
        self.add_new_button = UIButton(pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Add New",
                                       manager=self.ui_manager,
                                       container=self)
        button_spacing = button_spacing + button_padding + button_height
        self.delete_button = UIButton(
            pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Delete",
            manager=self.ui_manager,
            container=self)

        button_spacing = button_spacing + button_padding + button_height
        self.duplicate_button = UIButton(
            pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Duplicate",
            manager=self.ui_manager,
            container=self)

        # self.test_drop_down_menu.

    def handle_events(self, events):
        for window in self.windows:
            window.handle_events(events)

        for event in events:
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                self.handle_key_frame_click(event.text)

    def update(self, time_delta):
        super().update(time_delta)

    def render(self):
        for window in self.windows:
            window.render()

    def handle_key_frame_click(self, text):
        key_frame_found = [x for x in self.key_frames if text == str(x["second"])]

        if key_frame_found and len(key_frame_found) > 0:
            key_frame = key_frame_found[0]
        else:
            return

        self.add_key_frame_view(key_frame)

    def add_key_frame_view(self, key_frame):
        if self.selected_key_frame_view:
            rect = self.selected_key_frame_view.rect
            self.selected_key_frame_view.kill()
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

    def bubble_events_up(self, events: list[CustomUIEvent]):
        self.parent.bubble_events_up(events)

    def bubble_events_down(self, events: list[CustomUIEvent]):
        for window in self.windows:
            window.bubble_events_down(events)

        for event in events:
            if event.event_type == customuieventtype.KEY_FRAME_CLICKED:
                # self.test_drop_down_menu.sel
                self.add_key_frame_view(event.data)
