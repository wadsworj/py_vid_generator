import pygame

from src.corelayer.elements.elementBuilder import ElementBuilder
from src.sceneBuilder import SceneBuilder
from src.video import Video
from src.config import config


class VideoBuilder:
    def __init__(self):
        pass

    def build(self, data):
        video = Video()
        video.name = data["name"]
        video.resolution = data["resolution"]

        video.screen = pygame.display.set_mode(video.resolution)

        config.SCREEN_WIDTH = video.resolution[0]
        config.SCREEN_HEIGHT = video.resolution[1]

        if 'audio' in data:
            video.audio_file = data["audio"]

        if 'start_seconds' in data:
            video.start_seconds = data["start_seconds"]

        if 'debug' in data:
            video.debug = data['debug']

        video.back_color = data["back_color"]

        scene_builder = SceneBuilder(ElementBuilder())

        for data_scene in data["scenes"][data["start_scene"]:]:
            scene = scene_builder.build(data_scene)
            video.add_scene(scene)

        return video
