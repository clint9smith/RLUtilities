from rlbot.utils.structures.game_data_struct import Physics
from RLUtilities.LinearAlgebra import vec3, mat3
from RLUtilities.util.conversion import vector3_to_vec3, rotator_to_vec3, rotator_to_mat3


class PhysicsObject:

    def __init__(self):

        self.location = vec3(0, 0, 0)
        self.rotation = vec3(0, 0, 0)
        self.velocity = vec3(0, 0, 0)
        self.angular_velocity = vec3(0, 0, 0)
        self.rotation_matrix = mat3(*[0 for i in range(9)])

    def read_physics(self, physics: Physics):

        self.location = vector3_to_vec3(physics.location)
        self.rotation = rotator_to_vec3(physics.rotation)
        self.velocity = vector3_to_vec3(physics.velocity)
        self.angular_velocity = vector3_to_vec3(physics.angular_velocity)
        self.rotation_matrix = rotator_to_mat3(physics.rotation)
