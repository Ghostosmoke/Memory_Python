import weakref
class Good:
    __slots__ = ('x', '__weakref__')  # weakref явно!
class Bad:
    __slots__ = ('x',)  # weakref забыли
g = Good()
weakref.ref(g)  # OK
b = Bad()
# weakref.ref(b)  # → TypeError!
# Динамические атрибуты — тоже нельзя:
g.x = 10      # OK
# g.z = 99    # → AttributeError
# Pickle требует __getstate__/__setstate__:
class Pickled:
    __slots__ = ('x', 'y')
    def __getstate__(self): return (self.x, self.y)
    def __setstate__(self, s): self.x, self.y = s
