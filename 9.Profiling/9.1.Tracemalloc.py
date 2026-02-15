import tracemalloc
tracemalloc.start()  # начинаем трекинг

# Код который хотим проверить
x = [dict(i=i, val=i*2) for i in range(10000)]
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics('lineno')

# Топ-3 по потреблению памяти
for stat in top[:3]:
    print(stat)
# example.py:5: size=3.7 MiB, count=30003, average=129 B

# Сравнение двух снимков — найти утечку
snap1 = tracemalloc.take_snapshot()
y = ["leak"] * 100000
snap2 = tracemalloc.take_snapshot()
diff = snap2.compare_to(snap1, 'lineno')
for stat in diff[:3]:
    print(stat)
