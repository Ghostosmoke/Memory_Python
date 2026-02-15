import weakref

# Коллбэк при удалении объекта
class Sensor:
    def __init__(self, name):
        self.name = name

def on_delete(ref):
    print(f"Сенсор удалён!")

s = Sensor("temperature")
ref = weakref.ref(s, on_delete)  # коллбэк как второй аргумент
del s  # → выведет "Сенсор удалён!"

# WeakSet — множество со слабыми ссылками
observers = weakref.WeakSet()

class Observer:
    def update(self): pass

obs1 = Observer()
obs2 = Observer()
observers.add(obs1)
observers.add(obs2)
print(len(observers))  # 2
del obs1
print(len(observers))  # 1 — автоматически!
