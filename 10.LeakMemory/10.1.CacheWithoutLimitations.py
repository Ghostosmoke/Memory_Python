import functools
import weakref

# ПЛОХО: бесконечный рост кеша
cache = {}  # никогда не очищается!

def get_user(user_id):
    if user_id not in cache:
        cache[user_id] = {"id": user_id, "data": "..."}
    return cache[user_id]

# ЛУЧШЕ 1: lru_cache с ограничением
@functools.lru_cache(maxsize=1000)
def get_user_lru(user_id):
    return {"id": user_id, "data": "..."}

# ЛУЧШЕ 2: WeakValueDictionary — само очищается
class User:
    def __init__(self, uid): self.uid = uid

user_cache = weakref.WeakValueDictionary()

def get_user_weak(uid):
    if uid not in user_cache:
        user_cache[uid] = User(uid)
    return user_cache[uid]
