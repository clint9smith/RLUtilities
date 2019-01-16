from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket, PlayerInfo, \
    GameInfo, BoostPadState, FieldInfoPacket, BoostPad, GoalInfo

from RLUtilities.util.conversion import vector3_to_vec3
from RLUtilities.util.game_values import BACK_WALL
from RLUtilities.util.math import sign
from RLUtilities.LinearAlgebra import vec3, mat3

from RLUtilities.structure import Player, Ball, Goal, Pad


class GameData:

    """Internal structure representing data provided by the rlbot framework."""

    def __init__(self, name: str = 'nameless', team: int = 0, index: int = 0):

        self.name = name
        self.index = index
        self.team = team

        # cars
        self.my_car = Player()

        self.opponnents: List[Player] = []
        self.teammates: List[Player] = []

        # ball
        self.ball = Ball()

        # boost pads
        self.large_pads: List[Pad] = []
        self.small_pads: List[Pad] = []

        # goals
        own_goal_loc = vec3(0, BACK_WALL * sign(team), 0)
        own_goal_dir = vec3(0, sign(team), 0)

        self.opp_goal = Goal(own_goal_loc * -1, own_goal_dir * -1)
        self.own_goal = Goal(own_goal_loc, own_goal_dir)

        self.opp_goals = [self.opp_goal]
        self.own_goals = [self.own_goal]

        # other info
        self.time = 0.0
        self.time_remaining = 0.0
        self.overtime = False
        self.round_active = False
        self.kickoff_pause = False
        self.match_ended = False
        self.gravity = -650.0

    def read_game_tick_packet(self, game_tick_packet: GameTickPacket):
        """Reads an instance of GameTickPacket provided by the rlbot framework,
        and converts it's contents into our internal structure."""

        self.read_game_cars(game_tick_packet.game_cars,
                            game_tick_packet.num_cars)
        self.ball.read_game_ball(game_tick_packet.game_ball)
        self.read_game_boosts(game_tick_packet.game_boosts)
        self.read_game_info(game_tick_packet.game_info)

    def read_game_cars(self, game_cars: List[PlayerInfo], num_cars: int):

        self.my_car.read_game_car(game_cars[self.index])

        self.opponnents = []
        self.teammates = []
        for i in range(num_cars):
            if i != self.index:
                car = game_cars[i]
                team = self.opponnents if car.team != self.my_car.team else self.teammates
                team.append(Player().read_game_car(car))

    def read_game_boosts(self, game_boosts: List[BoostPadState]):

        for pad_type in (self.large_pads, self.small_pads):
            for pad in pad_type:
                pad.is_active = game_boosts[pad.index].is_active
                pad.timer = game_boosts[pad.index].timer

    def read_game_info(self, game_info: GameInfo):

        self.time = game_info.seconds_elapsed
        self.time_remaining = game_info.game_time_remaining
        self.overtime = game_info.is_overtime
        self.round_active = game_info.is_round_active
        self.kickoff_pause = game_info.is_kickoff_pause
        self.match_ended = game_info.is_match_ended
        self.gravity = game_info.world_gravity_z

    def read_field_info(self, field_info: FieldInfoPacket):
        """Reads an instance of FieldInfoPacket provided by the rlbot framework,
        and converts it's contents into our internal structure."""

        if field_info.num_boosts != 0:
            self.read_boost_pads(field_info.boost_pads, field_info.num_boosts)
            self.read_goals(field_info.goals, field_info.num_goals)

    def read_boost_pads(self, boost_pads: List[BoostPad], num_boosts: int):

        self.large_pads = []
        self.small_pads = []

        for i in range(num_boosts):
            pad = boost_pads[i]
            pad_type = self.large_pads if pad.is_full_boost else self.small_pads
            pad_obj = Pad(i, vector3_to_vec3(pad.location))
            pad_type.append(pad_obj)

    def read_goals(self, goals: List[GoalInfo], num_goals: int):

        self.opp_goals = []
        self.own_goals = []

        for i in range(num_goals):
            goal = goals[i]
            goal_type = self.opp_goals if goal.team_num != self.team else self.own_goals
            goal_obj = Goal(vector3_to_vec3(goal.location),
                            vector3_to_vec3(goal.direction))
            goal_type.append(goal_obj)

        if len(self.opp_goals) == 1:
            self.opp_goal = self.opp_goals[0]
        if len(self.own_goals) == 1:
            self.own_goal = self.own_goals[0]

        # TODO: add read_rigid_body_tick
