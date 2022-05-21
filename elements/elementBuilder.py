from elements.animatedElement import AnimatedTextElement
from elements.textElement import TextElement


class ElementBuilder:
    def __init__(self):
        pass

    def build(self, data):
        if data["type"] == "TEXT":
            return self.build_text_element(data)
        elif data["type"] == "ANIMATED_TEXT":
            return self.build_animated_text_element(data)

    def build_text_element(self, data):
        element = TextElement()
        element.name = data["name"]
        element.text = data["text"]
        element.position = data["position"]
        element.bounding_box = data["bounding_box"]
        element.duration = data["duration"]
        element.font_size = data["font_size"]
        element.font_type = data["font_type"]
        element.text_align = data["text_align"]
        element.start_time = data["start_time"]

        if "font_color" in data:
            element.font_color = data["font_color"]

        return element

    def build_animated_text_element(self, data):
        element = AnimatedTextElement()
        element.name = data["name"]
        element.text = data["text"]
        element.font_size = data["font_size"]
        element.font_type = data["font_type"]
        element.text_align = data["text_align"]

        if "font_color" in data:
            element.font_color = data["font_color"]

        return element

