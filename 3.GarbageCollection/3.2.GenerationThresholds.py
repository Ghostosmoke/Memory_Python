import gc
# Текущие пороги
print(gc.get_threshold())  # (700, 10, 10)
# Gen0=700, Gen1=10, Gen2=10
# Посмотреть сколько объектов в каждом поколении
print(gc.get_count())  # например (245, 5, 1)
# Принудительно запустить GC
gc.collect(0)  # только Gen0
gc.collect(1)  # Gen0 + Gen1
gc.collect()   # все поколения
