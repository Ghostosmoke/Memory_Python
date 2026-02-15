# Поведение __del__ РАЗНОЕ в разных реализациях!
class Resource:
    def __init__(self, name):
        self.name = name
        print(f" Создан: {name}")
    def __del__(self):
        print(f" Удалён: {self.name}")

# CPython: детерминированное удаление (refcount)
r = Resource("файл")
del r  # СРАЗУ выведет "Удалён: файл"

# PyPy/Jython/IronPython: НЕ детерминировано!
# __del__ вызовется "когда-нибудь" при GC

# ПРАВИЛО: никогда не полагайся на __del__
# для освобождения ресурсов!

# ПРАВИЛЬНО: context manager
class SafeResource:
    def __enter__(self): return self
    def __exit__(self, *args):
        print("Освобождён!")  # детерминировано везде

with SafeResource() as r:
    pass  # "Освобождён!" — гарантировано
