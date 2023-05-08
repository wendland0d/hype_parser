from Parsers import Buff

import asyncio

async def start():
    buff = Buff(
        login="Zaciendishay",
        password="es1lKqjOQT6VYJ3c{BX",
        secret="ITUYDWEA3EWV45VT6XT37GLXIUK3EKQS",
        proxies=['', ''],
    )
    buff.steam_login()
    buff.log_in()

    data = buff.parse()
    print(data)

if __name__ == '__main__':
    asyncio.run(start())
