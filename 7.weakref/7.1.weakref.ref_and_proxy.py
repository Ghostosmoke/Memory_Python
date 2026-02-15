import weakref

class Node:
    def __init__(self, val):
        self.val = val

obj = Node(42)
# Слабая ссылка — НЕ увеличивает refcount
ref = weakref.ref(obj)
print(ref())        # <__main__.Node object at 0x...> — объект жив
print(ref().val)    # 42
del obj
print(ref())        # None — объект удалён!

# Proxy — прозрачный доступ к атрибутам
obj2 = Node(99)
proxy = weakref.proxy(obj2)
print(proxy.val)    # 99 — как обычный атрибут
del obj2
# proxy.val → ReferenceError!
