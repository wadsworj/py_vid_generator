class Interpolator:
    @staticmethod
    def get_previous_current_frames(key_frames, scene_seconds):
        previous_key_frame = None
        next_key_frame = None
        for key_frame in key_frames:
            if scene_seconds >= key_frame["second"] or not previous_key_frame:
                previous_key_frame = key_frame
            elif not next_key_frame and scene_seconds <= key_frame["second"]:
                next_key_frame = key_frame

        # if done next animation then set to previous
        if not next_key_frame:
            next_key_frame = previous_key_frame

        return [previous_key_frame, next_key_frame]

    # https://stackoverflow.com/questions/46732939/how-to-interpolate-2-d-points-between-two-timesteps
    @staticmethod
    def interpolate(t, time_1, time_2, point_1, point_2):
        if t <= time_1:
            return point_1

        if time_1 == time_2:
            return point_1

        dt = (t - time_1) / (time_2 - time_1)
        returned_points = []

        for i in range(len(point_1)):
            interpolated_point = point_2[i] - point_1[i]
            returned_points.append(dt * interpolated_point + point_1[i])

        return returned_points