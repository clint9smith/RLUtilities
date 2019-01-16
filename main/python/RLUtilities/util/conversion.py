import math
from rlbot.utils.structures.game_data_struct import Vector3, Rotator
from RLUtilities.LinearAlgebra import vec3, mat3


def vector3_to_vec3(vector3: Vector3) -> vec3:
    """Converts Vector3 to vec3"""
    return vec3(vector3.x, vector3.y, vector3.z)


def rotator_to_vec3(rotator: Rotator):
    """Converts rotator to vec3"""
    return vec3(rotator.pitch, rotator.yaw, rotator.roll)


def rotator_to_mat3(rotator: Rotator) -> mat3:
    """Converts Rotator to 3x3 matrix"""
    CP = math.cos(rotator.pitch)
    SP = math.sin(rotator.pitch)
    CY = math.cos(rotator.yaw)
    SY = math.sin(rotator.yaw)
    CR = math.cos(rotator.roll)
    SR = math.sin(rotator.roll)

    theta = mat3(*[0 for i in range(9)])

    # front direction
    theta[0, 0] = CP * CY
    theta[1, 0] = CP * SY
    theta[2, 0] = SP

    # left direction
    theta[0, 1] = CY * SP * SR - CR * SY
    theta[1, 1] = SY * SP * SR + CR * CY
    theta[2, 1] = -CP * SR

    # up direction
    theta[0, 2] = -CR * CY * SP - SR * SY
    theta[1, 2] = -CR * SY * SP + SR * CY
    theta[2, 2] = CP * CR

    return theta
