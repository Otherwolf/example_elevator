# Elevator Control System

This project implements an **elevator control system** in Python using the object-oriented programming paradigm.
The application simulates the movement of an elevator, its stops and status, 
and handles passengers requesting rides from different floors.

## Install
require **python 3.9+**
```bash
git clone https://github.com/Otherwolf/example_elevator.git

# for testing
pip install pytest
```

## Simple Demo

```python
from elevator import Elevator, Passenger

# creating a new passenger with params [from floor, to floor]
passenger = Passenger(1, 2)

# creating a new elevator with params [capacity of elevator]
elevator = Elevator(5)

# passenger calls the elevator
passenger.call_elevator(elevator)

# move elevator by one floor and open doors cause there is passenger waits the elevator
elevator.move()

elevator.open_doors()
passenger.enter_elevator(elevator)
elevator.close_doors()

elevator.move()

# climbed to the desired floor and released the passenger
elevator.open_doors()
passenger.exit_elevator(elevator)
elevator.close_doors()
```

## Tests

```python
pytest elevator_tests.py
```
