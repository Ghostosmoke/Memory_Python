import weakref

# ПРОБЛЕМА: цикл удерживает оба объекта
class Parent:
    def __init__(self):
        self.child = None

class Child:
    def __init__(self, parent):
        self.parent = parent  # ← strong ref → цикл!

# РЕШЕНИЕ: слабая ссылка на родителя
class ChildFixed:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)  # ← weak ref
    
    @property
    def parent(self):
        return self._parent()  # None если удалён

p = Parent()
c = ChildFixed(p)
p.child = c
del p  # родитель удалится! (нет strong ref от ребёнка)
print(c.parent)  # None
