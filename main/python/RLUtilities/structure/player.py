from rlbot.utils.structures.game_data_struct import PlayerInfo
from RLUtilities.structure import PhysicsObject


class Player(PhysicsObject):

    def __init__(self):

        # physics
        super(Player, self).__init__()

        # other game_car info
        self.boost = 0.0
        self.jumped = False
        self.double_jumped = False
        self.on_ground = False
        self.supersonic = False
        self.team = 0

    def read_game_car(self, game_car: PlayerInfo):

        super(Player, self).read_physics(game_car.physics)
        self.boost = game_car.boost
        self.jumped = game_car.jumped
        self.double_jumped = game_car.double_jumped
        self.on_ground = game_car.has_wheel_contact
        self.supersonic = game_car.is_super_sonic
        self.team = game_car.team
