import pygame
from pygame_gui.elements import UIWindow, UITextEntryLine, UISelectionList, UILabel, UIButton

padding = 100
x_offset = 120
y_offset = 120

control_height = 30
label_width = 100
textbox_width = 150
sub_textbox_width = textbox_width / 2


class JsonEditControlBuilder:
    def __init__(self, ui_manager, container):
        self.y_spacing = 0
        self.ui_manager = ui_manager
        self.container = container

    def return_control_collection(self,
                                  json_dict,
                                  x_offset: 0,
                                  y_offset: 0,
                                  add_save_button: False,
                                  add_delete_button: False,
                                  elements_to_skip: []):

        control_collection = self.create_control_collection(json_dict, elements_to_skip)

        if add_save_button:
            save_button = self.add_save_button()
            control_collection['save_button'] = save_button

        if add_delete_button:
            delete_button = self.add_delete_button()
            control_collection['delete_button'] = delete_button

        return control_collection

    def create_control_collection(self, json_dict, elements_to_skip):
        control_collection = {}

        for key in json_dict:
            if key in elements_to_skip:
                continue

            element = json_dict[key]
            self.add_label(str(key), self.y_spacing)

            # add sub elements
            if isinstance(element, list):
                control_collection[key] = []
                index = 0
                x_spacing = 0
                for sub_element in element:
                    text_box = self.create_text_box(x_spacing, sub_textbox_width)
                    text_box.set_text(str(sub_element))
                    control_collection[key].append(text_box)
                    index = index + 1
                    x_spacing = x_spacing + sub_textbox_width + 10
                self.y_spacing = self.y_spacing + control_height + 10

            else:
                text_box = self.create_text_box(0, textbox_width)
                text_box.set_text(str(element))
                control_collection[key] = text_box
                self.y_spacing = self.y_spacing + control_height + 10

        return control_collection

    def add_label(self, text, spacing):
        position = pygame.Rect((int(0), int(0) + spacing), (label_width, -1))
        label = UILabel(position, text, self.ui_manager, container=self.container)

    def create_text_box(self, x_spacing, width):
        position = pygame.Rect((int(0) + label_width + 10 + x_spacing, int(0) + self.y_spacing), (width, control_height))

        test_text_entry = UITextEntryLine(position,
                                          self.ui_manager,
                                          container=self.container)
        return test_text_entry

    def add_save_button(self):
        position = pygame.Rect((int(0), int(0) + self.y_spacing), (label_width, control_height))
        return UIButton(position, "Save", self.ui_manager, self.container, object_id="#save_button")

    def add_delete_button(self):
        position = pygame.Rect((label_width + int(10), int(0) + self.y_spacing), (label_width, control_height))
        return UIButton(position, "Delete", self.ui_manager, self.container, object_id="#save_button")
