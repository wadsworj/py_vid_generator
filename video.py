import os
import pygame
from pygame.locals import *

import config
from pygame import mixer


class Video:
    def __init__(self, name, resolution, audio_file):
        self.name = name
        self.video = None
        self.screen = pygame.display.set_mode(resolution)
        self.scenes = []
        self.current_scene = None
        self.audio_file = audio_file
        self.playing_audio = False

    def add_scene(self, scene):
        self.scenes.append(scene)

    def render(self):
        self.play_audio()

        done_capturing = False

        file_num = 0
        self.current_scene = self.scenes.pop(0)
        clock = pygame.time.Clock()
        while not done_capturing:
            pygame.display.update()

            file_num = file_num + 1
            # Save every frame
            filename = "output/%04d.png" % file_num
            pygame.image.save(self.screen, filename)

            self.screen.fill(config.BLACK)

            clock.tick(config.FRAME_RATE)

            # Save every frame
            # filename = "Snaps/%04d.png" % file_num
            # pygame.image.save(image, filename)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done_capturing = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done_capturing = True

            if self.current_scene:
                self.current_scene.render(self.screen)

                if self.current_scene.finished:
                    if self.scenes:
                        self.current_scene = self.scenes.pop(0)
                    else:
                        return


        # Combine frames to make video
        # os.system("avconv -r 8 -f image2 -i Snaps/%04d.png -y -qscale 0 -s 640x480 -aspect 4:3 result.avi")

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

                # Start playing the song
                mixer.music.play()
                count = count + 1