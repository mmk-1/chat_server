from textwrap import dedent


class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()

    def send_welcome_message(self, writer):
        message = dedent(f"""
        ===        
        Welcome {writer.nickname}!

        There are {len(self.connection_pool) - 1} user(s) here beside you

        Help:
         - Type anything to chat
         - /list will list all the connected users
         - /quit will disconnect you
        ===
        """)

        writer.write(f"{message}\n".encode())

    def broadcast(self, writer, message):
        for user in self.connection_pool:
            if user != writer:
                # Don't broadcast msg to the user/writer
                user.write(f"{message}\n".encode())

    def broadcast_user_join(self, writer):
        self.broadcast(writer, f"{writer.nickname} just joined")

    def broadcast_user_quit(self, writer):
        self.broadcast(writer, f"{writer.nickname} just quit")

    def broadcast_new_message(self, writer, message):
        self.broadcast(writer, f"[{writer.nickname}] {message}")

    def list_users(self, writer):
        message = "===\n"
        message += "Currently connected users:"
        for user in self.connection_pool:
            if user == writer:
                message += f"\n - {user.nickname} (you)"
            else:
                message += f"\n - {user.nickname}"

        message += "\n==="
        writer.write(f"{message}\n".encode())

    def add_new_user_to_pool(self, writer):
        self.connection_pool.add(writer)

    def remove_user_from_pool(self, writer):
        self.connection_pool.remove(writer)