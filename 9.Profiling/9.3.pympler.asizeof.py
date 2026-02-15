from pympler import asizeof
import sys

# sys.getsizeof — только сам объект (неполный)
d = {'key': [1, 2, 3, 4, 5]}
print(sys.getsizeof(d))        # 232 (только dict!)
print(sys.getsizeof(d['key'])) # 120 (только list!)

# asizeof — рекурсивный обход (реальный размер)
print(asizeof.asizeof(d))      # ~600+ (всё вместе)

# Подробный отчёт
asizeof.asizeof(d, detail=1)

# Сравнение нескольких объектов
class A:
    def __init__(self): self.data = list(range(100))

class B:
    __slots__ = ('data',)
    def __init__(self): self.data = list(range(100))

a, b = A(), B()
print(asizeof.asizeof(a))      # больше (есть __dict__)
print(asizeof.asizeof(b))      # меньше (~на 40–50%)
