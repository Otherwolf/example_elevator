"""
This module contains custom exception classes related to elevator operations and passenger behavior.
These exceptions are used to handle specific error scenarios
that may occur during the execution of an elevator system.
"""


class ElevatorMoveError(Exception):
    """
    This error is triggered when the elevator tries to move out of bounds.
    """
    pass


class ElevatorInvalidCallingFloorError(Exception):
    """
    This error is caused when the elevator is called outside of the allowed values.
    """
    pass


class PassengerAlreadyInElevator(Exception):
    """
    This error is triggered when a passenger who is already in the elevator tries to enter the elevator again.
    """
    pass


class PassengerWrongFloorElevator(Exception):
    """
    This error is triggered when a passenger is on a different floor than the elevator.
    """
    pass


class PassengerCantEnterFullElevator(Exception):
    """
    This error is triggered when a passenger cannot enter a full elevator.
    """
    pass


class PassengerNotInElevator(Exception):
    """
    This error is triggered when a passenger who is not in the elevator tries to exit the elevator.
    """
    pass
