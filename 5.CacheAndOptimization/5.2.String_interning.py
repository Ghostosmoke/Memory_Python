import sys
# Автоматический interning для «идентификаторов»
a = "hello"
b = "hello"
print(a is b)  # True (автоматически интернировано)
# Строки с пробелами — НЕ интернируются автоматически
c = "hello world"
d = "hello world"
print(c is d)  # False (зависит от реализации)
# Ручное интернирование
e = sys.intern("hello world")
f = sys.intern("hello world")
print(e is f)  # True — теперь один объект
