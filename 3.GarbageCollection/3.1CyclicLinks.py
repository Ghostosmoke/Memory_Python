import gc
# Создаём цикл: a → b → a
a = {}
b = {}
a['other'] = b
b['other'] = a
del a, b
# refcount не 0, но объекты недостижимы!
collected = gc.collect()  # GC находит и удаляет
print(f"Собрано объектов: {collected}")  # 2
