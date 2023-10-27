import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    request = conn.recv(4096)
    request = request.decode().splitlines()
    _, path, _ = request[0].split(" ")

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith('/echo'):
        content = path.split("/echo/")[1]
        response = ("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "\r\n"
                    f"{content}\r\n")
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())



if __name__ == "__main__":
    main()
