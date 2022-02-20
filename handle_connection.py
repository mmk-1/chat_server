import asyncio
from connection_pool import ConnectionPool


connection_pool = ConnectionPool()
async def handle_connection(reader, writer):
    # Get nickname
    writer.write("> Choose your nickname: ".encode())

    response = await reader.readuntil(b"\n")
    writer.nickname = response.decode().strip()

    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    # New user announcement
    connection_pool.broadcast_user_join(writer)

    while True:
        try:
            data = await reader.readuntil(b"\n")
        except asyncio.exceptions.IncompleteReadError:
            connection_pool.broadcast_user_quit(writer)
            break

        message = data.decode().strip()
        if message == "/quit":
            connection_pool.broadcast_user_quit(writer)
            break
        elif message == "/list":
            connection_pool.list_users(writer)
        else:
            connection_pool.broadcast_new_message(writer, message)

        await writer.drain()

        if writer.is_closing():
            break
    # Cleaning up after user leaves
    writer.close()
    await writer.wait_closed()
    connection_pool.remove_user_from_pool(writer)