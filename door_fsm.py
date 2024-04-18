# Imports #
from enum import Enum

# Global Variables #
timer_duration = 10


class DoorState(Enum):
    LOCKED = 0
    CLOSED = 1
    CLOSING = 2
    OPENING = 3
    OPEN = 4

class DoorStateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.timer = timer_duration
        self.locked = False
        self.user_actions = {
            'lock': lambda: self.lock(),
            'unlock': lambda: self.unlock(),
            'open': lambda: self.open(),
            'close': lambda: self.close()
        }

    # Helper Methods #
    def transition(self, next_state):
        self.state = next_state

    # Methods for modifying non-state State Machine variables #
    def decrement_timer(self):
        print("Ticking down timer")
        self.timer -= 1

    def reset_timer(self):
        print("Resetting timer")
        self.timer = timer_duration

    def lock(self):
        if self.state == (DoorState.CLOSED or DoorState.OPEN):
            if self.locked == True:
                print("Door already locked")
            else:
                print("Locking the door")
                self.locked = True

    def unlock(self):
        if self.state == (DoorState.CLOSED or DoorState.OPEN):
            if self.locked == False:
                print("Door already unlocked")
            else:
                print("Unlocking the door")
                self.locked = False


    # State modifying functions #
    def open(self):
        if (self.state == DoorState.CLOSED) and (self.locked == False):
            print("Opening door")
            self.transition(DoorState.OPENING)
        elif (self.state != DoorState.CLOSED):
            print("Door can't be opened unless it's CLOSED")
        else:
            print("Door can't be opened unless it's unlocked")

    def close(self):
        if (self.state == DoorState.OPEN) and (self.locked == False):
            print("Closing Door")
            self.transition(DoorState.CLOSING)
        elif (self.state != DoorState.OPEN):
            print("Door can't be closed unless it's OPEN")
        else:
            print("Door can't be closed unless it's unlocked")


    # Runtime #
    def run(self):
        running = True
        while running:
            try:
                # Accept user input and perform appropriate actions only in OPEN and CLOSED states
                if self.state in [DoorState.CLOSED, DoorState.OPEN]:
                    user_action = input("Enter a door action: ").strip().lower() # using .strip() to remove all trailing spaces and .lower() to convert to lowercase
                    if user_action not in self.user_actions:
                        print("Unknown action entered, please enter one of the following: lock, unlock, open, close")
                    else:
                        print("Executing action",repr(user_action))
                        #print(repr(self.user_actions[user_action]))
                        self.user_actions[user_action]()
                elif self.state in [DoorState.OPENING, DoorState.CLOSING]:
                    self.decrement_timer()
                    if self.timer == 0:
                        if self.state == DoorState.OPENING:
                            self.transition(DoorState.OPEN)
                            self.reset_timer()
                            print("Door has fully opened")
                        elif self.state == DoorState.CLOSING:
                            self.transition(DoorState.CLOSED)
                            self.reset_timer()
                            print("Door has fully closed")
            except KeyboardInterrupt:
                print("\nExiting state machine...")
                running = False
                #print("Running has been set to",running)


# Example usage
door = DoorStateMachine(DoorState.CLOSED)
door.run()


"""
        # (startstate, list_of_conditions): (list_of_actions, endstate)
        # Modified version --> (startstate, user_action, list_of_guard_conditions): (list_of_actions, endstate)
        self.transitions = {
            (DoorState.CLOSED, 'lock', (self.is_locked())): (lambda:(print('Door already locked')), DoorState.CLOSED),
            (DoorState.CLOSED, 'lock', (not self.is_locked())): (lambda:(self.lock()), DoorState.CLOSED),
            (DoorState.CLOSED, 'unlock', (not self.is_locked())): (lambda:(print('Door already unlocked')), DoorState.CLOSED),
            (DoorState.CLOSED, 'unlock', (self.is_locked())): (lambda:(self.unlock()), DoorState.CLOSED),
            (DoorState.CLOSED, 'open', (not self.is_locked())): (lambda:(print('Opening the door'), self.decrement_timer()), DoorState.OPENING),
            (DoorState.OPENING, None, (not self.timer_finished())): (lambda:(self.decrement_timer()), DoorState.OPENING),
            (DoorState.OPENING, None, (self.timer_finished())): (lambda:(self.reset_timer()), DoorState.OPEN),
            (DoorState.OPEN, 'lock', (self.is_locked())): (lambda:(print('Door already locked')), DoorState.OPEN),
            (DoorState.OPEN, 'lock', (not self.is_locked())): (lambda:(self.lock()), DoorState.OPEN),
            (DoorState.OPEN, 'unlock', (not self.is_locked())): (lambda:(print('Door already unlocked')), DoorState.OPEN),
            (DoorState.OPEN, 'unlock', (self.is_locked())): (lambda:(self.unlock()), DoorState.OPEN),
            (DoorState.OPEN, 'close', (not self.is_locked())): (lambda:(print('Closing the door'), self.decrement_timer()), DoorState.CLOSING),
            (DoorState.CLOSING, None, (not self.timer_finished())): (lambda:(self.decrement_timer()), DoorState.CLOSING),
            (DoorState.CLOSING, None, (self.timer_finished())): (lambda:(self.reset_timer()), DoorState.CLOSED),
        }
        """