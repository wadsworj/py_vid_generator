from src.config import config


class PositionToGridPosition:
    @staticmethod
    def convert_position_to_grid_position(position):
        grid_position = [0, 0]
        grid_position[0] = float(position[0] / (config.SCREEN_WIDTH / 16))
        grid_position[1] = float(position[1] / (config.SCREEN_HEIGHT / 9))
        return grid_position

    @staticmethod
    def convert_grid_position_to_position(grid_position):
        position = [0, 0]
        position[0] = float(grid_position[0]) * (config.SCREEN_WIDTH / 16)
        position[1] = float(grid_position[0]) * (config.SCREEN_HEIGHT / 9)
        return position
