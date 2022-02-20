import asyncio
from handle_connection import handle_connection


async def main():
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())