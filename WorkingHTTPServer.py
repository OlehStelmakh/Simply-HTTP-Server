import socket

HOST = '0.0.0.0'
PORT = 8080

def get_data(conn):
    data = conn.recv(2048)
    file_name = str.split(data.decode('utf-8'))[1][1:]
    print(data.decode('utf-8'))
    
    if file_name == "":
        file_name = "main.html"
    mime = get_mimeType(str.split(file_name, ".")[1])

    responce = "HTTP/1.1"
    responce+= "200 OK\r\n"
    responce+= "Server: SimpleHttp\r\n"
    responce+= "Content-Type: "+mime+"\r\n"
    responce+= "Connection: close\r\n\r\n";

    file = open(file_name, "rb")
    data = file.read()
    conn.send(bytes(responce, 'utf-8'))
    conn.send(data)

def error_404(conn):
    file_name = "404.html"
    file = open(file_name, "rb")
    answer = file.read()
    mime = get_mimeType("");

    responce = "HTTP/1.1"
    responce+= "404 Not Found OK\r\n"
    responce+= "Server: SimpleHttp\r\n"
    responce+= "Content-Type:"+mime+"\r\n"
    responce+= "Connection: close\r\n\r\n"
    
    conn.send(bytes(responce, 'utf-8'))
    conn.send(answer)

def get_mimeType(mime):
    if mime == "html":
        return "text/html; charset=utf-8"
    elif mime == "jpeg":
        return "image/jpeg"
    elif mime == "png":
        return "image/png"
    else:
        return "text/html; charset=utf-8"


sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM, socket.IPPROTO_TCP)
sock.bind((HOST, PORT))
sock.listen(10)

try:
    while True:
        print("Server started...\nWaiting for connections...")
        conn, addr = sock.accept()
        try:
            print("Client connected..\n")
            get_data(conn)
        except KeyboardInterrupt:
            print('Socket connection is closed.')
        except:
            error_404(conn)
        finally:
            conn.close()
finally: 
    sock.close()

