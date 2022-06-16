import copy

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

        frames = self.build_frames_list()

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
        self.add_new_button = UIButton(
            pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Add New",
            manager=self.ui_manager,
            container=self,
            object_id='#add_new_button')

        button_spacing = button_spacing + button_padding + button_height
        self.delete_button = UIButton(
            pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Delete",
            manager=self.ui_manager,
            container=self,
            object_id='#delete_button')

        button_spacing = button_spacing + button_padding + button_height
        self.duplicate_button = UIButton(
            pygame.Rect(selection_list_size[0] + 20, 10 + button_spacing, 150, button_height), "Duplicate",
            manager=self.ui_manager,
            container=self,
            object_id='#duplicate_button')

    def handle_events(self, events):
        for window in self.windows:
            window.handle_events(events)

        for event in events:
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                self.handle_key_frame_click(event.text)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.delete_button:
                    self.handle_delete_button_click()
                elif event.ui_element == self.add_new_button:
                    self.handle_add_new_button_click()
                elif event.ui_element == self.duplicate_button:
                    self.handle_duplicate_button_click()

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

        if key_frame:
            event = CustomUIEvent(customuieventtype.KEY_FRAME_CLICKED, key_frame)
            self.bubble_events_up([event])

        self.windows.append(self.selected_key_frame_view)

    def kill_children(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

    def bubble_events_up(self, events: list[CustomUIEvent]):
        for event in events:
            if event.event_type == customuieventtype.KEY_FRAME_SAVED:
                self.save_key_frame(event.data)

        self.parent.bubble_events_up(events)

    def bubble_events_down(self, events: list[CustomUIEvent]):
        for window in self.windows:
            window.bubble_events_down(events)

        for event in events:
            if event.event_type == customuieventtype.KEY_FRAME_CLICKED:
                self.add_key_frame_view(event.data)

    def handle_delete_button_click(self):
        key_frame_to_remove = self.get_selected_key_frame()

        if key_frame_to_remove:
            self.key_frames.remove(key_frame_to_remove)
            self.update_key_frames_list()

    def handle_duplicate_button_click(self):
        selected_key_frame = self.get_selected_key_frame()

        if selected_key_frame:
            self.key_frames.append(selected_key_frame)
            self.update_key_frames_list()

    def handle_add_new_button_click(self):
        self.add_key_frame_view(copy.deepcopy(config.KEY_FRAME_EMPTY))

    def get_selected_key_frame(self):
        selected_key_frame_key = self.test_drop_down_menu.get_single_selection()
        if not selected_key_frame_key:
            return None

        for key_frame in self.key_frames:
            if str(key_frame['second']) == selected_key_frame_key:
                return key_frame

    def update_key_frames_list(self):
        frames = self.build_frames_list()
        self.test_drop_down_menu.set_item_list(frames)

    def build_frames_list(self):
        frames = []
        for keyframe in self.key_frames:
            frames.append(str(keyframe['second']))
        return frames

    def save_key_frame(self, data):
        if not data['second']:
            return

        key_frame_found = [x for x in self.key_frames if str(data['second']) == str(x["second"])]
        if key_frame_found:
            return

        self.key_frames.append(data)
        self.key_frames = sorted(self.key_frames, key=lambda kv: kv['second'])
        self.update_key_frames_list()

    def close_all_windows(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

        self.windows = []
