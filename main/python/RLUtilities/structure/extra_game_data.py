from rlbot.agents.base_agent import SimpleControllerState
from RLUtilities.structure import GameData
from RLUtilities.structure import ExtraPlayerData


class ExtraGameData:

    """Contains extra info not immediatly avalaible in the GameData class."""

    def __init__(self):
        self.frame = 0
        self.my_car = ExtraPlayerData()

    def update(self, game_data: GameData):
        """Extracts and updates extra game data from GameData."""

        self.my_car.update(game_data.my_car, game_data.time)

    def feedback(self, game_data: GameData, controls: SimpleControllerState):
        """Called just before the end of a bot's get_output(),
        it saves some useful data to be used in the next ticks."""

        self.frame += 1
        self.my_car.feedback(game_data.my_car, controls)
