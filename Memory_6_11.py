"""
    1.Запуск скрипта, создающего 1 миллион объектов класса с __dict__ и 1 миллион объектов с __slots__. Вывод в консоль суммарного потребления памяти через tracemalloc. Ожидаемый результат: разница примерно в 2 раза (например, 120 МБ против 48 МБ).
    
    2.Показать ошибку при попытке присвоить новый атрибут объекту со слотами (AttributeError). Показать успешное создание экземпляра dataclass(slots=True) и замер его размера через sys.getsizeof.
    
    3.Создание цикла «Родитель-Ребёнок» с обычными ссылками → показ через objgraph, что объекты живы после del. Замена ссылки на родителя на weakref.ref → повторный gc.collect() → объекты исчезают. Демонстрация WeakValueDictionary: добавление объекта, удаление сильной ссылки, проверка наличия ключа в словаре (становится False).
    
    4.Замер памяти списка из 1000 целых чисел vs array.array('i') из 1000 чисел. Создание memoryview большого байт-массива, изменение данных через view, показ изменения исходных данных.
    
    5.Запуск скрипта с утечкой (растущий список). Снятие двух снапшотов tracemalloc до и после роста. Вывод разницы (compare_to), показывающей строку кода, где создаются объекты.
    
    6.Показать статичную картинку Flame Graph из memray, где видно «горячую» функцию. Объяснить, как читать график: ширина прямоугольника пропорциональна потреблению памяти.
    
    7.Показать код с глобальным списком ошибок, который растёт. Показать, как sys.exc_info() или сохранение исключения в переменную удерживает локальные переменные функции в памяти (через gc.get_referrers).
    
    8.Устный пример: код с __del__, который печатает сообщение. В CPython сообщение выйдет сразу после del, в PyPy — в случайный момент при сборке мусора.
    
    9.Показать вывод функции sys._is_gil_enabled() (доступна в 3.13+). Упомянуть, что в будущем возможно выделение простых объектов на стеке, а не в куче.
    
"""
"""
=============================================================
  Python Memory Management — Полная демонстрация
=============================================================
Запуск: python memory_demo.py
Зависимости: pip install objgraph weakref (weakref встроен)
             pip install memray  (опционально, для секции 6)
=============================================================
"""

import sys
import gc
import array
import weakref
import tracemalloc
from dataclasses import dataclass


# ──────────────────────────────────────────────────────────
# Секция 1. __dict__ vs __slots__: потребление памяти
# ──────────────────────────────────────────────────────────
def section1_slots_vs_dict():
    print("\n" + "="*60)
    print("СЕКЦИЯ 1: __dict__ vs __slots__ — потребление памяти")
    print("="*60)

    class WithDict:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class WithSlots:
        __slots__ = ("x", "y", "z")

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    N = 1_000_000

    # Замер __dict__
    tracemalloc.start()
    dict_objects = [WithDict(i, i * 2, i * 3) for i in range(N)]
    snap_dict = tracemalloc.take_snapshot()
    stats_dict = snap_dict.statistics("lineno")
    mem_dict = sum(s.size for s in stats_dict)
    tracemalloc.stop()

    # Замер __slots__
    tracemalloc.start()
    slot_objects = [WithSlots(i, i * 2, i * 3) for i in range(N)]
    snap_slots = tracemalloc.take_snapshot()
    stats_slots = snap_slots.statistics("lineno")
    mem_slots = sum(s.size for s in stats_slots)
    tracemalloc.stop()

    print(f"  Объектов: {N:,}")
    print(f"  Память с __dict__  : {mem_dict / 1024 / 1024:.1f} МБ")
    print(f"  Память с __slots__ : {mem_slots / 1024 / 1024:.1f} МБ")
    ratio = mem_dict / mem_slots if mem_slots else 0
    print(f"  Соотношение        : {ratio:.1f}x  (ожидается ~2x)")

    # Очистка
    del dict_objects, slot_objects


# ──────────────────────────────────────────────────────────
# Секция 2. AttributeError + dataclass(slots=True)
# ──────────────────────────────────────────────────────────
def section2_slots_attr_error():
    print("\n" + "="*60)
    print("СЕКЦИЯ 2: AttributeError и dataclass(slots=True)")
    print("="*60)

    class Point:
        __slots__ = ("x", "y")

        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Point(1, 2)
    print(f"  Point(1, 2) создан, x={p.x}, y={p.y}")

    print("  Попытка присвоить p.z = 99 ...")
    try:
        p.z = 99  # type: ignore
    except AttributeError as e:
        print(f"  ✗ AttributeError: {e}")

    # dataclass с slots=True (Python 3.10+)
    try:
        @dataclass(slots=True)
        class Vector:
            x: float
            y: float
            z: float

        v = Vector(1.0, 2.0, 3.0)
        print(f"\n  dataclass(slots=True) Vector создан: {v}")
        print(f"  sys.getsizeof(v)  = {sys.getsizeof(v)} байт")
        print(f"  hasattr __dict__  = {hasattr(v, '__dict__')}")
    except TypeError:
        print("  ℹ  dataclass(slots=True) требует Python 3.10+")


# ──────────────────────────────────────────────────────────
# Секция 3. Циклические ссылки и weakref
# ──────────────────────────────────────────────────────────
def section3_weakref():
    print("\n" + "="*60)
    print("СЕКЦИЯ 3: Циклические ссылки и weakref")
    print("="*60)

    # 3a. Цикл с обычными ссылками
    class Parent:
        def __init__(self, name):
            self.name = name
            self.child = None

        def __repr__(self):
            return f"Parent({self.name!r})"

    class Child:
        def __init__(self, name, parent):
            self.name = name
            self.parent = parent  # сильная ссылка → цикл

        def __repr__(self):
            return f"Child({self.name!r})"

    parent = Parent("Alice")
    child = Child("Bob", parent)
    parent.child = child

    try:
        import objgraph
        print("  [objgraph] объектов Parent до del:", objgraph.count("Parent"))
    except ImportError:
        print("  (objgraph не установлен, пропускаем визуализацию)")
        objgraph = None

    del parent, child
    gc.collect()

    if objgraph:
        print("  [objgraph] объектов Parent после del + gc.collect():",
              objgraph.count("Parent"))
        print("  → При цикле объекты остаются до вызова gc !")

    print()

    # 3b. weakref вместо сильной ссылки
    class ParentWeak:
        def __init__(self, name):
            self.name = name
            self.child = None

    class ChildWeak:
        def __init__(self, name, parent):
            self.name = name
            self.parent = weakref.ref(parent)  # слабая ссылка

    pw = ParentWeak("Alice")
    cw = ChildWeak("Bob", pw)
    pw.child = cw

    ref_to_parent = weakref.ref(pw)
    print(f"  weakref живёт: {ref_to_parent() is not None}")

    del pw, cw
    gc.collect()
    print(f"  weakref после del + gc.collect(): {ref_to_parent()}")
    print("  → None: объект освобождён без цикличной задержки")

    print()

    # 3c. WeakValueDictionary
    print("  WeakValueDictionary:")

    class Obj:
        def __init__(self, val):
            self.val = val

    registry = weakref.WeakValueDictionary()
    strong = Obj(42)
    registry["key"] = strong
    print(f"  'key' в registry: {'key' in registry}  (ожидается True)")

    del strong
    gc.collect()
    print(f"  'key' в registry: {'key' in registry}  (ожидается False)")


# ──────────────────────────────────────────────────────────
# Секция 4. list vs array.array + memoryview
# ──────────────────────────────────────────────────────────
def section4_array_memoryview():
    print("\n" + "="*60)
    print("СЕКЦИЯ 4: list vs array.array, memoryview")
    print("="*60)

    N = 1000
    py_list = list(range(N))
    arr = array.array("i", range(N))

    print(f"  list из {N} int   : sys.getsizeof = {sys.getsizeof(py_list):,} байт")
    print(f"  array.array('i')  : sys.getsizeof = {sys.getsizeof(arr):,} байт")
    ratio = sys.getsizeof(py_list) / sys.getsizeof(arr)
    print(f"  Список ~в {ratio:.1f}x больше array")

    print()

    # memoryview
    data = bytearray(b"Hello, World!")
    view = memoryview(data)

    print(f"  Исходные данные    : {bytes(data)}")
    view[0:5] = b"Privet"[:5]          # меняем через view — без копирования
    print(f"  После view[0:5]=.. : {bytes(data)}")
    print("  → memoryview изменил исходный bytearray без копирования")


# ──────────────────────────────────────────────────────────
# Секция 5. tracemalloc: обнаружение утечки
# ──────────────────────────────────────────────────────────
def section5_tracemalloc_leak():
    print("\n" + "="*60)
    print("СЕКЦИЯ 5: Обнаружение утечки через tracemalloc")
    print("="*60)

    # Функция-«утечка» — растущий список в замыкании / модуле
    _leak_storage: list = []

    def leaky_function():
        """Имитируем утечку: добавляем большие объекты в глобальный список."""
        for _ in range(50_000):
            _leak_storage.append("x" * 100)   # ← строка-виновник

    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    leaky_function()

    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()

    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("  Топ-3 строки по росту памяти:")
    for stat in top_stats[:3]:
        print(f"    {stat}")

    print("\n  → Строка с 'x' * 100 показана как источник роста")


# ──────────────────────────────────────────────────────────
# Секция 6. Memray Flame Graph (текстовое пояснение)
# ──────────────────────────────────────────────────────────
def section6_memray_flamegraph():
    print("\n" + "="*60)
    print("СЕКЦИЯ 6: Memray Flame Graph")
    print("="*60)
    print("""
  Запуск профилирования:
      memray run -o output.bin my_script.py
      memray flamegraph output.bin          # → HTML-файл

  Как читать Flame Graph:
  ┌──────────────────────────────────────────────────────────┐
  │                    main()                                 │
  │        ┌──────────────────┐  ┌───────────┐              │
  │        │  process_data()  │  │  load()   │              │
  │        │ (широкий = много │  │ (узкий)   │              │
  │        │  памяти здесь)   │  │           │              │
  │        └──────────────────┘  └───────────┘              │
  └──────────────────────────────────────────────────────────┘

  • Ширина прямоугольника ∝ объёму выделенной памяти
  • «Горячая» функция — самый широкий блок на своём уровне
  • Цвет: красный/оранжевый = больше памяти
  • Клик на блок → фильтрация по этому стеку вызовов
    """)


# ──────────────────────────────────────────────────────────
# Секция 7. Исключения и утечки через exc_info
# ──────────────────────────────────────────────────────────
def section7_exception_leak():
    print("\n" + "="*60)
    print("СЕКЦИЯ 7: Исключения и утечки через sys.exc_info()")
    print("="*60)

    error_log: list = []   # глобальный список ошибок — растёт

    def risky(n):
        big_local = list(range(n))   # локальная переменная
        try:
            if n > 5:
                raise ValueError(f"n={n} слишком большой")
        except ValueError as e:
            # ← УТЕЧКА: `e` (и через трейсбек) держит `big_local` в памяти!
            error_log.append(e)
            # Чтобы избежать утечки, нужно: error_log.append(str(e))

    for i in range(10):
        risky(i)

    print(f"  error_log содержит {len(error_log)} исключений")

    # Показываем, что исключение удерживает фрейм
    import gc as _gc
    exc = error_log[-1]
    referrers = _gc.get_referrers(exc)
    print(f"  gc.get_referrers(exc) нашёл {len(referrers)} объектов-хозяев")
    print("  → traceback → frame → locals → big_local живёт в памяти!")

    print("""
  Решение:
      error_log.append(str(e))          # сохранять строку, не объект
      # или после блока except:
      del e                             # явно удалить переменную
    """)


# ──────────────────────────────────────────────────────────
# Секция 8. __del__ и финализаторы
# ──────────────────────────────────────────────────────────
def section8_del_finalizer():
    print("\n" + "="*60)
    print("СЕКЦИЯ 8: __del__ и финализаторы")
    print("="*60)

    class Resource:
        def __init__(self, name):
            self.name = name
            print(f"  [__init__] Resource({name!r}) создан")

        def __del__(self):
            print(f"  [__del__]  Resource({self.name!r}) уничтожен")

    r = Resource("db_connection")
    print("  del r ...")
    del r
    # В CPython: сразу увидим [__del__] (подсчёт ссылок → 0)
    # В PyPy/Jython: момент вызова __del__ не определён

    print("""
  CPython  → __del__ вызывается сразу при del (ref-counting)
  PyPy     → __del__ вызывается в момент GC (непредсказуемо)
  Вывод    → не полагайтесь на __del__ для освобождения ресурсов;
             используйте context managers (with / __exit__)
    """)


# ──────────────────────────────────────────────────────────
# Секция 9. GIL и Python 3.13+
# ──────────────────────────────────────────────────────────
def section9_gil():
    print("\n" + "="*60)
    print("СЕКЦИЯ 9: GIL и Python 3.13+")
    print("="*60)

    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")

    if version >= (3, 13):
        try:
            gil_enabled = sys._is_gil_enabled()   # type: ignore[attr-defined]
            print(f"  sys._is_gil_enabled() = {gil_enabled}")
            if not gil_enabled:
                print("  → Запущено в режиме Free-Threaded (GIL отключён)!")
            else:
                print("  → GIL активен (стандартный режим CPython)")
        except AttributeError:
            print("  sys._is_gil_enabled() недоступна в этой сборке")
    else:
        print("  sys._is_gil_enabled() доступна только в Python 3.13+")
        print("  (текущая версия ниже 3.13)")

    print("""
  Дорожная карта памяти в Python:
  • 3.12 → улучшена арена аллокатора (pymalloc)
  • 3.13 → опциональный Free-Threaded режим (--disable-gil)
  • Будущее → возможно выделение простых объектов на стеке (escape analysis),
              что устранит нагрузку на кучу для short-lived объектов
    """)



# ──────────────────────────────────────────────────────────
# Точка входа
# ──────────────────────────────────────────────────────────
def main():
    print("\n" + "★"*60)
    print("  Python Memory Management — Демонстрационный скрипт")
    print("★"*60)

    section1_slots_vs_dict()
    section2_slots_attr_error()
    section3_weakref()
    section4_array_memoryview()
    section5_tracemalloc_leak()
    section6_memray_flamegraph()
    section7_exception_leak()
    section8_del_finalizer()
    section9_gil()
    section10_qr_slide()

    print("\n" + "★"*60)
    print("  Все секции выполнены!")
    print("★"*60 + "\n")


if __name__ == "__main__":
    main()
