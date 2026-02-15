import sys
# pymalloc работает для объектов ≤ 512 байт
# Блоки: 8, 16, 24, ... 512 байт (кратны 8)
# Запрос 9 байт → выделяется блок 16 байт (внутренняя фрагментация)
# Запрос 513 байт → уходит в системный malloc
small = b"x" * 9    # ≤512 → pymalloc, блок 16 байт
big   = b"x" * 600  # >512 → системный malloc
print(sys.getsizeof(small))  # 42
print(sys.getsizeof(big))    # 633
# Отладка аллокатора:
# PYTHONMALLOC=debug python script.py
# sys._debugmallocstats()  ← детальная статистика
