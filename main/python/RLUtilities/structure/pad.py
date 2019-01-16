from RLUtilities.LinearAlgebra import vec3


class Pad:

    def __init__(self, index: int = 0, location: vec3 = None, is_active: bool = True,
                 timer: float = 0.0):

        self.index = index
        self.is_active = is_active
        self.timer = timer

        if location is None:
            self.location = vec3(0, 0, 0)
        else:
            self.location = location
