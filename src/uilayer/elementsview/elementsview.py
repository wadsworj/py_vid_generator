import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UISelectionList, UIButton

from src.config import config
from src.scene import Scene
from src.uilayer.elementsview.elementsviewpresenter import ElementsViewPresenter

padding = 100
y_offset = 120


class ElementsView(UIWindow):
    def __init__(self, parent, element, screen, ui_manager):
        self.ui_manager = None
        self.presenter: ElementsViewPresenter = None

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

        # elements = self.build_elements_list()
        elements = []

        selection_list_size = [self.size[0] / 2, self.size[1] / 1.2]

        self.test_drop_down_menu = UISelectionList(pygame.Rect(10, 10, selection_list_size[0], selection_list_size[1]),
                                                   item_list=elements,
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
        # for window in self.windows:
        #     window.handle_events(events)

        for event in events:
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.test_drop_down_menu:
                self.presenter.handle_element_click(event.text)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.delete_button:
                    self.handle_delete_button_click()
                elif event.ui_element == self.add_new_button:
                    self.handle_add_new_button_click()
                elif event.ui_element == self.duplicate_button:
                    self.handle_duplicate_button_click()

    def set_scene(self, scene_index):
        self.presenter.set_scene(scene_index)
        self.set_display_title("elements - scene: " + str(scene_index))

    def set_elements(self, elements):
        self.test_drop_down_menu.set_item_list(elements)

    def handle_delete_button_click(self):
        pass

    def handle_add_new_button_click(self):
        pass

    def handle_duplicate_button_click(self):
        self.presenter.duplicate_selected_element()

    def bubble_events_up(self, events):
        self.parent.bubble_events_up(events)

    def bubble_events_down(self, events):
        pass

    def selected_element(self):
        return self.test_drop_down_menu.get_single_selection()
