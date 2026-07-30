# from typing_extensions import Self

# from collections import defaultdict
from typing import TypeVar, Generic

# def_dict: defaultdict[str, None | str] = defaultdict(lambda: None)
# a = def_dict["name"]
# print(a)

# class A(str, Enum):
#     DEFAULT = "default"
#     NORMAL = "normal"


# def hello(*, name: str, a: int, b: int):
#     print(name, a, b)


# def test(*arg, **kwargs) -> None:
#     print(arg)
#     print(kwargs)


# class B(str):
#     def __new__(cls) -> Self:
#         instance = super().__new__(cls)
#         instance.name = "youssef"
#         return instance
#
#     def __init__(self) -> None:
#         pass
#
#
# b = B()
# print(b.name)


# test(10, 3, 4, 5)


# a = {"first_name": "youssef", "last_name": "taoussi"}
# match a:
#     case {"first_name": "youssef", **details}:
#         print("youssef", details)
#     case _:
#         pass
# class A:
# def __init__(self, name: str) -> None:
# self.name: str = name

# @override
# def __eq__(self, value: object) -> bool:
#     if id(self) == id(value):
#         return True
#     else:
#         return False

# @override
# def __hash__(self) -> int:
#    return id(self.name)


# c = A("amine")
#
# b = "string"
# a = 10
# d = {a: "number", b: "string", True: c}
# b = True
# c = True
# d = False
# print(id(c), id(b))


# UNPACKING

T = TypeVar("T")


class Number(Generic[T]):
    def __init__(self, lst: list[T]):
        self.lst: list[T] = lst

    def log(self) -> None:
        for item in self.lst:
            print(item)


a = Number[int]([1, 3, 4, 0.2])
a.log()
