import socket
import time


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(('localhost', 8001))


    time.sleep(0.1)

    s.send('11')

    print s.recv(1024)

    s.close()