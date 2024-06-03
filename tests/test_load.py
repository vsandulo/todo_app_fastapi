import asyncio
import aiohttp
from faker import Faker
import time
from decorators import timeit

fake = Faker()

async def create_todos(session, url, num_todos):
    todos = [
        {
            "title": fake.sentence(),
            "body": fake.text(),
            "user_id": fake.random_int(min=1, max=100)
        } for _ in range(num_todos)
    ]
    await asyncio.gather(*(session.post(url, json=todo) for todo in todos))

@timeit
async def measure_get_todos(session, url, duration=30):
    start_time = time.time()
    request_count = 0

    while time.time() - start_time < duration:
        async with session.get(url) as response:
            await response.read()
            request_count += 1

    elapsed = time.time() - start_time
    print(f"Середній час запиту-відповіді: {elapsed / request_count:.5f} сек/запит")

async def load_test(url, num_todos):
    async with aiohttp.ClientSession() as session:
        await create_todos(session, url + "/todos", num_todos)
        
        await measure_get_todos(session, url + "/todos")

if __name__ == "__main__":
    for num in [10, 100, 1000, 10000, 100000]:
        print(f"Тестуємо {num} Todos")
        asyncio.run(load_test("http://localhost:8000", num))
