import gc
gc.set_debug(gc.DEBUG_SAVEALL)
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
    def __del__(self):
        pass  # __del__ + цикл → утечка!
a = Node(1)
b = Node(2)
a.next = b
b.next = a  # цикл!
del a, b
gc.collect()
# Объекты не удалены — в gc.garbage!
print(len(gc.garbage))  # > 0
# Решение: использовать weakref вместо __del__
