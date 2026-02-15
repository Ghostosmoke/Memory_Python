import sys
data = bytearray(b'Hello, World! ' * 1000)

# Срез bytearray — КОПИРУЕТ данные
slice1 = data[0:7000]
print(sys.getsizeof(slice1))  # 7000+ байт (копия!)

# memoryview — ССЫЛКА на тот же буфер (zero-copy)
mv = memoryview(data)
slice2 = mv[0:7000]
print(sys.getsizeof(slice2))  # ~200 байт (только метаданные!)

# Работа с memoryview
print(bytes(mv[0:5]))         # b'Hello'
mv[0:5] = b'Privet'           # изменяем оригинал!
print(data[:6])               # bytearray(b'Privet')

# Полезно при работе с сетевыми буферами,
# файлами, NumPy массивами
