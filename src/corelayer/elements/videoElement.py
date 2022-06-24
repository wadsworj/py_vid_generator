class VideoElement:
    def __init__(self, name):
        self.name = name
        self.video = None
        self.data = None
        self.layer_priority = None

    def render(self):
        self.video.render()
