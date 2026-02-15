a = [1, 2, 3]
b = a          # та же ссылка
print(id(a) == id(b))  # True — один объект
print(hex(id(a)))      # адрес в памяти, напр. 0x7f3a1b2c3d40
c = [1, 2, 3]  # новый объект
print(id(a) == id(c))  # False
