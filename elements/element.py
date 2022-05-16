def abstract(args):
    pass


class Element:
    def __init__(self, name):
        self.name = name
        self.scenes = []

    @abstract
    def render(self, scene_seconds):
        pass
