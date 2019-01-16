from RLUtilities.LinearAlgebra import vec3


class Goal:

    def __init__(self, location: vec3 = None, direction: vec3 = None):

        if location is not None:
            self.location = location
        else:
            self.location = vec3(0, 0, 0)

        if direction is not None:
            self.direction = direction
        else:
            self.direction = vec3(0, 0, 0)
