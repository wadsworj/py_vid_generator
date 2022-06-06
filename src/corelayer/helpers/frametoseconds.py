from src.config import config


class FrameToSeconds:
    @staticmethod
    def convert_frame_to_seconds(frame):
        return frame / config.FRAME_RATE