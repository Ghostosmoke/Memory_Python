import sys
import array

# list хранит PyObject* (указатели) → каждый int = 28 байт
lst = list(range(1000))
print(sys.getsizeof(lst))  # ~8056 байт (только указатели!)
# + 1000 * 28 байт для самих int → ~36 КБ суммарно

# array.array — компактное хранение чисел
arr = array.array('i', range(1000))  # 'i' = signed int (4 байта)
print(sys.getsizeof(arr))  # ~4064 байт — в 9× меньше!

# Типы: 'b'=int8, 'h'=int16, 'i'=int32,
# 'l'=int64, 'f'=float32, 'd'=float64

# Операции те же что у list:
arr.append(1000)
arr.extend([1001, 1002])
print(arr[0])  # 0
