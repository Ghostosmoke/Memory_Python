import gc

# Python 3.13+: Incremental GC по умолчанию
# Паузы <1мс вместо потенциальных 10–100мс в 3.12

# Проверить параметры GC:
print(gc.get_threshold())
# (700, 10, 10) — порог инкрементального сбора

# Настройка:
gc.set_threshold(1000, 15, 15)

# Демонстрация разницы (псевдокод):
# Python 3.12: Full GC pause = O(живые объекты)
# Python 3.13: Incremental = O(молодые объекты) per step

# Отслеживать статистику GC:
stats = gc.get_stats()
for gen, s in enumerate(stats):
    print(f"Gen{gen}: collections={s['collections']}, "
          f"collected={s['collected']}")
