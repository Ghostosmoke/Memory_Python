import gc

# Все живые объекты в памяти
all_objs = gc.get_objects()
print(f"Объектов в памяти: {len(all_objs)}")

# Кто ссылается на объект (referrers)
lst = [1, 2, 3]
referrers = gc.get_referrers(lst)
print(f"Ссылаются на lst: {len(referrers)}")

# На что ссылается объект (referents)
d = {'a': [1,2], 'b': {3,4}}
referents = gc.get_referents(d)
print(f"lst ссылается на: {referents}")

# Отладка утечек
gc.set_debug(gc.DEBUG_LEAK)
# gc.DEBUG_LEAK = DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE
# | DEBUG_SAVEALL
gc.collect()
# Выводит инфо о недостижимых объектах
