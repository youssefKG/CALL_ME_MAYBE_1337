import asyncio
import time


async def worker(worker_id, delay):
    print(f"Worker {worker_id} starting...")
    # Pause without freezing the entire script
    await asyncio.sleep(delay)
    print(f"Worker {worker_id} finished after {delay}s!")


async def hello(time: int):
    while True:
        await asyncio.sleep(3)
        print("hello")


async def test_one():
    while True:
        await asyncio.sleep(1)
        print("test one")


async def test():
    await asyncio.gather(hello(3), test_one())


def main():
    asyncio.run(test())
    print("main")


if __name__ == "__main__":
    start_time = time.perf_counter()
    # Start the event loop and run main
    main()
