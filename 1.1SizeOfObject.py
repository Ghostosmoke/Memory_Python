import sys
x = 42
s = "hello"
lst = [1, 2, 3]
print(sys.getsizeof(x))    # 28 байт (int)
print(sys.getsizeof(s))    # 54 байт (str)
print(sys.getsizeof(lst))  # 88 байт (list — без вложенных!)
# id() == адрес PyObject_HEAD в CPython
print(id(x))   # например: 140712345678912
