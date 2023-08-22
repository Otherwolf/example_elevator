import pytest

import exceptions as exc
from elevator import Elevator, ElevatorDirection, Passenger


# _____________________ Elevator tests _________________________
@pytest.fixture
def elevator():
    return Elevator()


def test_add_floor(elevator: Elevator):
    assert elevator.queue == []
    elevator.add_floor(5)
    assert elevator.queue == [5]

    elevator.add_floor(3)
    assert elevator.queue == [3, 5]
    elevator.add_floor(3)
    assert elevator.queue == [3, 5]

    with pytest.raises(exc.ElevatorInvalidCallingFloorError):
        elevator.add_floor(0)

    with pytest.raises(exc.ElevatorInvalidCallingFloorError):
        elevator.add_floor(11)


def test_enter_passenger(elevator: Elevator):
    passenger = Passenger(1, 5)
    elevator.current_floor = 1
    elevator.enter_passenger(passenger)
    assert passenger in elevator.passengers
    assert elevator.queue == [5]

    with pytest.raises(exc.PassengerAlreadyInElevator):
        elevator.enter_passenger(passenger)

    passenger = Passenger(1, 5)

    with pytest.raises(exc.PassengerWrongFloorElevator):
        passenger.current_floor = 2
        elevator.enter_passenger(passenger)

    with pytest.raises(exc.PassengerCantEnterFullElevator):
        for i in range(10):
            elevator.enter_passenger(Passenger(elevator.current_floor, i + 1))


def test_exit_passenger(elevator: Elevator):
    passenger = Passenger(1, 5)
    elevator.current_floor = 1
    elevator.enter_passenger(passenger)
    elevator.current_floor = 5
    elevator.exit_passenger(passenger)
    assert passenger not in elevator.passengers
    assert elevator.queue == []

    with pytest.raises(exc.PassengerNotInElevator):
        elevator.exit_passenger(passenger)


def test_is_filled(elevator: Elevator):
    assert not elevator.is_filled

    for i in range(elevator.capacity):
        passenger = Passenger(elevator.current_floor, 8)
        elevator.enter_passenger(passenger)

    assert elevator.is_filled


def test_move(elevator: Elevator):
    elevator.add_floor(5)

    for i in range(1, 6):
        elevator.move()
        assert elevator.current_floor == i
        assert elevator.direction == ElevatorDirection.UP.value

    elevator.add_floor(4)
    elevator.move()
    assert elevator.current_floor == 4
    elevator.queue = []
    elevator.move()
    assert elevator.direction == ElevatorDirection.IDLE.value

    with pytest.raises(exc.ElevatorMoveError):
        for i in range(10):
            elevator.queue.append(0)
            elevator.move()


def test_open_doors(elevator: Elevator, capsys):
    elevator.open_doors()
    captured = capsys.readouterr()
    assert captured.out == "Elevator doors opened on floor 0\n"


def test_close_doors(elevator: Elevator, capsys):
    elevator.close_doors()
    captured = capsys.readouterr()
    assert captured.out == "Elevator doors closed on floor 0\n"


def test_can_passenger_enter(elevator: Elevator):
    passenger = Passenger(1, 5)
    elevator.current_floor = 1
    assert elevator.can_passenger_enter(passenger)

    elevator.enter_passenger(passenger)
    assert not elevator.can_passenger_enter(passenger)


def test_can_passenger_exit(elevator: Elevator):
    passenger = Passenger(1, 2)
    assert not elevator.can_passenger_exit(passenger)

    elevator.current_floor = 1
    elevator.enter_passenger(passenger)
    assert not elevator.can_passenger_exit(passenger)
    elevator.move()
    assert elevator.can_passenger_exit(passenger)


def test__remove_current_floor(elevator: Elevator):
    elevator.add_floor(5)
    elevator.current_floor = 5
    elevator._remove_current_floor()
    assert elevator.queue == []

    elevator.add_floor(3)
    elevator._remove_current_floor()
    assert elevator.queue == [3]


def test__stop(elevator: Elevator):
    elevator.add_floor(5)
    elevator.add_floor(7)
    elevator.move()
    elevator._stop()
    assert elevator.direction == ElevatorDirection.IDLE.value


# _____________________ Passenger tests _________________________

@pytest.fixture
def passenger():
    return Passenger(1, 5)


def test_call_elevator(passenger: Passenger, elevator: Elevator):
    passenger.call_elevator(elevator)
    assert elevator.queue == [1]


def test_enter_elevator(passenger: Passenger, elevator: Elevator):
    passenger.enter_elevator(elevator)
    assert elevator.passengers == []
    elevator.current_floor = 1
    passenger.enter_elevator(elevator)
    assert elevator.passengers == [passenger]


def test_exit_elevator(passenger: Passenger, elevator: Elevator):
    elevator.current_floor = 1
    passenger.enter_elevator(elevator)
    elevator.current_floor = 5
    passenger.exit_elevator(elevator)
    assert elevator.passengers == []
    assert passenger.is_achieved is True
