import sys
from collections import namedtuple
from dataclasses import dataclass

# 1. dict — максимально гибко, максимально дорого
d = {'x': 1.0, 'y': 2.0, 'z': 3.0}
print(sys.getsizeof(d))  # ~232 байт

# 2. __slots__ — убираем __dict__
class Vec3Slots:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

# 3. namedtuple — иммутабельно, tuple под капотом
Vec3NT = namedtuple('Vec3', ['x', 'y', 'z'])

# 4. dataclass(slots=True) — лучшее из обоих миров
@dataclass(slots=True)
class Vec3DC:
    x: float; y: float; z: float

v1 = Vec3Slots(1, 2, 3)
v2 = Vec3NT(1, 2, 3)
v3 = Vec3DC(1, 2, 3)
print(sys.getsizeof(v1))  # ~56 байт
print(sys.getsizeof(v2))  # ~72 байт
print(sys.getsizeof(v3))  # ~56 байт
