import json
import os
import pygame
import cv2
import pygame_gui
from pygame_gui.elements import UIWindow

from src import config
from pygame import mixer
from src.config import config
from src.corelayer.helpers.frametoseconds import FrameToSeconds
from src.uilayer import customuievent, customuieventtype
from src.uilayer.customuievent import CustomUIEvent
from src.uilayer.elementview.elementpropertiesview import ElementPropertiesView


class Video:
    def __init__(self):
        self.name = None
        self.video = None
        self.data = None
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
        self.ui_windows: list[UIWindow] = []
        self.ui_manager = None
        self.selected_key_frame = None
        self.visible_key_frames = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def save_data_file(self):
        json_string = json.dumps(self.data)
        # Directly from dictionary
        path = os.path.join(config.OUTPUT_LOCATION, config.OUTPUT_DATA_LOCATION, str(self.name) + '.json')
        with open(path, 'w') as outfile:
            json.dump(self.data, outfile, indent=4, sort_keys=True)

    def render(self, preview):
        frame = 0
        time_delta = None
        self.current_scene = self.scenes.pop(0)

        clock = pygame.time.Clock()
        self.current_scene_start = pygame.time.get_ticks() - (self.start_seconds * 1000)

        while not self.done_capturing and self.current_scene:
            time_delta = clock.tick(config.FRAME_RATE)

            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)

            pygame.display.update()

            events = pygame.event.get()
            self.handle_events(events)

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

            for ui_window in self.ui_windows:
                ui_window.render()

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

        for visible_key_frame in self.visible_key_frames:
            rect = pygame.Rect(visible_key_frame["grid_position"][0] * (self.resolution[0] / 16),
                               visible_key_frame["grid_position"][1] * (self.resolution[1] / 9),
                               self.resolution[0] / 128,
                               self.resolution[0] / 128)

            # center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0] / 128,
            #                           self.resolution[0] / 128)

            if rect.collidepoint(self.mouse_click_pos_x, self.mouse_click_pos_y):
                event = CustomUIEvent(customuieventtype.KEY_FRAME_CLICKED, visible_key_frame)
                self.bubble_events_down([event])

        rect_clicked = []
        for rect_object in self.screen_objects:
            rect = rect_object[0]
            center_rect = pygame.Rect(rect.centerx, rect.centery, self.resolution[0] / 128,
                                      self.resolution[0] / 128)

            if center_rect.collidepoint(self.mouse_click_pos_x, self.mouse_click_pos_y):
                rect_clicked.append(rect_object)
                properties = ElementPropertiesView(self, rect_object[1], self.screen, self.ui_manager)
                self.pause_preview()
                self.close_all_windows()
                self.ui_windows.append(properties)
                break

        return rect_clicked

    def render_debug_info(self, frame):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        seconds = FrameToSeconds.convert_frame_to_seconds(frame)
        text_surface = my_font.render(str(round(frame, 1)) + " frame " + str(round(seconds, 2)) + " seconds", True,
                                      config.RED)
        self.screen.blit(text_surface, (0, 0))

        if self.mouse_click_pos_x and self.mouse_click_pos_y:
            mouse_click_text_surface = my_font.render(
                "[" + str(self.mouse_click_pos_x) + "," + str(self.mouse_click_pos_y)
                + "] position", True, config.RED)
            self.screen.blit(mouse_click_text_surface, (text_surface.get_width() + 5, 0))

        if self.rect_clicked:
            for rect_object in self.rect_clicked:
                rect = rect_object[0]
                pygame.draw.rect(self.screen, (0, 100, 255), rect, 3)  # width = 3

                if "key_frames" in rect_object[1]:
                    self.visible_key_frames = []
                    for key_frame in rect_object[1]["key_frames"]:
                        self.render_key_frame_center(key_frame, config.BLUE)
                        self.visible_key_frames.append(key_frame)

        if self.selected_key_frame:
            self.render_key_frame_center(self.selected_key_frame, config.GREEN)

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
            config.OUTPUT_VIDEO_LOCATION + str(scene_file_start) + "_" + str(scene_file_end) + ".avi", fourcc,
            config.FRAME_RATE, (self.resolution[0], self.resolution[1]))

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
            if not audio:
                continue

            audio_location = os.path.join(config.RESOURCES_LOCATION, "audio", audio)
            if not os.path.exists(audio_location):
                continue

            mixer.music.load(audio_location)

            # translate frames to seconds
            frame_second = FrameToSeconds.convert_frame_to_seconds(frame)
            mixer.music.set_volume(0.3)
            # Start playing the song
            mixer.music.play()
            mixer.music.set_pos(frame_second)
        self.playing_audio = True

    def handle_events(self, events):
        for ui_window in self.ui_windows:
            ui_window.handle_events(events)

        for event in events:
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                self.done_capturing = True
            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                if event.ui_element in self.ui_windows:
                    self.ui_windows.remove(event.ui_element)
                    event.ui_element.close_all_windows()
                    event.ui_element.kill()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.ui_windows and len(self.ui_windows) > 0:
                        self.close_all_windows()
                    else:
                        self.done_capturing = True

                elif event.key == pygame.K_SPACE:
                    self.handle_space_pressed()
                elif event.key == pygame.K_LEFT:
                    self.paused_frame = self.paused_frame - FrameToSeconds.convert_frame_to_milliseconds(1)
                elif event.key == pygame.K_PAGEDOWN:
                    self.paused_frame = self.paused_frame - FrameToSeconds.convert_frame_to_milliseconds(10)
                elif event.key == pygame.K_RIGHT:
                    self.paused_frame = self.paused_frame + FrameToSeconds.convert_frame_to_milliseconds(1)
                elif event.key == pygame.K_PAGEUP:
                    self.paused_frame = self.paused_frame + FrameToSeconds.convert_frame_to_milliseconds(10)

            elif event.type == pygame.MOUSEBUTTONUP:
                new_rect_clicked = self.handle_mouse_click()
                if new_rect_clicked:
                    self.rect_clicked = new_rect_clicked

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
        self.paused = True
        self.paused_frame = pygame.time.get_ticks()
        self.playing_audio = False
        mixer.music.stop()

    def handle_space_pressed(self):
        if self.ui_windows and len(self.ui_windows) > 0:
            return

        self.paused = not self.paused
        if self.paused:
            self.pause_preview()

    def close_all_windows(self):
        for ui_window in self.ui_windows:
            ui_window.kill_children()
            ui_window.kill()

        self.ui_windows = []

    def bubble_events_down(self, events: list[CustomUIEvent]):
        for window in self.ui_windows:
            window.bubble_events_down(events)

    def bubble_events_up(self, events: list[CustomUIEvent]):
        for event in events:
            if event.event_type == customuieventtype.KEY_FRAME_CLICKED:
                self.selected_key_frame = event.data

    def render_key_frame_center(self, key_frame, color):
        if not "grid_position" in key_frame:
            return

        grid_position_center_rect = pygame.Rect(float(key_frame["grid_position"][0]) * (self.resolution[0] / 16),
                                                float(key_frame["grid_position"][1]) * (self.resolution[1] / 9),
                                                self.resolution[0] / 128,
                                                self.resolution[0] / 128)

        pygame.draw.rect(self.screen, color, grid_position_center_rect, 3)  # width = 3
