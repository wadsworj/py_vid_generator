import math
from os.path import exists

import pygame

import config


class AnimatedTextElement:
    def __init__(self):
        self.name = None
        self.text = None
        self.count = 0
        self.font_size = None
        self.font_type = None
        self.font_color = config.WHITE
        self.text_align = None
        self.start_time = None
        self.key_frames = None

    # https://stackoverflow.com/questions/46732939/how-to-interpolate-2-d-points-between-two-timesteps
    def interpolate(self, t, time_1, time_2, point_1, point_2):
        if t <= time_1:
            return point_1

        if time_1 == time_2:
            return point_1

        dt = (t - time_1) / (time_2 - time_1)
        returned_points = []

        for i in range(len(point_1)):
            interpolated_point = point_2[i] - point_1[i]
            returned_points.append(dt * interpolated_point + point_1[i])

        return returned_points

    def render(self, screen, scene_seconds):
        key_frames = self.get_previous_current_frames(scene_seconds)

        lines = self.text.splitlines()
        length = len(self.text)

        screen_rect = screen.get_rect()
        previous_position_scaled = [key_frames[0]["grid_position"][0] * (screen_rect.width / 16), key_frames[0]["grid_position"][1] * (screen_rect.height / 9)]
        next_position_scaled = [key_frames[1]["grid_position"][0] * (screen_rect.width / 16), key_frames[1]["grid_position"][1] * (screen_rect.height / 9)]

        current_position = self.interpolate(scene_seconds,
                                            key_frames[0]["second"],
                                            key_frames[1]["second"],
                                            previous_position_scaled,
                                            next_position_scaled)

        if "opacity" in key_frames[1]:
            current_opacity = self.interpolate(scene_seconds,
                                               key_frames[0]["second"],
                                               key_frames[1]["second"],
                                               [key_frames[0]["opacity"]],
                                               [key_frames[1]["opacity"]])[0]
        else:
            current_opacity = 1

        line_count = 0
        for line in lines:
            font_exists = exists("fonts/" + self.font_type + ".ttf")

            if font_exists:
                my_font = pygame.font.Font("fonts/" + self.font_type + ".ttf", self.font_size)
            else:
                my_font = pygame.font.SysFont(self.font_type, self.font_size)

            text_position = pygame.Rect(current_position[0], current_position[1], screen_rect.width, screen_rect.height)
            text_surface = my_font.render(line, True, self.font_color)
            text_surface.set_alpha(int(255 * current_opacity))
            screen.blit(text_surface, (text_position.left, (text_position.top + (line_count * self.font_size))))
            line_count = line_count + 1

    def get_previous_current_frames(self, scene_seconds):
        previous_key_frame = None
        next_key_frame = None
        for key_frame in self.key_frames:
            if scene_seconds >= key_frame["second"] or not previous_key_frame:
                previous_key_frame = key_frame
            elif not next_key_frame and scene_seconds <= key_frame["second"]:
                next_key_frame = key_frame

        # if done next animation then set to previous
        if not next_key_frame:
            next_key_frame = previous_key_frame

        return [previous_key_frame, next_key_frame]
