import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

print("Connected to server. Type 'exit' to end chat.")

while True:
    # Send message
    msg = input("You: ")
    client.send(msg.encode())
    if msg.lower() == 'exit':
        print("You ended the chat.")
        break

    # Receive reply
    reply = client.recv(1024).decode()
    if not reply or reply.lower() == 'exit':
        print("Server ended the chat.")
        break
    print(f"Server: {reply}")

client.close()
