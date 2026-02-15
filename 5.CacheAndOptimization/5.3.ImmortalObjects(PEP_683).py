import sys
# None, True, False — бессмертные объекты
# refcount = 0xFFFFFFFF, никогда не удаляются
print(id(None))   # всегда один адрес
print(id(True))   # всегда один адрес
print(id(False))  # всегда один адрес
# Проверка: количество ссылок очень большое
print(sys.getrefcount(None))   # огромное число
print(sys.getrefcount(True))   # огромное число
