import socket


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8001))

    sock.listen(5)

    # while True:
    client_connection,address = sock.accept()

    try:
        client_connection.settimeout(5)

        buf = client_connection.recv(1024)
        if buf == '1':
            client_connection.send('welcome to server!')
        else:
            client_connection.send('please go out!')

    except socket.timeout:
        print 'time out'

    client_connection.close()