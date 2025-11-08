# ⚙️ 一、传统 Django 是 WSGI 模型（同步阻塞）：

每个请求都占用一个线程；

如果请求里有阻塞操作（例如数据库查询、外部 HTTP 请求、文件 IO），该线程会卡住；当并发量上升时，线程数很快耗尽。

例如：

```python
def get_user(request):
    user = User.objects.get(id=1)  # 阻塞查询
    return JsonResponse({"name": user.name})
```

当数据库查询慢时，其他请求就得排队


# ⚙️ 二、asyncio 带来的改变

Python 的 asyncio 提供了 事件循环（event loop），让 I/O 操作异步化。

在 Django 3.1+ 中已经支持 ASGI（Asynchronous Server Gateway Interface）：

你可以写 async def view(request): ...

Django 不会为每个请求创建线程，而是通过事件循环在单线程内调度多个协程。

异步示例：

```python
async def async_view(request):
    await asyncio.sleep(1)  # 模拟IO操作
    return JsonResponse({"msg": "Hello, async!"})
```

当有多个请求进入时，一个请求 await 时，Django 会自动去执行别的请求逻辑。
→ 更好的 CPU 利用率 + 更高并发能力。


     ┌───────────────────────────┐
     │        Client (Browser)   │
     └────────────┬──────────────┘
                  │ HTTP Request
                  ▼
     ┌───────────────────────────┐
     │        Uvicorn Server     │
     │ (基于 asyncio 的事件循环)  │
     └────────────┬──────────────┘
                  │ 调用 ASGI 接口
                  ▼
     ┌───────────────────────────┐
     │  Django (ASGI 模式运行)    │
     │ async def view(request):  │
     │     await asyncio.sleep() │
     │     return response       │
     └───────────────────────────┘

- 每一个 HTTP 请求都会被事件循环调度成一个协程执行。

- 每个 GET 请求对应的协程是由 Django / ASGI 自动创建的，你不用自己为每个请求再定义单独的协程。

- Django async view 对每个http请求一个协程, 不同请求的协程之间天然并发


## Django 的运行模式（两种世界）

它实际上可以通过 两种运行模式 启动：

| 模式	| 协议	| 启动方式	| 运行特点 |
|-------|------|-----------|---------|
|同步模式| WSGI| python manage.py runserver|传统阻塞式，同步视图|
|异步模式| ASGI |uvicorn myproject.asgi:application|异步非阻塞，支持 WebSocket、async view|

```bash
uvicorn {name of your project}.asgi:application --host x.x.x.x --port xxxx
```

```bash
(env)$ uvicorn hello_async.asgi:application --reload
```
The *--reload* flag tells Uvicorn to watch your files for changes and reload if it finds any. That was probably self-explanatory.

### 在 Python 中，async 关键字只能出现在三种语法结构前：

|用法   |语法	| 作用|
|-|-|-|
|1️⃣ 定义异步函数	|async def func():	|定义一个 协程函数（coroutine function），调用时不会立即执行，而是返回一个 协程对象（需要 await 或事件循环执行）|
|2️⃣ 异步上下文管理器	|async with ...:|	用于管理异步资源（如连接池、网络会话），支持 __aenter__() / __aexit__() 异步方法|
|3️⃣ 异步迭代器	|async for ... in ...:	|用于异步遍历（如逐条读取网络数据流、数据库游标等）|


# ✅ 三、asyncio 核心机制

## 1️⃣ 协程（Coroutine）= 可暂停和恢复执行的函数。

用 async def 定义的函数。返回一个 协程对象，**不是立即执行**。

如果要执行，必须将协程对象交给事件循环来处理。

```python
async def foo():
    print("start")
    await asyncio.sleep(1)
    print("end")

coro = foo()   # 不会执行
asyncio.run(coro)  # 启动执行
```

## 2️⃣ await（等待）

await 关键字告诉解释器：“我这里要执行一个可能很耗时的操作（比如网络 I/O），先暂停我，让别人跑。”

```python
await asyncio.sleep(2)
```

不会阻塞整个线程，它只把当前协程的控制权还给事件循环；事件循环会调度其他协程继续运行；2 秒后再回来恢复执行。

await 后面只能加可等待对象：
- 协程对象
- task对象
- asyncio.future对象


## 3️⃣ 事件循环（Event Loop）：asyncio 的核心调度器

负责：

- 运行协程；
- 管理任务的挂起与恢复；
- 响应 I/O 事件（socket、网络等）。

```python
import asyncio

async def say(word, delay):
    await asyncio.sleep(delay)
    print(word)

async def main():
    await asyncio.gather(
        say("hello", 1),
        say("world", 2)
    )

asyncio.run(main())
```

``asyncio.run()`` 作用：

- 创建一个 事件循环（event loop）；

- 将 ``main()`` 这个协程对象封装成一个 主Task；

- 把它放进事件循环中运行。

#### 事件循环的行为：

- t=0: hello 等待 1s，world 等待 2s

- t=1: hello 输出，world 继续等待

- t=2: world 输出，全部完成

事件循环的功能可以被看作如下伪代码
```python
task = [main, say, say, ...]

while True:
    executable, done = findtask()

    for ready in executable:
        ready.run()

    for don in done:
        task.remove(don)
    
    if task == None:
        break
```
```python
async def task():
    pass

# old fashion style

# 生成或者获取一个事件循环
loop = asyncio.get_event_loop()
# 将任务task 放到任务列表
loop.run_until_complete(task)

# 等价于 new style Python 3.7+
asyncio.run( task() )
```

### uvloop

**python原生event_loop的一个高效替代。**

```bash
pip install uvloop
```

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# async def as usual....

# async run() 自动使用uvloop
asyncio.run(...)
```

#### 在asgi->uvicorn 内部就是使用了 uvloop



## 4️⃣ Task（任务）

Task 是包装协程的执行单元。事件循环通过 Task 管理协程的状态。

Task 把协程交给事件循环执行。

```python 
task = asyncio.create_task(foo()) # foo() is a Coroutine !
```

create_task() 将协程对象 foo() 封装成 Task，并注册进事件循环。

创建任务会立刻交给事件循环执行；类似线程池中的“线程对象”；

事件循环在空闲时会轮流执行这些任务。

## ✅ 总结一句话

asyncio 的核心机制是：用事件循环调度协程执行，通过 await 让出控制权，实现单线程并发。

- 一个 事件循环（loop） 中可以包含多个 Task。

- 每个 Task 负责执行一个 协程对象（async def 定义的函数的实例）。

- async def 的 main() 只是一个顶层协程，用来 await 多个子任务。

```    
             Event Loop         ←→ 一个进程里通常只有 1 个 loop
     ┌──────────────────────────┐
     │        Task 1            │← 每个任务包裹一个协程对象
     │    └── main() 协程 ─┘    |
     |        Task 2            |
     |    └── foo() 协程 ───┘   |
     |        Task 3            |
     |    └── bar() 协程 ───┘   |
     └──────────────────────────┘
       循环调度：谁可运行？谁在等待？
```

```python
import asyncio

async def task_fn(name):
    print(f"任务 {name} 开始")
    await asyncio.sleep(1)
    print(f"任务 {name} 结束")

async def main():
    print("main 启动")
    t1 = asyncio.create_task(task_fn("A"))
    t2 = asyncio.create_task(task_fn("B"))
    await t1
    await t2
    print("main 结束")

asyncio.run(main())
```

# 🧠 与 Django / Uvicorn 的关系

- Uvicorn 启动时会**自动创建事件循环**；

- 所以 Django 的 ASGI 环境 **已经有一个全局的 event loop**，不要手动 **asyncio.run()**

- Django（ASGI） 的异步视图 **（async def view）会注册到事件循环**；

- 当请求到来时，Uvicorn 把请求交给事件循环；

- Django 异步 view 在 await I/O（如数据库/HTTP 请求）时让出执行权；其他请求得以并发执行。


# 异步上下文管理器：

## 🧩 什么是上下文管理器（Context Manager）

上下文管理器是一个定义了特定方法的对象，用来**在代码块执行前后自动执行资源管理逻辑。**

最常见的例子：
```python
with open("file.txt", "r") as f:
    data = f.read()
```

这里 ``open()`` 返回的文件对象 f 就是一个上下文管理器。

进入 with 代码块前，会自动调用它的 ``__enter__()``；退出时无论是否异常，都会调用 ``__exit__()`` 来清理资源。

## 🧠 上下文管理协议（同步版）

实现上下文管理器需要实现两个魔术方法 __enter__() and __exit__()：
```python
class MyContext:
    def __enter__(self):
        print("进入上下文")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("离开上下文")
        # 返回 True 可以抑制异常，否则异常会向外传播
        return False

with MyContext() as obj:
    print("在上下文中")
```

## 🧪 常见用途

| 场景     | 上下文管理器                             |
| ------ | ---------------------------------- |
| 文件操作   | `open()` 自动关闭文件                    |
| 数据库连接  | `with connection.cursor() as cur:` |
| 线程/锁   | `with threading.Lock():`           |
| 资源清理   | 自动释放网络连接、关闭 socket                 |
| 临时状态更改 | 改环境变量、日志级别、浮点精度                    |

当你在异步编程中（asyncio）需要管理异步资源（比如异步数据库连接、网络请求、文件IO）时，就需要 异步上下文管理器。


## 异步上下文管理器的实现

``__aenter__()`` and ``__aexit__()``
```python
import asyncio

class AsyncExample:
    async def __aenter__(self):
        print("异步进入")
        await asyncio.sleep(1)
        # 打开一个数据库连接并返回
        return "资源"

    async def __aexit__(self, exc_type, exc, tb):
        print("异步退出")
        await asyncio.sleep(1)
        # 关闭数据库连接

async def main():
    async with AsyncExample() as res:
        print("使用", res)

asyncio.run(main())
```

## 🧩 异步上下文管理器的应用场景

| 场景      | 库                                     | 说明        |
| ------- | ------------------------------------- | --------- |
| 异步数据库连接 | `aiomysql`, `asyncpg`, `databases`    | 自动打开/关闭连接 |
| 异步文件    | `aiofiles.open()`                     | 异步读写文件    |
| 异步HTTP  | `aiohttp.ClientSession()`             | 自动关闭连接池   |
| 异步锁     | `asyncio.Lock()`                      | 异步任务互斥    |
| 异步事务    | 异步ORM（Tortoise ORM, SQLAlchemy async） | 自动提交/回滚事务 |

### example:
```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as resp:
            text = await resp.text()
            print(text[:100])

asyncio.run(main())
```
同样，``async with`` 也必须在协程中使用

# 四、并发执行多个协程

在 asyncio 中，一个事件循环（event loop）可以同时调度多个协程（coroutine）执行。

那么问题是：

如果我有多个 async 函数，想让它们“同时开始、一起等待完成”，应该怎么做？

这时就轮到 asyncio.gather() 上场了。

```
            ┌─────────────┐
foo()  ---> │             │
bar()  ---> │ asyncio.gather │ → 等待所有任务结束 → 返回结果列表
baz()  ---> │             │
            └─────────────┘
```

gather() 将每个协程包装成 Task, 把所有任务注册到事件循环, 当所有任务都完成后，返回它们的结果（按传入顺序）。

- gather() = 批量创建任务

- await = 等待这些任务全部完成，拿到最终结果
  
```python
await asyncio.gather() ≈ 自动帮你完成 “创建多个 task + 并发执行 + await 等待结果” 的过程。
```
## 与create_task()区别

|  |   |
|---|---|
| create_task() | 想自己控制任务执行、取消、后台运行 |
| gather() | 想并发运行多个任务并收集结果 |

#### 🔍 通常在 Django 异步视图或后台任务中：

- 若你只是“并发取结果” → 用 gather, 一次性创建并等待多个任务。

- 若你要“启动后台子任务” → 用 create_task, 手动创建任务，稍后自己 await。

```python
from django.http import JsonResponse
import asyncio
import httpx

async def fetch_json(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json()

async def my_view(request):
    url1 = "https://api.github.com"
    url2 = "https://api.python.org"
    data1, data2 = await asyncio.gather(fetch_json(url1), fetch_json(url2))
    return JsonResponse({"github": data1, "python": data2})
```

| 特性     | async for        | await asyncio.gather()     |
| ------ | ---------------- | -------------------------- |
| 执行顺序   | 顺序               | 并发                         |
| 每次迭代等待 | 是，每次迭代 await 前一个 | 在 gather 内部自动 await 所有任务完成 |
| 总耗时    | 累加每个协程耗时         | ≈ 最慢的那个协程耗时                |
| 使用场景   | 异步生成器、按顺序处理数据流   | 并发处理多个独立任务                 |


# 五、asyncio.Future 和 concurrent.futures.Future

- asyncio.Future

👉 是 协程世界的“占位符”。

表示“某个异步操作的结果还没准备好，但未来会有”。

通常由事件循环（event loop）调度。

只有协程或异步回调才能完成（set_result）。

- concurrent.futures.Future

👉 是 线程或进程执行结果的占位符。

当你用 ThreadPoolExecutor 或 ProcessPoolExecutor 提交任务时，返回的就是这个。

它代表某个任务在线程/进程中运行的结果。

由线程池管理，不属于 asyncio 事件循环。

| 特性          | `asyncio.Future`      | `concurrent.futures.Future`              |
| ----------- | --------------------- | ---------------------------------------- |
| 所属模块        | `asyncio`（协程模型）       | `concurrent.futures`（线程/进程池模型）           |
| 谁管理执行       | 事件循环（event loop）      | 线程池或进程池                                  |
| 谁设置结果       | 通常由 `asyncio` 内部协程    | 线程或进程执行完后自动设置                            |
| 可 `await` 吗 | ✅ 可以直接 `await future` | ❌ 不能直接 `await`（要用 `asyncio.wrap_future`） |
| 使用场景        | 异步 IO、协程              | CPU 密集型任务、多线程/多进程                        |
| 执行环境        | 单线程事件循环               | 多线程 / 多进程执行                              |


### 🔁 它们能不能混用？

可以，但要通过桥接函数。在 Django、FastAPI、或异步框架中，你想在异步函数中调用阻塞代码。

比如你在 asyncio 事件循环中想等待一个线程池任务的结果，需要这样：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 这是一个阻塞任务，且不支持直接用异步
def blocking_task():
    return "done from thread!"

async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        # 把 concurrent.futures.Future 转成 asyncio.Future
        result = await loop.run_in_executor(pool, blocking_task)
        print(result)

asyncio.run(main())
```



# 六、 others

## 异步可迭代器: async for

在异步环境中（例如网络、数据库、文件IO），我们经常需要逐个异步地获取数据项，
比如：

- 从数据库逐条异步读取结果；

- 从网络流（WebSocket、HTTP流）异步接收消息；

- 从异步生成器中逐步产生结果。

普通的 for 只能处理同步可迭代对象，不能 await。

而 async for 能在每次迭代时等待异步操作完成，**只能在协程对象中使用**。


| 特性    | 普通 `for`                         | `async for`                        |
| ----- | -------------------------------- | ---------------------------------- |
| 使用的协议 | 同步迭代协议 (`__iter__` / `__next__`) | 异步迭代协议 (`__aiter__` / `__anext__`) |
| 每次取值  | 立即返回下一个元素                        | `await` 下一个元素（可能要等待异步IO）           |
| 场景    | 遍历普通列表、字典等                       | 遍历异步生成器、异步流、异步IO结果                 |


```csharp
异步数据流 async for
│
├── async def generator():
│       await IO操作
│       yield 数据项
│
└── async for item in generator():
        await 获取下一个 item
```

## 基本概念回顾

- 可迭代对象（Iterable）：实现 ``__iter__()``，能返回一个迭代器（或实现 ``__getitem__`` 的旧式序列）。可以用 for x in obj: 遍历。

- 迭代器（Iterator）：实现 ``__iter__()``（返回 self）和 ``__next__()（Python 3 中名为 __next__）``。``next(it) 会调用 it.__next__()``，当结束时抛 StopIteration。

- 生成器（Generator）：**用 yield 的函数会返回生成器对象**。生成器是迭代器的一种特殊实现，维护自己的执行状态（局部变量、指令指针等）。

yield：暂停函数并“产出”一个值，同时保持函数状态以便下次继续执行。和 return 不同，yield 会把函数变成生成器并可多次执行（每次返回一个值）。

yield 不能在普通函数中使用：定义了 yield 的函数变成生成器。

**不要把 yield 与 return 混用：return 结束生成器，yield 是产出点。**

- yield 表达式的两种角色：

1) ``yield <expr>：把 <expr> ``交给调用者，

2) 同时 yield 本身是一个表达式，其值由下一次 ``send(value)`` 提供。

```python
def gen():
    x = yield "first"
    print("x:", x)
    y = yield "second"
    print("y:", y)

g = gen()
print(next(g))      # prints "first"
print(g.send(10))   # prints "x: 10", prints "second"

```

``x = yield y``：调用者得到 y，生成器暂停；

当外部 g.send(v) 恢复时，x 得到 v。

## 生成器 vs 手写迭代器类（对比）
```python
def squares(n):
    for i in range(n):
        yield i*i
```
```python
class Squares:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        val = self.i*self.i
        self.i += 1
        return val
```
yield 把函数变为生成器，生成器是迭代器的一种简洁实现。


生成器对象有 .send(), .throw(), .close() 可以进行高级控制（协程式通信、异常注入、优雅关闭）。

## 常见场景 / 使用理由（为什么用生成器）

- 节省内存：生成器按需生成元素，适合处理大数据流或无限序列。

- 流处理 / 管道：把多个生成器串联成处理流水线（类似 Unix pipe）。

- 懒计算：避免一次性计算所有元素。

- 异步流（结合 async for / async generators）：处理网络/IO 流。

- 协程通信（用 send() 实现简单协程交互，已部分被 async/await 取代）。

- 实现自定义迭代器：比写类更简单直接。

对于异步代码，使用 async def / await / async for 是现代推荐方式；但生成器仍然在很多同步流处理场景中很有用。

异步生成器（async def + yield）：
```python
async def async_gen():
    await asyncio.sleep(1)
    yield 1

async def main():
    async for x in async_gen():
        print(x)
```

# 七、Problems

## 确认你没有混用 sync 和 async 逻辑

如果在 async 视图中用了阻塞的数据库查询（比如 MyModel.objects.all()），会触发警告或阻塞。


### 🧩 一、Django ORM 是同步的

Django 自带的 ORM（`Model.objects.all()、filter()` 等）是同步阻塞的。
这意味着即使你在 `async def` 视图中调用它，Django ORM 仍会阻塞事件循环：

```python
async def apps(request):
    rows = Agent.objects.all()  # ❌ 同步操作，会卡住事件循环
```

所以，异步环境下应使用：

```python
from asgiref.sync import sync_to_async

@sync_to_async
def get_data():
    return list(MyModel.objects.all())

async def apps(request):
    data = await get_data()
    return JsonResponse({"data": data})
```

sync_to_async 会把同步函数（这里是 ORM 查询）放入线程池（ThreadPoolExecutor）中执行，从而不会阻塞主事件循环（event loop）。

#### ⚙️ 线程池来自哪里？

sync_to_async 使用的是 asgiref 库（Django 自带依赖之一）。

在 asgiref.sync 模块中，有一个默认的线程池：

```python
import concurrent.futures

# 源码（简化）
loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor()
loop.set_default_executor(executor)
```

- Django（通过 asgiref）默认会使用一个 全局的 ThreadPoolExecutor，
- 所有 sync_to_async() 调用都共用它。

对于 Django 项目，可以在 asgi.py 中设置 max_workers；

```python
# asgi.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from django.core.asgi import get_asgi_application

# 限制线程池大小 max_workers ，防止过多 ORM 查询阻塞
executor = ThreadPoolExecutor(max_workers=16)
loop = asyncio.get_event_loop()
loop.set_default_executor(executor)

application = get_asgi_application()
```
通常建议设置在：CPU 核心数 × 4 ~ 8 之间。

### ⚡ 二、如果你使用 aiomysql，就不再使用 Django ORM

aiomysql 是一个纯异步 MySQL 驱动，基于 asyncio，它不会用 Django 的 ORM。
你必须用 SQL 语句 自己查询：

```python
import aiomysql
from django.http import JsonResponse

async def apps(request):
    conn = await aiomysql.connect(
        host='localhost', port=3306,
        user='root', password='123456',
        db='demo_db'
    )
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute("SELECT * FROM agents;")
        rows = await cur.fetchall()
    conn.close()
    return JsonResponse(rows, safe=False)
```

🟢 在这个例子中：

- 数据库连接和查询都是异步的；

- await cur.execute() 和 await cur.fetchall() 都不会阻塞事件循环；

- 不需要再用 @sync_to_async 包裹。