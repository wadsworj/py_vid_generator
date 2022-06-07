import os
import pygame
import cv2
from src import config
from pygame import mixer
from src.config import config
from src.corelayer.helpers.frametoseconds import FrameToSeconds
from src.uilayer.elementpropertiesview import ElementPropertiesView


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
        self.mouse_click_pos_x = None
        self.mouse_click_pos_y = None
        self.screen_objects = []
        self.done_capturing = False
        self.file_num = 0
        self.frames_since_start = 0
        self.current_scene_start = None
        self.rect_clicked = None
        self.paused = False
        self.paused_frame = None
        self.ui_elements = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def render(self, preview):
        frame = 0
        time_delta = None
        self.play_audio(frame)
        self.current_scene = self.scenes.pop(0)

        clock = pygame.time.Clock()
        self.current_scene_start = pygame.time.get_ticks()

        while not self.done_capturing and self.current_scene:
            pygame.display.update()

            events = pygame.event.get()
            self.handle_events(events)

            time_delta = clock.tick(config.FRAME_RATE)

            frame = self.determine_current_frame(preview, frame)

            if not self.paused:
                self.play_audio(frame + self.frames_since_start)
                self.file_num = self.file_num + 1
                self.save_image_file(self.file_num)

            self.screen.fill(self.back_color)

            if self.debug:
                self.render_debug_info(frame)

            self.screen_objects = []
            self.current_scene.render(self.screen, frame, self.screen_objects)

            for ui_element in self.ui_elements:
                ui_element.render()

            # if the current scene is finished then we need to load the next scene
            if self.current_scene.finished:
                if self.scenes:
                    self.frames_since_start = self.frames_since_start + frame
                    self.current_scene = self.scenes.pop(0)
                    self.current_scene_start = pygame.time.get_ticks()
                else:
                    return

    def handle_mouse_click(self):
        self.mouse_click_pos_x, self.mouse_click_pos_y = pygame.mouse.get_pos()
        rect_clicked = []
        for rect_object in self.screen_objects:
            rect = rect_object[0]
            center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0] / 128,
                                      self.resolution[0] / 128)
            if center_rect.collidepoint(self.mouse_click_pos_x, self.mouse_click_pos_y):
                rect_clicked.append(rect_object)

        return rect_clicked

    def render_debug_info(self, frame):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        seconds = FrameToSeconds.convert_frame_to_seconds(frame)
        text_surface = my_font.render(str(round(frame, 1)) + " frame " + str(round(seconds, 2)) + " seconds", True, config.RED)
        self.screen.blit(text_surface, (0, 0))

        if self.mouse_click_pos_x and self.mouse_click_pos_y:
            mouse_click_text_surface = my_font.render("[" + str(self.mouse_click_pos_x) + "," + str(self.mouse_click_pos_y)
                                                      + "] position", True, config.RED)
            self.screen.blit(mouse_click_text_surface, (text_surface.get_width() + 5, 0))

        if self.rect_clicked:
            for rect_object in self.rect_clicked:
                properties = ElementPropertiesView(rect_object[1], self.screen)
                self.pause_preview()
                properties.update()
                #
                # rect = rect_object[0]
                # pygame.draw.rect(self.screen, (0, 100, 255), rect, 3)  # width = 3
                #
                # if "key_frames" in rect_object[1]:
                #     for key_frame in rect_object[1]["key_frames"]:
                #         if "grid_position" in key_frame:
                #             grid_position_center_rect = pygame.Rect(key_frame["grid_position"][0] * (self.resolution[0] / 16), key_frame["grid_position"][1] * (self.resolution[1] / 9), self.resolution[0] / 128,
                #                                       self.resolution[0] / 128)
                #
                #             pygame.draw.rect(self.screen, config.GREEN, grid_position_center_rect, 3)  # width = 3
        self.rect_clicked = []
        self.render_center_square_each_surface()

    def save_image_file(self, file_num):
        # Save every frame
        filename = os.path.join(config.OUTPUT_LOCATION, config.OUTPUT_FRAMES_LOCATION, "%04d.png" % file_num)
        pygame.image.save(self.screen, filename)

    def save_video_file(self, scene_file_start, scene_file_end):
        image_path = os.path.join(config.OUTPUT_LOCATION, config.OUTPUT_FRAMES_LOCATION)
        images = [img for img in os.listdir(image_path) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_path, images[0]))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(
            config.OUTPUT_VIDEO_LOCATION + str(scene_file_start) + "_" + str(scene_file_end) + ".avi", fourcc, config.FRAME_RATE, (self.resolution[0], self.resolution[1]))

        for image in images[scene_file_start:scene_file_end]:
            video.write(cv2.imread(os.path.join(image_path, image)))

        cv2.destroyAllWindows()
        video.release()

    def play_audio(self, frame):
        # play music if it is configured
        if not self.audio_file or self.playing_audio:
            return

        mixer.init()
        for audio in self.audio_file:
            mixer.music.load(os.path.join(config.RESOURCES_LOCATION, "audio", audio))

            # translate frames to seconds
            frame_second = FrameToSeconds.convert_frame_to_seconds(frame)

            # Start playing the song
            mixer.music.play()
            mixer.music.set_pos(frame_second)
        self.playing_audio = True

    def handle_events(self, events):
        for ui_element in self.ui_elements:
            ui_element.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.done_capturing = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done_capturing = True
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    if self.paused:
                        self.pause_preview()
                elif event.key == pygame.K_LEFT:
                    self.paused_frame = self.paused_frame - FrameToSeconds.convert_frame_to_milliseconds(1)
                elif event.key == pygame.K_PAGEDOWN:
                    self.paused_frame = self.paused_frame - FrameToSeconds.convert_frame_to_milliseconds(10)
                elif event.key == pygame.K_RIGHT:
                    self.paused_frame = self.paused_frame + FrameToSeconds.convert_frame_to_milliseconds(1)
                elif event.key == pygame.K_PAGEUP:
                    self.paused_frame = self.paused_frame + FrameToSeconds.convert_frame_to_milliseconds(10)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.rect_clicked = self.handle_mouse_click()

    def determine_current_frame(self, preview, frame):
        if self.paused:
            self.determine_paused_frame_offset()

        if preview:
            return ((pygame.time.get_ticks() - self.current_scene_start) / 1000) * config.FRAME_RATE
        else:
            return frame + 1

    def determine_paused_frame_offset(self):
        paused_gap = pygame.time.get_ticks() - self.paused_frame
        restart_frame = max((pygame.time.get_ticks() - self.current_scene_start) - paused_gap, 0)
        self.current_scene_start = pygame.time.get_ticks() - restart_frame
        self.paused_frame = pygame.time.get_ticks()

    def render_center_square_each_surface(self):
        for rect_object in self.screen_objects:
            rect = rect_object[0]
            center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0] / 128, self.resolution[0] / 128)
            pygame.draw.rect(self.screen, config.RED, center_rect)  # width = 3

    def pause_preview(self):
        self.paused_frame = pygame.time.get_ticks()
        self.playing_audio = False
        mixer.music.stop()

