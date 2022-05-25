from elements.animatedElement import AnimatedTextElement
from elements.imageElement import ImageElement
from elements.textElement import TextElement


class ElementBuilder:
    def __init__(self):
        pass

    def build(self, data):
        if data["type"] == "TEXT":
            return self.build_text_element(data)
        elif data["type"] == "ANIMATED_TEXT":
            return self.build_animated_text_element(data)
        elif data["type"] == "IMAGE":
            return self.build_image_element(data)

    def build_image_element(self, data):
        element = ImageElement()
        element.image_string = data["image"]

        if 'position' in data:
            element.position = data["position"]

        if 'key_frames' in data:
            element.key_frames = data["key_frames"]

        if 'grid_position' in data:
            element.grid_position = data["grid_position"]
        return element

    def build_text_element(self, data):
        element = TextElement()
        element.text = data["text"]
        if 'position' in data:
            element.position = data["position"]

        if 'grid_position' in data:
            element.grid_position = data["grid_position"]

        if 'duration' in data:
            element.duration = data["duration"]

        if 'font_size' in data:
            element.font_size = data["font_size"]

        if 'font_type' in data:
            element.font_type = data["font_type"]

        if 'text_align' in data:
            element.text_align = data["text_align"]

        if 'start_time' in data:
            element.start_time = data["start_time"]

        if "font_color" in data:
            element.font_color = data["font_color"]

        return element

    def build_animated_text_element(self, data):
        element = AnimatedTextElement()
        element.text = data["text"]
        element.font_size = data["font_size"]
        element.font_type = data["font_type"]
        # if "text_align" in data:
        #     element.text_align = data["text_align"]
        element.key_frames = data["key_frames"]

        if "font_color" in data:
            element.font_color = data["font_color"]

        return element

