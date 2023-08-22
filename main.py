"""
Write code that simulates people using the elevator over a day:
- Passengers arrive randomly at different floors and press the elevator button.
- Passengers enter the queue of the Elevator's called floors.
- Passengers can enter the Elevator only if it's on their current floor and if it's not full.
- The elevator moves from floor to floor and stops whenever needed to let Passengers in or out.

"""
import random
import time
from typing import List

from elevator import Elevator, Passenger


ELEVATOR_CAPACITY = 3
MAX_FLOOR = 10
MAX_PASSENGERS = 100


def print_building(elevator: Elevator, passengers_list: List[Passenger]) -> None:
    """
    method for drawing an elevator
    :param elevator: Elevator
    :param passengers_list: list of passengers for test
    :return:
    """
    print('-----------------------------------------')
    unfinished_passengers = [passenger for passenger in passengers_list if not passenger.is_achieved]
    print(f'floor={elevator.current_floor};    {elevator.queue=}; '
          f'{unfinished_passengers[:6]=}({len(unfinished_passengers)})')
    for i in range(MAX_FLOOR, 0, -1):
        if elevator.current_floor == i:
            queue_char = passengers = ' '
            if elevator.passengers:
                queue_char = 'X'
                passengers = elevator.passengers
            print(f'|  [{queue_char}]  |', passengers)
        else:
            print('|       |')


def main():
    elevator = Elevator(ELEVATOR_CAPACITY)
    passengers = []

    for _ in range(random.randint(1, MAX_PASSENGERS)):  # Simulate 100 passengers over a day
        current_floor = random.randint(1, MAX_FLOOR)
        destination_floor = random.randint(1, MAX_FLOOR)

        passenger = Passenger(current_floor, destination_floor)
        passengers.append(passenger)

        passenger.call_elevator(elevator)

    while elevator.queue:
        elevator.move()

        if elevator.current_floor in elevator.queue:
            elevator.open_doors()

            for passenger in list(elevator.passengers):
                # first we release everyone who needs to get out of the elevator
                passenger.exit_elevator(elevator)

            for passenger in passengers:
                if passenger.is_achieved:
                    continue
                passenger.enter_elevator(elevator)

            elevator.close_doors()

        print_building(elevator, passengers)
        time.sleep(0.2)

    assert not [True for passenger in passengers if not passenger.is_achieved], \
        'not all passengers reached the goal'


if __name__ == "__main__":
    main()
