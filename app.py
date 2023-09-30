import httpx
from threading import Thread
import asyncio
import requests
import aiohttp
import time
import functools
import time
import resource # Not run in Windows (use docker)

# Config
times = 1000
timeout = 30
url = "https://chatgptdemo.net/"
# url = "http://example.com/"

# Memory profiler
def timer_memory(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def timer_memory(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        value = func(*args, **kwargs)
        delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs - mem: {delta_mem}")
        return value
    return timer_memory
def async_timer_memory(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    async def timer_memory(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        value = await func(*args, **kwargs)
        delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs - mem: {delta_mem}")
        return value
    return timer_memory


#
# Sync
#
# Test 1000 requests thread
@timer_memory
def thread_requests():
    def get():
        r = requests.get(url, timeout=timeout)
        
    threads = []
    for i in range(times):
        t = Thread(target=get)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
@timer_memory
def thread_httpx():
    def get():
        with httpx.Client() as client:
            r = client.get(url, timeout=timeout)
    
    threads = []
    for i in range(1000):
        t = Thread(target=get)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
@timer_memory
def thread_httpx_http2():
    def get():
        with httpx.Client(http2=True) as client:
            r = client.get(url, timeout=timeout)
    
    threads = []
    for i in range(1000):
        t = Thread(target=get)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


#
# Async
#
# Test 1000 requests asyncio
async def aiohttp_async(client):
    async with client.get(url) as response:
        html = await response.text()
async def httpx_async(client):
    r = await client.get(url, timeout=timeout)

@async_timer_memory
async def test_async_aiohttp():
    conn = aiohttp.TCPConnector(limit=times)
    timeout_ = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout_) as session:
        await asyncio.gather(*[aiohttp_async(session) for _ in range(times)])
@async_timer_memory
async def test_async_httpx():
    limits = httpx.Limits(max_connections=times)
    async with httpx.AsyncClient(limits=limits) as client:
        await asyncio.gather(*[httpx_async(client) for _ in range(times)])
@async_timer_memory
async def test_async_httpx_http2():
    limits = httpx.Limits(max_connections=times)
    async with httpx.AsyncClient(limits=limits, http2=True) as client:
        await asyncio.gather(*[httpx_async(client) for _ in range(times)])



# Run
# asyncio.run(test_async_httpx_http2())
# asyncio.run(test_async_httpx())
asyncio.run(test_async_aiohttp())

# thread_requests()
# thread_httpx()
# thread_httpx_http2()

# docker run --name test -it -v ${PWD}:/app:rw python:3.11.4-slim-bullseye  /bin/bash