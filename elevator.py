"""
Elevator Control System

This module implements an elevator control system in Python using object-oriented programming paradigm.
It includes an Elevator class and a Passenger class to simulate the movement of the elevator, its stops and status,
and handle passengers requesting rides from different floors.
Elevator algorithm - LOOK

Author: Pavel Volkov (vpe304@gmail.com)
Date: 2023-08-22
"""
import enum

import exceptions as exc


class ElevatorDirection(enum.IntEnum):
    IDLE = 0
    UP = 1
    DOWN = -1


class Elevator:
    def __init__(self, capacity: int = 10, min_floor: int = 1, max_floor: int = 10):
        self.num_floors = max_floor
        self.min_floor = min_floor
        self.capacity = capacity
        self.direction = ElevatorDirection.IDLE.value  # 0 for idle, 1 for up, -1 for down

        self.current_floor = min_floor - 1
        self.passengers = []
        self.queue = []  # The queue of floors it needs to stop on.

    def add_floor(self, floor: int) -> None:
        if floor not in self.queue:

            if floor < self.min_floor:
                raise exc.ElevatorInvalidCallingFloorError("Elevator was called below ground level.")
            elif floor > self.num_floors:
                raise exc.ElevatorInvalidCallingFloorError("Elevator was called above top floor.")

            self.queue.append(floor)
            self.queue.sort()  # Sort the queue to optimize the journey

    def enter_passenger(self, passenger):
        if passenger in self.passengers:
            raise exc.PassengerAlreadyInElevator(f"The {passenger} is already in the elevator")

        if passenger.current_floor != self.current_floor:
            raise exc.PassengerWrongFloorElevator(f"Expected floor {passenger.current_floor} "
                                                  f"but current floor of elevator is {self.current_floor}")

        if self.is_filled:
            raise exc.PassengerCantEnterFullElevator("Passenger cannot enter a full elevator")

        self.passengers.append(passenger)
        self.add_floor(passenger.destination_floor)
        return self._remove_current_floor()

    def exit_passenger(self, passenger):
        if passenger not in self.passengers:
            raise exc.PassengerNotInElevator("There is no passenger in the elevator")

        self.passengers.remove(passenger)
        self._remove_current_floor()

    @property
    def is_filled(self):
        return len(self.passengers) >= self.capacity

    def move(self) -> None:
        """
        move the elevator by one floor.
        """
        if self.queue:
            index_direction = 0 if self.direction == ElevatorDirection.DOWN.value else -1
            # move one floor by direction
            if self.queue[index_direction] > self.current_floor:
                self.direction = ElevatorDirection.UP.value
            elif self.queue[index_direction] < self.current_floor:
                self.direction = ElevatorDirection.DOWN.value
            else:
                self.direction = -self.direction

            # Check for invalid floor movement
            next_floor = self.current_floor + self.direction
            if next_floor < self.min_floor:
                raise exc.ElevatorMoveError("Elevator moved below ground level.")
            elif next_floor > self.num_floors:
                raise exc.ElevatorMoveError("Elevator moved above top floor.")

            # add one floor +1 or -1
            self.current_floor = next_floor

        # stop the elevator if the queue is over
        else:
            self._stop()

    def open_doors(self) -> None:
        print(f"Elevator doors opened on floor {self.current_floor}")

    def close_doors(self) -> None:
        print(f"Elevator doors closed on floor {self.current_floor}")

    def can_passenger_enter(self, passenger) -> bool:
        return passenger.current_floor == self.current_floor and passenger not in self.passengers

    def can_passenger_exit(self, passenger) -> bool:
        return passenger.destination_floor == self.current_floor and passenger in self.passengers

    def _remove_current_floor(self):
        if self.current_floor in self.queue:
            self.queue.remove(self.current_floor)

    def _stop(self):
        if self.direction != ElevatorDirection.IDLE.value:
            self.direction = ElevatorDirection.IDLE.value


class Passenger:
    def __init__(self, current_floor: int, destination_floor: int):
        self.current_floor = current_floor
        self.destination_floor = destination_floor

        self.is_achieved = False  # for testing

    def call_elevator(self, elevator: Elevator) -> None:
        elevator.add_floor(self.current_floor)

    def enter_elevator(self, elevator: Elevator) -> None:
        if elevator.can_passenger_enter(self):
            if elevator.is_filled:
                # call the elevator again if it was overloaded
                self.call_elevator(elevator)
            else:
                print(f"{self} entered ")
                elevator.enter_passenger(self)

                if self.current_floor == self.destination_floor:
                    return self.exit_elevator(elevator)

    def exit_elevator(self, elevator: Elevator) -> None:
        if elevator.can_passenger_exit(self):
            print(f"{self} exited ")
            elevator.exit_passenger(self)
            self.is_achieved = True

    def __str__(self) -> str:
        return f"Passenger[{self.current_floor}:{self.destination_floor}]"

    def __repr__(self) -> str:
        return str(self)
