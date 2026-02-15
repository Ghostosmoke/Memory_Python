# Python 3.13: экспериментальный copy-and-patch JIT
# Запуск: python --enable-experimental-jit script.py
# JIT снижает количество временных объектов:

def hot_loop(n):
    total = 0
    for i in range(n):
        total += i * i  # JIT: i остаётся в регистре (не PyObject!)
    return total

# Без JIT: каждый i, i*i → полноценный PyObject (28+ байт)
# С JIT: числа хранятся как C int (4 байта) пока возможно

# Проверить трассировку специализации (3.11+):
import sys

# python -X perf -c "..." — интеграция с Linux perf
# PYTHONPROFILEIMPORTTIME=1 — время импортов
# Статистика специализации (3.12+):
# python -X specialization=1 -c "..."
