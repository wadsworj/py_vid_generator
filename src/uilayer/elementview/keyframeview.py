import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel, UITextBox

from src.config import config
from src.corelayer.helpers.intfloatstringconverter import IntFloatStringConverter
from src.uilayer import customuieventtype
from src.uilayer.controls.jsoneditcontrol import JsonEditControlBuilder
from src.uilayer.customuievent import CustomUIEvent

label_width = 120


class KeyFrameView(UIWindow):
    def __init__(self, parent, key_frame, screen, ui_manager, rect):
        self.parent = parent
        self.ui_manager = ui_manager
        self.key_frame = key_frame
        self.screen = screen
        self.windows = []
        self.json_control_builder = JsonEditControlBuilder(self.ui_manager, self)

        title = ''
        if key_frame:
            title = str(key_frame['second'])

        super().__init__(rect, self.ui_manager,
                         window_display_title=("second: " + title),
                         object_id='#key_frame_window',
                         resizable=True)

        spacing = 0
        self.controls = self.json_control_builder.return_control_collection(self.key_frame, 0, 0, True)
        # for key in self.key_frame:
        #     self.add_label(key, spacing)
        #     self.add_text_box(self.key_frame[key], spacing, None)
        #     spacing += 30

    def handle_events(self, events):
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.controls['save_button']:
                    self.save()

    def update(self, time_delta):
        super().update(time_delta)

    def render(self):
        for window in self.windows:
            window.render()

    def add_text_box(self, text, spacing, command):
        if not str(text):
            return
        position = pygame.Rect((int(0) + label_width + 10, int(0) + spacing), (400, -1))

        test_text_entry = UITextEntryLine(position,
                                          self.ui_manager,
                                          container=self)

        test_text_entry.set_text(str(text))

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

    def save(self):
        for control_key in self.controls:
            if control_key in self.key_frame:
                if isinstance(self.key_frame[control_key], list):
                    for index, x in enumerate(self.controls[control_key]):
                        value = self.controls[control_key][index].text
                        self.key_frame[control_key][index] = IntFloatStringConverter.convert(value)
                else:
                    value = self.controls[control_key].text
                    self.key_frame[control_key] = IntFloatStringConverter.convert(value)

        event = CustomUIEvent(customuieventtype.KEY_FRAME_SAVED, self.key_frame)
        self.bubble_events_up([event])

    def close_all_windows(self):
        for window in self.windows:
            window.kill_children()
            window.kill()

        self.windows = []
