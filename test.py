from typing_extensions import Self

from collections import defaultdict
from typing_extensions import override

def_dict: defaultdict[str, None | str] = defaultdict(lambda: None)
a = def_dict["name"]
print(a)

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
class A:
    def __init__(self, name: str) -> None:
        self.name: str = name

    # @override
    # def __eq__(self, value: object) -> bool:
    #     if id(self) == id(value):
    #         return True
    #     else:
    #         return False

    @override
    def __hash__(self) -> int:
        return id(self.name)


# c = A("amine")
#
# b = "string"
# a = 10
# d = {a: "number", b: "string", True: c}
# b = True
# c = True
# d = False
# print(id(c), id(b))
