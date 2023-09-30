# Docker command
docker run --name test -it -v ${PWD}:/app:rw python:3.11.4-slim-bullseye  /bin/bash

# Results
## Chatgptdemo.net (https)
Finished 'test_async_httpx_http2' in 9 secs - mem: 90776
Finished 'test_async_httpx' in 21 secs - mem: 349428
Finished 'test_async_aiohttp' in 11 secs - mem: 618588

Finished 'thread_requests' in 12 secs - mem: 1154180
Finished 'thread_httpx' in 23 secs - mem: 1323808	
Finished 'thread_httpx_http2' in 38 secs - mem: 1327800


# Example.com (http)
Finished 'test_async_httpx_http2' in 14 secs - mem: 46904
Finished 'test_async_httpx' in 21 secs - mem: 36300
Finished 'test_async_aiohttp' in 3 secs - mem: 17176

Finished 'thread_requests' in 4 secs - mem: 57352
Finished 'thread_httpx' in 4 secs - mem: 724140
Finished 'thread_httpx_http2' in 4 secs - mem: 649764