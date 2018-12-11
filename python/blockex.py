from urllib.request import urlopen
import asyncio


def run_in_executor(f):
    def inner(*args):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args))

    return inner


@run_in_executor
def foo(arg):
    r = urlopen("https://example.com")
    resp = r.read().decode()
    return f"{arg}{len(resp)}"


@run_in_executor
def bar(arg):
    r = urlopen("https://example.com")
    resp = r.read().decode()
    return f"{len(resp)}{arg}"


async def process_input(inp):
    res = await foo(inp)
    return await bar(res)


async def main():
    inputs = ["one", "two", "three"]
    input_tasks = [asyncio.create_task(process_input(inp)) for inp in inputs]
    print([await t for t in asyncio.as_completed(input_tasks)])
    # print([await t for t in asyncio.as_completed([process_input(inp) for inp in input_tasks])])


if __name__ == '__main__':
    asyncio.run(main())
