import asyncio


async def request_traffic_jams():
    # await asyncio.sleep(0.1) # This will pass
    await asyncio.sleep(10)


async def main():
    try:
        await asyncio.wait_for(request_traffic_jams(), timeout=1.0)
    except asyncio.TimeoutError:
        print('Problems with traffic_jams service')


if __name__ == '__main__':
    asyncio.run(main())
