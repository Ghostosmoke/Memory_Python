import gc
import sys

# ПРОБЛЕМА: замыкание держит фрейм → цикл
def make_closure():
    local_data = list(range(100000))  # 800 КБ
    def inner():
        return local_data[0]  # захватывает local_data
    return inner

f = make_closure()
# local_data жив пока жив f — ОК, ожидаемо

# СКРЫТАЯ ПРОБЛЕМА: трейсбек держит фрейм
try:
    1 / 0
except ZeroDivisionError as e:
    exc = e  # ← фрейм (locals!) жив пока жив exc!

# РЕШЕНИЕ:
try:
    1 / 0
except ZeroDivisionError as e:
    exc = str(e)  # сохраняем только строку
# или используй 'from None'
