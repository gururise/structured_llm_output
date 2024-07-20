import asyncio

class AsyncSocketServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = set()

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")
        self.clients.add(writer)

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                message = data.decode()
                print(f"Received {message!r} from {addr}")

                # Echo the data back to the client
                writer.write(data)
                await writer.drain()

        except asyncio.CancelledError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            self.clients.remove(writer)
            print(f"Connection closed for {addr}")

    async def send_data_to_clients(self, data):
        if not self.clients:
            print("No clients connected")
            return

        for writer in self.clients:
            try:
                writer.write(data.encode())
                await writer.drain()
                print(f"Sent to {writer.get_extra_info('peername')}: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")

async def main():
    server = AsyncSocketServer()
    server_task = asyncio.create_task(server.start_server())

    while True:
        message = await asyncio.to_thread(input, "Enter message to send (or 'quit' to exit): ")
        if message.lower() == 'quit':
            break
        await server.send_data_to_clients(message)

    server_task.cancel()
    await server_task

if __name__ == "__main__":
    asyncio.run(main())
