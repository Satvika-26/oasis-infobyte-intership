import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)

print("Server is waiting for connection...")
conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    # Receive message
    msg = conn.recv(1024).decode()
    if not msg or msg.lower() == 'exit':
        print("Client disconnected.")
        break
    print(f"Client: {msg}")

    # Send reply
    reply = input("You: ")
    conn.send(reply.encode())
    if reply.lower() == 'exit':
        print("Chat ended by server.")
        break

conn.close()
server.close()
