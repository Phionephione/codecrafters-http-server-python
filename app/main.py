import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    request = conn.recv(4096)
    request = request.decode().split("\r\n")
    http_method, path, http_version = request[0].split(" ")

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    conn.send(response)


if __name__ == "__main__":
    main()
