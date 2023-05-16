import socket

HOST = "10.0.95.222"  # The IP address of the scanner
PORT = 9005  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        if data:
            print(f"Received {data!r}")