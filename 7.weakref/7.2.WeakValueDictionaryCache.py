import weakref

# Кеш с автоматической очисткой
cache = weakref.WeakValueDictionary()

class Image:
    def __init__(self, name):
        self.name = name

img = Image("photo.jpg")
cache["photo"] = img
print("photo" in cache)        # True
print(cache["photo"].name)    # photo.jpg
del img                       # удаляем единственную strong ref
import gc; gc.collect()
print("photo" in cache)       # False — автоматически очищено!

# WeakKeyDictionary — слабые ключи
wkd = weakref.WeakKeyDictionary()
key = Image("key.jpg")
wkd[key] = "metadata"
del key                       # запись исчезнет автоматически
