import sys
import socket
import threading


HOST = "localhost"
PORT = 4221
FILES_DIR = ""

HTTP_STATUS_OK = "HTTP/1.1 200 OK\r\n"
HTTP_STATUS_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"


def get_response(request, files=None):
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
    elif path.startswith('/files'):
        file_name = path.split("/files/")[1]
        file_content = handle_files(file_name)

        if file_content:
            response = (HTTP_STATUS_OK +
                        "Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {len(file_content)}\r\n"
                        "\r\n"
                        f"{file_content}\r\n")
        else:
            response = HTTP_STATUS_NOT_FOUND + "\r\n"

    else:
        response = HTTP_STATUS_NOT_FOUND + "\r\n"

    return response


def handle_files(file_name):
    try:
        with open(f"{FILES_DIR}{file_name}", "r") as f:
            file = f.read()
    except FileNotFoundError:
        file = None
    return file


def handle_client(conn, addr):
    request = conn.recv(4096)
    request = request.decode().splitlines()
    response = get_response(request)

    conn.send(response.encode())
    conn.close()


def main(args):
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    if args:
        global FILES_DIR
        FILES_DIR = args[1]

    while True:
        conn, addr = server_socket.accept() # wait for client

        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()



if __name__ == "__main__":
    main(sys.argv[1:])

