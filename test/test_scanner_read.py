import asyncio
import socket

IP = '10.0.95.222' # Scanner IP
# IP = '10.0.95.120'  # Server IP
# IP = '127.0.0.1'  # Servers localhost IP

# PORT = 9009
# PORT = 9005
PORT = 9006

loop = asyncio.get_event_loop()

async def Scanner():
    while True:
        try:
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client = socket.socket()
            client.settimeout(1)
            await loop.sock_connect(client, (IP, PORT))
            
            client.settimeout(900)
            response = await loop.sock_recv(client, 1024)
            fixedCode = response.decode("utf-8").split(':')
            print("Scanner: ", fixedCode[1].strip())
            client.close()
            await asyncio.sleep(1)
        except Exception as e:
            print("Exception: ", e)
            await asyncio.sleep(10)
            print("Scanner: Reconnecting")
        #await Scanner()
           

loop.create_task(Scanner())
loop.run_forever()

