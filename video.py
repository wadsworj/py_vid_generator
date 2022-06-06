import os
import pygame
from pygame.locals import *
import cv2
import config
from pygame import mixer


class Video:
    def __init__(self):
        self.name = None
        self.video = None
        self.resolution = None
        self.screen = None
        self.scenes = []
        self.current_scene = None
        self.audio_file = None
        self.playing_audio = False
        self.back_color = None
        self.debug = False
        self.start_seconds = 0
        self.mouse_click_pos_x = None
        self.mouse_click_pos_y = None
        self.screen_objects = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def render(self):
        self.play_audio()

        done_capturing = False

        file_num = 0
        scene_file_start = 1
        self.current_scene = self.scenes.pop(0)
        clock = pygame.time.Clock()
        paused = False
        rect_clicked = None

        while not done_capturing:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done_capturing = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done_capturing = True
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                        if not paused:
                            self.play_audio()
                        else:
                            self.playing_audio = False
                            mixer.music.stop()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_click_pos_x, self.mouse_click_pos_y = pygame.mouse.get_pos()
                    clicked_rect = pygame.Rect(self.mouse_click_pos_x, self.mouse_click_pos_y, 1, 1)
                    rect_clicked = []
                    for rect_object in self.screen_objects:
                        rect = rect_object[0]
                        center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0] / 128,
                                                  self.resolution[0] / 128)
                        if center_rect.collidepoint(self.mouse_click_pos_x, self.mouse_click_pos_y):
                            rect_clicked.append(rect_object)

            clock.tick(config.FRAME_RATE)

            if paused:
                if self.debug:
                    self.render_debug_info(rect_clicked)

                self.start_seconds = self.start_seconds - (1 / config.FRAME_RATE)
                continue

            file_num = file_num + 1
            # Save every frame
            filename = "output/%04d.png" % file_num
            pygame.image.save(self.screen, filename)

            self.screen.fill(self.back_color)

            if self.current_scene:
                if self.debug:
                    self.render_debug_info(rect_clicked)

                self.screen_objects = []
                self.current_scene.render(self.screen, self.start_seconds, self.screen_objects)

                if self.current_scene.finished:
                    # self.save_video_file(scene_file_start, file_num)
                    # scene_file_start = file_num + 1

                    if self.scenes:
                        self.current_scene = self.scenes.pop(0)
                        self.start_seconds = 0
                    else:
                        return

    def render_debug_info(self, rect_clicked):
        video_time = pygame.time.get_ticks()
        seconds = round(((video_time / 1000) % 60) + self.start_seconds, 2)

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(str(seconds) + " seconds", True, config.RED)
        self.screen.blit(text_surface, (0, 0))

        if self.mouse_click_pos_x and self.mouse_click_pos_y:
            mouse_click_text_surface = my_font.render("[" + str(self.mouse_click_pos_x) + "," + str(self.mouse_click_pos_y)
                                                      + "] position", True, config.RED)
            self.screen.blit(mouse_click_text_surface, (text_surface.get_width() + 5, 0))

        if rect_clicked:
            for rect_object in rect_clicked:
                rect = rect_object[0]
                pygame.draw.rect(self.screen, (0, 100, 255), rect, 3)  # width = 3

                if "key_frames" in rect_object[1]:
                    for key_frame in rect_object[1]["key_frames"]:
                        if "grid_position" in key_frame:
                            grid_position_center_rect = pygame.Rect(key_frame["grid_position"][0] * (self.resolution[0] / 16), key_frame["grid_position"][1] * (self.resolution[1] / 9), self.resolution[0] / 128,
                                                      self.resolution[0] / 128)

                            pygame.draw.rect(self.screen, config.GREEN, grid_position_center_rect, 3)  # width = 3

                count = 0
                for x in rect_object[1]:
                    count = count + 2
                    text_surface = my_font.render(str(x), True, config.GREEN)
                    self.screen.blit(text_surface, (0, text_surface.get_height() * count))
                    if isinstance(rect_object[1][x], list):
                        for y in rect_object[1][x]:
                            count = count + 1
                            text_surface = my_font.render(str(y), True, config.GREEN)
                            self.screen.blit(text_surface, ((self.resolution[0]/8), text_surface.get_height() * count))
                    else:
                        count = count + 1
                        text_surface = my_font.render(str(rect_object[1][x]), True, config.GREEN)
                        self.screen.blit(text_surface, (self.resolution[0]/8, text_surface.get_height() * count))

        # render the center square for each surface
        for rect_object in self.screen_objects:
            rect = rect_object[0]
            center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0]/128, self.resolution[0]/128)
            pygame.draw.rect(self.screen, config.RED, center_rect)  # width = 3



    def save_video_file(self, scene_file_start, scene_file_end):
        images = [img for img in os.listdir("output") if img.endswith(".png")]
        frame = cv2.imread(os.path.join("output", images[0]))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter("output_video/" + str(scene_file_start) + "_" + str(scene_file_end) + ".avi", fourcc, config.FRAME_RATE, (self.resolution[0], self.resolution[1]))

        for image in images[scene_file_start:scene_file_end]:
            video.write(cv2.imread(os.path.join("output", image)))

        cv2.destroyAllWindows()
        video.release()

    def play_audio(self):
        # play music if it is configured
        if self.audio_file and not self.playing_audio:
            count = 0
            mixer.init()
            for audio in self.audio_file:
                mixer.music.load("audio/" + audio)
                # Setting the volume
                if count > 0:
                    mixer.music.set_volume(0.5)

                video_time = pygame.time.get_ticks()
                seconds = ((video_time / 1000) % 60) + self.start_seconds

                # Start playing the song
                mixer.music.play()
                mixer.music.set_pos(seconds)
                count = count + 1