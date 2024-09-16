import asyncio

import aiohttp


async def main():
    session = aiohttp.ClientSession()
    #
    # response = await session.post(
    #     "http://127.0.0.1:8080/user/",
    #     json={'name': 'user_6', 'password': '1234'},
    #
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.post(
    #     "http://127.0.0.1:8080/adv/",
    #     json={'heading': 'Aticle7d',
    #           'description': 'descriptions',
    #           'user_id': 1
    #           }
    #
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.get(
    #     "http://127.0.0.1:8080/adv/1/",
    #
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.patch(
    #     "http://127.0.0.1:8080/adv/1/",
    #     json={
    #         'heading': 'Aticle5'
    #     }
    #
    # )
    # print(response.status)
    # print(await response.json())
    #
    # response = await session.get(
    #     "http://127.0.0.1:8080/user/4/",
    #
    # )
    # print(response.status)
    # print(await response.json())

    response = await session.delete(
        "http://127.0.0.1:8080/adv/1/",
    )
    print(response.status)
    print(await response.json())

    response = await session.get(
        "http://127.0.0.1:8080/adv/1/",
    )
    print(response.status)
    print(await response.json())
    #
    # await session.close()


asyncio.run(main())
