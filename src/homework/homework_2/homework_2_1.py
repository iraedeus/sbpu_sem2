from typing import Any, Optional

from src.homework.homework_1.homework_1_1 import *

START_MESSAGE = (
    "This is a program for performing actions on a list of integers. Available commands: \n"
    "1) InsertFirst --value (Insert your value to the beginning of the list) \n"
    "2) InsertLast --value (Insert your value to the end of the list) \n"
    "3) Swap --first_index --second_index (Swap the values in the list that are on the indexes) \n"
    "4) Add --index --value (Add value to element in the list by index) \n"
    "5) Flip --index (Reverse the sign of element by index) \n"
    "6) Square --index (Square the element by index) \n"
    "7) Reverse (Reverse the list) \n"
    "8) DeleteSlice --first_index --second_index (Delete all elements by first index to second index inclusive) \n"
    "9) Pop --index (Delete element by index) \n"
    "10) Move --step (Move all elements to the right by step)"
    "11) Undo (Undo last action) \n"
    "12) ShowList (Print your list in console) \n"
    "13) Exit (Exit the program)"
)
ACTIONS = Registry["Action"](default=None)


class Node:
    def __init__(self, next: Optional["Node"], value: Any):
        self.next: Optional[Node] = next
        self.value = value


class Stack:
    def __init__(self, head: Optional[Node]) -> None:
        self.head: Optional[Node] = head

    def put(self, value: Any) -> None:
        new_node = Node(self.head, value)
        self.head = new_node

    def pop(self) -> Any:
        if self.head is None:
            raise IndexError("Pop from empty Stack object")

        value = self.head.value
        new_node = self.head.next
        self.head = new_node

        return value


class PerformedCommandStorage:
    def __init__(self, storage: list[int], history: Stack = Stack(None)) -> None:
        if not isinstance(storage, list):
            raise TypeError("Storage must be list")
        self.history: Stack = history
        self.storage: list[int] = storage

    def apply(self, action: "Action") -> None:
        self.history.put(action)
        action.do(self)

    def undo(self) -> None:
        if self.history.head is None:
            raise IndexError("Pop from empty Stack object")
        action = self.history.head.value
        action.undo(self)
        self.history.pop()


class Action:
    def do(self, command_storage: PerformedCommandStorage) -> None:
        pass

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        pass


@ACTIONS.register("InsertFirst")
class ActionInsertFirst(Action):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value

    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage.insert(0, self.value)

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        del command_storage.storage[0]


@ACTIONS.register("InsertLast")
class ActionInsertLast(Action):
    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the value must be an int")
        self.value = value

    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage.append(self.value)

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        del command_storage.storage[-1]


@ACTIONS.register("Swap")
class ActionSwap(Action):
    def __init__(self, first_index: int, second_index: int):
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")
        self.first_index = first_index
        self.second_index = second_index

    def do(self, command_storage: PerformedCommandStorage) -> None:
        first_value, second_value = (
            command_storage.storage[self.first_index],
            command_storage.storage[self.second_index],
        )
        command_storage.storage[self.first_index], command_storage.storage[self.second_index] = (
            second_value,
            first_value,
        )

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        self.do(command_storage)


@ACTIONS.register("Add")
class ActionAdd(Action):
    def __init__(self, index: int, value: int):
        if not isinstance(value, int) or not isinstance(index, int):
            raise TypeError("The type of the value and index must be an int")
        self.index = index
        self.value = value

    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage[self.index] += self.value

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage[self.index] -= self.value


@ACTIONS.register("Flip")
class ActionFlip(Action):
    def __init__(self, index: int) -> None:
        self.index = index

    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage[self.index] = -command_storage.storage[self.index]

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        self.do(command_storage)


@ACTIONS.register("Square")
class ActionSquare(Action):
    def __init__(self, index: int) -> None:
        self.index = index

    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage[self.index] = command_storage.storage[self.index] ** 2

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage[self.index] = int(command_storage.storage[self.index] ** 0.5)


@ACTIONS.register("Reverse")
class ActionReverse(Action):
    def do(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage.reverse()

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage.reverse()


@ACTIONS.register("DeleteSlice")
class ActionDeleteSlice(Action):
    def __init__(self, first_index: int, second_index: int) -> None:
        if not isinstance(first_index, int) or not isinstance(second_index, int):
            raise TypeError("The type of the indexes must be an int")

        self.first_index: int = first_index
        self.second_index: int = second_index
        self.deleted_slice: list[int] = []

    def do(self, command_storage: PerformedCommandStorage) -> None:
        self.deleted_slice = command_storage.storage[self.first_index : self.second_index + 1]
        command_storage.storage = (
            command_storage.storage[: self.first_index] + command_storage.storage[self.second_index + 1 :]
        )

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage = (
            command_storage.storage[: self.first_index]
            + self.deleted_slice
            + command_storage.storage[self.first_index :]
        )


@ACTIONS.register("Pop")
class ActionPop(Action):
    def __init__(self, index: int) -> None:
        self.index = index
        self.value: Optional[int] = None

    def do(self, command_storage: PerformedCommandStorage) -> None:
        self.value = command_storage.storage.pop(self.index)

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        command_storage.storage.insert(self.index, self.value)


@ACTIONS.register("Move")
class ActionMove(Action):
    def __init__(self, step):
        self.step = step

    def do(self, command_storage: PerformedCommandStorage) -> None:
        if self.step == 0:
            return None

        length = len(command_storage.storage)
        command_storage.storage = (
            command_storage.storage[length - self.step :] + command_storage.storage[: length - self.step]
        )

    def undo(self, command_storage: PerformedCommandStorage) -> None:
        if self.step == 0:
            return None

        length = len(command_storage.storage)
        command_storage.storage = (
            command_storage.storage[length - self.step :] + command_storage.storage[: length - self.step]
        )


def parse_args(user_command: str) -> tuple[str, list[Any]]:
    strings = user_command.split(" ")
    return strings[0], strings[1:]


def to_int(args: list[Any]) -> list[int]:
    for i in range(len(args)):
        args[i] = int(args[i])

    return args


def do_action(user_cmd_storage: PerformedCommandStorage, user_action: str, args: list[Any]) -> None:
    if user_action == "Undo":
        try:
            return user_cmd_storage.undo()
        except IndexError:
            print("No action in history")
            return None

    try:
        action = ACTIONS.dispatch(user_action)
    except ValueError:
        print("Unknown command")
        return None

    try:
        args = to_int(args)
    except ValueError:
        print("Your arguments must be integer")
        return None

    try:
        user_cmd_storage.apply(action(*args))
    except IndexError as error:
        print(error)


def main() -> None:
    print(START_MESSAGE)
    user_cmd_storage = PerformedCommandStorage([], Stack(None))
    while True:
        user_command = input("Enter your command with args: \n")
        user_action, args = parse_args(user_command)

        if user_action == "Exit":
            break
        elif user_action == "Show":
            print(user_cmd_storage.storage)
        else:
            do_action(user_cmd_storage, user_action, args)


if __name__ == "__main__":
    main()
