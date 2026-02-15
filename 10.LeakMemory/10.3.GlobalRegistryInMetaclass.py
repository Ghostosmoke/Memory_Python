import weakref

# УТЕЧКА: метакласс держит все классы навсегда
class RegistryMeta(type):
    _registry = {}  # ← strong refs → утечка!
    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, ns)
        mcs._registry[name] = cls  # никогда не удаляется
        return cls

# РЕШЕНИЕ: слабые ссылки в реестре
class SafeRegistryMeta(type):
    _registry = weakref.WeakValueDictionary()  # ← слабые!
    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, ns)
        mcs._registry[name] = cls
        return cls

class MyModel(metaclass=SafeRegistryMeta):
    pass

print(SafeRegistryMeta._registry)  # {'MyModel': <class '__main__.MyModel'>}
