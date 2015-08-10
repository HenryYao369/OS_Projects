#coding=utf-8
__author__ = 'Hengzhi'

import socket,sys

#设置默认的ip地址和端口号，在没有使用命令传入参数的时候将使用默认的值
host="localhost"
port=44100

def usage():
    print """
    -h --help             print the help
    """

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.send(message)

    while True:
        feedback = sock.recv(2048)

        if feedback == 'RETRY':
            msg_retry = raw_input("Please retry:")
            sock.send(msg_retry)
        else:
            print feedback
            break

        # if sys.argv[2] == 'GET':
        #     print 'GET: '+ sock.recv(2048)
        # elif sys.argv[2] == 'SET':
        #     print 'Set to: '+ sock.recv(2048)

    sock.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit(usage())

    ip_addr = sys.argv[1]
    command = sys.argv[2]

    if command == "GET":
        message = "GET"
    elif command == "SET":
        message = "SET " + sys.argv[3]
    else:
        message = sys.argv[2]
        # sys.exit(usage())

    main()








