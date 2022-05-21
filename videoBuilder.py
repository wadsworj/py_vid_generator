import pygame

from video import Video


class VideoBuilder:
    def __init__(self):
        pass

    def build(self, data):
        video = Video()
        video.name = data["name"]
        video.resolution = data["resolution"]
        video.screen = pygame.display.set_mode(video.resolution)

        if 'audio' in data:
            video.audio_file = data["audio"]
        video.back_color = data["back_color"]
        return video
