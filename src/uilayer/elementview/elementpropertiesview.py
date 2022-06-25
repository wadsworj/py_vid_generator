import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel, UIButton

from src.config import config
from src.corelayer.helpers.intfloatstringconverter import IntFloatStringConverter
from src.uilayer import customuieventtype
from src.uilayer.controls.jsoneditcontrol import JsonEditControlBuilder
from src.uilayer.customuievent import CustomUIEvent
from src.uilayer.elementview.keyframesview import KeyFramesView

padding = 100
x_offset = 120
y_offset = 120

label_width = 100


class ElementPropertiesView(UIWindow):
    def __init__(self, parent, element, screen, ui_manager):
        self.parent = parent
        self.ui_manager = ui_manager
        self.json_control_builder = JsonEditControlBuilder(self.ui_manager, self)

        size_x = config.SCREEN_WIDTH / 2
        size_y = int(config.SCREEN_HEIGHT / 2.2)
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

        for base_key in config.ELEMENT_EMPTY:
            if base_key not in self.element:
                self.element[base_key] = config.ELEMENT_EMPTY[base_key]

        self.screen = screen
        self.windows = []
        spacing = 0
        button_height = 30
        button_width = 150
        button_spacing = 10

        self.controls = self.json_control_builder.return_control_collection(self.element,
                                                                            0,
                                                                            0,
                                                                            True,
                                                                            True,
                                                                            ['key_frames'])

        if 'key_frames' in self.element:
            self.add_key_frames_view()

        # spacing = spacing + 10

        # self.save_button = UIButton(
        #     pygame.Rect(button_spacing, spacing, button_width, button_height), "Save",
        #     manager=self.ui_manager,
        #     container=self,
        #     object_id='#save_button')
        #
        # button_spacing = button_spacing + button_width + 10
        #
        # self.delete_button = UIButton(
        #     pygame.Rect(button_spacing, spacing, button_width, button_height), "Delete",
        #     manager=self.ui_manager,
        #     container=self,
        #     object_id='#delete_button')
        #
        # button_spacing = button_spacing + button_width + 10
        #
        # self.duplicate_button = UIButton(
        #     pygame.Rect(button_spacing, spacing, button_width, button_height), "Duplicate",
        #     manager=self.ui_manager,
        #     container=self,
        #     object_id='#duplicate_button')

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
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.controls['save_button']:
                    self.save()

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
        size[1] = int(size[1] * 1.5)
        key_frames_view = KeyFramesView(self, key_frames, self.screen, self.ui_manager, position, size)

        self.windows.append(key_frames_view)

    def close_all_windows(self):
        for window in self.windows:
            window.close_all_windows()
            window.kill()

    def bubble_events_up(self, events):
        self.parent.bubble_events_up(events)

    def bubble_events_down(self, events):
        for window in self.windows:
            window.bubble_events_down(events)

    def save(self):
        for control_key in self.controls:
            if control_key in self.element:
                if isinstance(self.element[control_key], list):
                    for index, x in enumerate(self.controls[control_key]):
                        value = self.controls[control_key][index].text
                        self.element[control_key][index] = IntFloatStringConverter.convert(value)
                else:
                    value = self.controls[control_key].text
                    self.element[control_key] = IntFloatStringConverter.convert(value)

        event = CustomUIEvent(customuieventtype.ELEMENT_SAVED, self.element)
        self.bubble_events_up([event])
