import os
import pygame
from pygame.locals import *

import config


class Video:
    def __init__(self, name, resolution):
        self.name = name
        self.video = None
        self.screen = pygame.display.set_mode(resolution)
        self.scenes = []
        self.current_scene = None
        # self.cam = pygame.camera.Camera("/dev/video0",(640,480))
        # self.cam.start()

    def add_scene(self, scene):
        self.scenes.append(scene)

    def render(self):
        done_capturing = False

        self.current_scene = self.scenes.pop(0)
        clock = pygame.time.Clock()
        while not done_capturing:
            # file_num = file_num + 1
            # image = self.cam.get_image()
            # self.screen.blit(image, (0, 0))
            pygame.display.update()
            self.screen.fill(config.BLACK)

            clock.tick(config.FRAME_RATE)

            # Save every frame
            # filename = "Snaps/%04d.png" % file_num
            # pygame.image.save(image, filename)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done_capturing = True

            if self.current_scene:
                self.current_scene.render(self.screen)

                if self.current_scene.finished:
                    self.current_scene = self.scenes.pop(0)


        # Combine frames to make video
        # os.system("avconv -r 8 -f image2 -i Snaps/%04d.png -y -qscale 0 -s 640x480 -aspect 4:3 result.avi")
