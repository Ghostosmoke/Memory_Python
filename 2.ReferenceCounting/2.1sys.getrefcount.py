import sys
a = []
print(sys.getrefcount(a))  # 2 (a + временная в getrefcount)
b = a
print(sys.getrefcount(a))  # 3 (a, b + временная)
del b
print(sys.getrefcount(a))  # 2 снова

