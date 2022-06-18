import pygame

from src.config import config
from src.uilayer.controls.dragoperator import DragOperator


class KeyFrameCenter(pygame.sprite.Sprite):
    def __init__(self, spriteName, x, y, x_size, y_size):
        super().__init__()

        circle_radius = x_size / 2
        # self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)

        # self.original_image = pygame.Rect(float(x),
        #                                         float(y),
        #                                         x_size,
        #                                         y_size)

        self.original_image = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, config.BLUE, (circle_radius, circle_radius), circle_radius)

        self.drag_image = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.drag_image, config.GREEN, (circle_radius, circle_radius), circle_radius)
        pygame.draw.circle(self.drag_image, (255, 255, 255), (circle_radius, circle_radius), 25, 4)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x + (x_size / 2), y + (x_size / 2)))
        self.drag = DragOperator(self)
        # pygame.draw.rect(self.screen, color, grid_position_center_rect, 3)  # width = 3

    def update(self, event_list):
        self.drag.update(event_list)
        self.image = self.drag_image if self.drag.dragging else self.original_image
