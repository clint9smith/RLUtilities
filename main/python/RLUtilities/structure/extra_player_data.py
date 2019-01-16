from rlbot.agents.base_agent import SimpleControllerState
from RLUtilities.structure import Player


class ExtraPlayerData:

    """Contains extra info data not immediatly avalaible in the Player class."""

    def __init__(self):

        # the moment in time the action happened
        self.air_time = 0.0
        self.ground_time = 0.0
        self.jump_start_time = 0.0
        self.jump_end_time = 0.0
        self.dodge_time = 0.0

        # the time between when the action happened and the present
        self.air_timer = 0.0
        self.ground_timer = 0.0
        self.jump_start_timer = 0.0
        self.jump_end_timer = 0.0
        self.dodge_timer = 0.0

        self.jump_count = 2
        self.jump_available = True
        self.first_jump_ended = False

        self.time = 0.0
        self.last_time = 0.0
        self.last_jumped = False
        self.last_on_ground = False
        self.controls_history = [
            SimpleControllerState(), SimpleControllerState()]

    def update(self, player: Player, time: float):

        self.time = time

        # the moment we left the ground
        if not player.on_ground and (self.last_on_ground or self.air_time == 0.0):
            self.air_time = self.time

        # the moment we left the air
        if player.on_ground and (not self.last_on_ground or self.ground_time == 0.0):
            self.ground_time = self.time

        # the moment we start jumping
        if player.jumped and not self.last_jumped:
            self.jump_start_time = self.time
            self.jump_end_time = self.time + 0.2

        # the moment we let go of jump in the air
        if not self.last_on_ground and self.controls_history[-2].jump and not self.controls_history[-1].jump:
            self.jump_end_time = self.last_time

        self.air_timer = self.time - self.air_time
        self.ground_timer = self.time - self.ground_time
        self.jump_start_timer = self.time - self.jump_start_time
        self.jump_end_timer = self.time - self.jump_end_time

        # reset timers
        if player.on_ground and self.last_on_ground:
            self.air_timer = 0.0

        if not player.on_ground and not self.last_on_ground:
            self.ground_timer = 0.0

        # determining how many jumps we have available
        if player.on_ground:
            self.jump_count = 2
        elif player.double_jumped or (self.jump_end_timer > 1.25 and player.jumped):
            self.jump_count = 0
        else:
            self.jump_count = 1

        self.jump_available = self.jump_count > 0
        self.first_jump_ended = self.jump_end_timer >= 0

    def feedback(self, player: Player, controls: SimpleControllerState):

        self.last_time = self.time
        self.last_jumped = player.jumped
        self.last_on_ground = player.on_ground

        self.controls_history[-2] = self.controls_history[-1]
        self.controls_history[-1] = controls
