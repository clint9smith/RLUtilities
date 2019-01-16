from rlbot.utils.structures.game_data_struct import BallInfo, Touch, DropShotInfo

from RLUtilities.structure import PhysicsObject
from RLUtilities.LinearAlgebra import vec3


class Ball(PhysicsObject):

    def __init__(self):

        # physics
        super(Ball, self).__init__()

        # latest touch
        self.touch_player_name = "nameless"
        self.touch_time = 0.0
        self.touch_location = vec3
        self.touch_direction = vec3

        # drop shot info
        self.absorbed_force = 0.0
        self.damage_index = 0
        self.force_accum_recent = 0.0

    def read_game_ball(self, game_ball: BallInfo):

        super(Ball, self).read_physics(game_ball.physics)
        self.read_latest_touch(game_ball.latest_touch)
        self.read_drop_shot_info(game_ball.drop_shot_info)

    def read_latest_touch(self, latest_touch: Touch):

        self.touch_player_name = latest_touch.player_name
        self.touch_time = latest_touch.time_seconds
        self.touch_location = latest_touch.hit_location
        self.touch_direction = latest_touch.hit_normal

    def read_drop_shot_info(self, drop_shot_info: DropShotInfo):

        self.absorbed_force = drop_shot_info.absorbed_force
        self.damage_index = drop_shot_info.damage_index
        self.force_accum_recent = drop_shot_info.force_accum_recent
