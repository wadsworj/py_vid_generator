import pygame
from pygame_gui.elements import UIWindow, UISelectionList

from src.config import config

padding = 100
y_offset = 120


class ElementsView(UIWindow):
    def __init__(self, parent, element, screen, ui_manager):
        self.ui_manager = None
        self.presenter = None

        self.element = element
        self.parent = parent
        self.ui_manager = ui_manager

        x_offset = config.SCREEN_WIDTH - (config.SCREEN_WIDTH / 4)
        size_x = config.SCREEN_WIDTH / 4
        size_y = config.SCREEN_HEIGHT / 3
        self.position = [x_offset, y_offset]
        self.size = [size_x, size_y]

        title = "scene_elements"

        super().__init__(pygame.Rect(self.position, self.size), self.ui_manager,
                         window_display_title=title,
                         object_id='#pong_window',
                         resizable=True)

        elements = self.build_elements_list()

        selection_list_size = [self.size[0] / 1.2, self.size[1] / 1.2]

        self.test_drop_down_menu = UISelectionList(pygame.Rect(10, 10, selection_list_size[0], selection_list_size[1]),
                                                   item_list=elements,
                                                   manager=self.ui_manager,
                                                   container=self)

    def build_elements_list(self):
        elements = []
        count = 0
        for scene in self.element['scenes']:
            for element in scene['elements']:
                text = str(count)
                if 'name' in element:
                    text = element['name']
                elif 'text' in element:
                    text = element['text']
                elements.append(text)
                count = count + 1

        return elements
