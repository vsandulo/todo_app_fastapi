import asyncio
import time

def timeit(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} виконано за {end - start:.5f} секунд(у).")
        return result
    return wrapper
