import sys
class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class WithSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
a = WithDict(1, 2)
b = WithSlots(1, 2)
print(sys.getsizeof(a))           # ~48 байт
print(sys.getsizeof(a.__dict__))  # ~232 байт (словарь!)
print(sys.getsizeof(b))           # ~56 байт (нет __dict__)
# На 1 млн объектов: ~120 МБ vs ~48 МБ
