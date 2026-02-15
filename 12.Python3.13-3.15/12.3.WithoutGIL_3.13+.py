# python3.13t script.py (t = free-threaded)
# или: python --disable-gil script.py

import sys
import threading

# Проверить режим:
# print(sys._is_gil_enabled()) # False в free-threaded

# Теперь реальный параллелизм для CPU-задач:
import multiprocessing

def cpu_bound(n):
    return sum(i * i for i in range(n))

# Раньше (с GIL): потоки не ускоряли CPU задачи
# Теперь (без GIL): реальное ускорение!
# НО: нужна синхронизация!

# Потокобезопасные структуры (3.13+):
# - queue.Queue (была и раньше)
# - threading.Lock, RLock, Condition

# Небезопасны без Lock:
# - dict, list операции (были atomics через GIL!)
# - счётчики, флаги

shared = []
lock = threading.Lock()

def safe_append(val):
    with lock:
        shared.append(val)
