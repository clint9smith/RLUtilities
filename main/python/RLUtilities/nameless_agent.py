from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from RLUtilities.structure import GameData
from RLUtilities.structure import ExtraGameData


class NamelessAgent(BaseAgent):

    """Base class inheriting from BaseAgent that manages data provided by the rlbot framework,
    and converts it into our internal data structure, and extracts further useful info."""

    def __init__(self, name: str = 'nameless', team: int = 0, index: int = 0):

        super(NamelessAgent, self).__init__(name, team, index)

        self.game_data = GameData(self.name, self.team, self.index)
        self.extra_game_data = ExtraGameData()
        self.controls = SimpleControllerState()

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        """Overriding this function is not advised, use update_controls() instead."""

        self.pre_process(game_tick_packet)

        self.controls = self.update_controls()

        self.feedback()

        return self.controls

    def pre_process(self, game_tick_packet: GameTickPacket):
        """First thing executed in get_output()."""

        self.game_data.read_field_info(self.get_field_info())
        self.game_data.read_game_tick_packet(game_tick_packet)
        self.extra_game_data.update(self.game_data)

    def feedback(self):
        """Last thing executed in get_output() before return statement."""

        self.extra_game_data.feedback(self.game_data, self.controls)

    def update_controls(self) -> SimpleControllerState:
        """Function to override by inheriting classes"""
        return self.controls
