from __future__ import absolute_import, division, print_function

from compas.files import URDF

from .geometry import SCALE_FACTOR, Origin, _parse_floats

__all__ = ['Joint', 'ParentJoint', 'ChildJoint', 'Calibration',
           'Dynamics', 'Limit', 'Axis', 'Mimic', 'SafetyController']


class ParentJoint(object):
    """Describes a parent relation between joints."""

    def __init__(self, link):
        self.link = link

    def __str__(self):
        return str(self.link)


class ChildJoint(object):
    """Describes a child relation between joints."""

    def __init__(self, link):
        self.link = link

    def __str__(self):
        return str(self.link)


class Calibration(object):
    """Reference positions of the joint, used to calibrate the absolute position."""

    def __init__(self, rising=0.0, falling=0.0, reference_position=0.0):
        self.rising = float(rising)
        self.falling = float(falling)
        self.reference_position = float(reference_position)


class Dynamics(object):
    """Physical properties of the joint used for simulation of dynamics."""

    def __init__(self, damping=0.0, friction=0.0):
        self.damping = float(damping)
        self.friction = float(friction)


class Limit(object):
    """Joint limit properties.

    Attributes:
        effort: Maximum joint effort.
        velocity: Maximum joint velocity.
        lower: Lower joint limit (radians for revolute joints, millimeter for prismatic joints).
        upper: Upper joint limit (radians for revolute joints, millimeter for prismatic joints).
    """

    def __init__(self, effort=0.0, velocity=0.0, lower=0.0, upper=0.0):
        self.effort = float(effort)
        self.velocity = float(velocity)
        # TODO: Scale upper/lower limits once this is connected to a joint, if the joint is prismatic
        self.lower = float(lower)
        self.upper = float(upper)


class Mimic(object):
    """Description of joint mimic."""

    def __init__(self, joint, multiplier=1.0, offset=0):
        self.joint = joint
        self.multiplier = multiplier
        self.offset = offset


class SafetyController(object):
    """Safety controller properties."""

    def __init__(self, k_velocity, k_position=0.0, soft_lower_limit=0.0, soft_upper_limit=0.0):
        self.k_velocity = float(k_velocity)
        self.k_position = float(k_position)
        self.soft_lower_limit = float(soft_lower_limit)
        self.soft_upper_limit = float(soft_upper_limit)


class Axis(object):
    """Representation of an axis or vector."""

    def __init__(self, xyz='0 0 0'):
        # We are not using Vector here because we
        # cannot attach _urdf_source to it due to __slots__
        xyz = _parse_floats(xyz, SCALE_FACTOR)
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]


class Joint(object):
    """Representation of the kinematics and dynamics of a
    joint and its safety limits.

    Attributes:
        name: Unique name for the joint.
        type: Joint type.
        origin: Transformation from the parent link to the child link frame.
        parent: Name of the parent link.
        child: Name of the child link.
        axis: Joint axis specified in the joint frame. Represents the axis of rotation
            for revolute joints, the axis of translation for prismatic joints, and
            the surface normal for planar joints. The axis is specified in the joint
            frame of reference.
        calibration: Reference positions of the joint, used to calibrate the absolute
            position of the joint.
        dynamics: Physical properties of the joint. These values are used to specify
            modeling properties of the joint, particularly useful for simulation.
        limit: Joint limit properties.
        safety_controller: Safety controller properties.
        mimic: Used to specify that the defined joint mimics another existing joint.
        attr: Non-standard attributes.
        childlink: the joint's child link
    """
    SUPPORTED_TYPES = ('revolute', 'continuous', 'prismatic',
                       'fixed', 'floating', 'planar')

    def __init__(self, name, type, parent, child, origin=None, axis=None, calibration=None, dynamics=None, limit=None, safety_controller=None, mimic=None, **kwargs):
        if type not in (Joint.SUPPORTED_TYPES):
            raise ValueError('Unsupported joint type: %s' % type)

        self.name = name
        self.type = type
        self.parent = parent
        self.child = child
        self.origin = origin
        self.axis = axis
        self.calibration = calibration
        self.dynamics = dynamics
        self.limit = limit
        self.safety_controller = safety_controller
        self.mimic = mimic
        self.attr = kwargs
        self.childlink = None


URDF.add_parser(Joint, 'robot/joint')
URDF.add_parser(ParentJoint, 'robot/joint/parent')
URDF.add_parser(ChildJoint, 'robot/joint/child')
URDF.add_parser(Calibration, 'robot/joint/calibration')
URDF.add_parser(Dynamics, 'robot/joint/dynamics')
URDF.add_parser(Limit, 'robot/joint/limit')
URDF.add_parser(Axis, 'robot/joint/axis')
URDF.add_parser(Mimic, 'robot/joint/mimic')
URDF.add_parser(SafetyController, 'robot/joint/safety_controller')

URDF.add_parser(Origin, 'robot/joint/origin')