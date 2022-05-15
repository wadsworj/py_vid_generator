class VideoElement:
    def __init__(self, name):
        self.name = name
        self.video = None

    def render(self):
        self.video.render()
