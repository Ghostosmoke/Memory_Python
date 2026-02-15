import threading
import sys
# До Python 3.13: GIL делает потоки бесполезными для CPU
# Python 3.13+: экспериментальный режим без GIL
counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # НЕ потокобезопасно без GIL!

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # < 400_000 в Python 3.13 без GIL!
# С GIL (3.12-): около 400_000 (GIL "случайно" помогает)
# Проверить режим без GIL:
print(sys._is_gil_enabled())  # True/False (Python 3.13+)

# Потокобезопасная версия:
lock = threading.Lock()
def safe_increment():
    global counter
    with lock:
        counter += 1
