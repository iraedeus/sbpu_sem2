from typing import Callable, Generic, Optional, Type, TypeVar

T = TypeVar("T")


class AlreadyExistError(Exception):
    pass


class Registry(Generic[T]):
    def __init__(self, default: Optional[Type[T]]) -> None:
        self.classes: dict[str, Type[T]] = dict()
        self.default: Optional[Type[T]] = default

    def register(self, name: str) -> Callable[[Type[T]], Type[T]]:
        def inner(cls: Type[T]) -> Type[T]:
            if name not in self.classes:
                self.classes[name] = cls
                return cls
            else:
                raise AlreadyExistError("This name of class already exist in registry")

        return inner

    def dispatch(self, name: str) -> Type[T]:
        if name in self.classes:
            return self.classes[name]
        elif self.default is not None:
            return self.default
        else:
            raise ValueError("This class is unknown")


if __name__ == "__main__":
    class ParentClass:
        pass


    parent = Registry[ParentClass](default=None)


    @parent.register(name="AVL")
    class AVLTree(ParentClass):
        pass


    @parent.register(name="Treap")
    class CartesianTree(ParentClass):
        pass


    @parent.register(name="Smh")
    class SomethingElse(ParentClass):
        pass

    user_choice = input("Select the class whose object you want to create: \n" "Available: AVL, Treap, Smh \n")

    user_class = parent.dispatch(user_choice)
    print(user_class())
