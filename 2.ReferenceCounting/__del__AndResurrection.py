import gc
class Zombie:
    def __del__(self):
        print("Удаляюсь...")
        # Воскрешение — сохраняем ссылку на себя
        global survivor
        survivor = self   # ← объект НЕ удалится!
obj = Zombie()
del obj
gc.collect()
# Выведет "Удаляюсь..."
# но survivor всё ещё жив!
print(survivor)  # <__main__.Zombie object>
