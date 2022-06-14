import pygame
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel

padding = 100
x_offset = 120
y_offset = 120

control_height = 30
label_width = 100
textbox_width = 150
sub_textbox_width = textbox_width / 2


class JsonEditControl():
    @staticmethod
    def return_control_collection(ui_manager, container, json_dict, x_offset: 0, y_offset: 0):
        control_collection = {}
        y_spacing = 0

        for key in json_dict:
            element = json_dict[key]

            JsonEditControl.add_label(ui_manager, container, str(key), y_spacing)

            # add sub elements
            if isinstance(element, list):
                control_collection[key] = []
                index = 0
                x_spacing = 0
                for sub_element in element:
                    text_box = JsonEditControl.create_text_box(ui_manager, container, y_spacing, x_spacing, sub_textbox_width)
                    text_box.set_text(str(sub_element))
                    control_collection[key].append(text_box)
                    index = index + 1
                    x_spacing = x_spacing + sub_textbox_width + 10

                y_spacing = y_spacing + control_height + 10

            else:
                text_box = JsonEditControl.create_text_box(ui_manager, container, y_spacing, 0, textbox_width)
                text_box.set_text(str(element))
                control_collection[key] = text_box
                y_spacing = y_spacing + control_height + 10

    @staticmethod
    def add_label(ui_manager, container, text, spacing):
        position = pygame.Rect((int(0), int(0) + spacing), (label_width, -1))
        label = UILabel(position, text, ui_manager, container=container)

    @staticmethod
    def create_text_box(ui_manager, container, y_spacing, x_spacing, width):
        position = pygame.Rect((int(0) + label_width + 10 + x_spacing, int(0) + y_spacing), (width, control_height))

        test_text_entry = UITextEntryLine(position,
                                          ui_manager,
                                          container=container)

        return test_text_entry
