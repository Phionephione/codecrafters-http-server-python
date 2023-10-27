import socket
import threading


HTTP_STATUS_OK = "HTTP/1.1 200 OK\r\n"
HTTP_STATUS_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"


def handle_client(conn, addr):
    request = conn.recv(4096)
    request = request.decode().splitlines()

    _, path, _ = request[0].split(" ")

    if path == "/":
        response = HTTP_STATUS_OK + "\r\n"
    elif path.startswith('/echo'):
        content = path.split("/echo/")[1]
        response = (HTTP_STATUS_OK +
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "\r\n"
                    f"{content}\r\n")
    elif path.startswith('/user-agent'):
        content = request[2].split(": ")[1]
        response = (HTTP_STATUS_OK +
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "\r\n"
                    f"{content}\r\n")
    else:
        response = HTTP_STATUS_NOT_FOUND + "\r\n"

    conn.send(response.encode())
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client

        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()



if __name__ == "__main__":
    main()
