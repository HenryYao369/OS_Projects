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
#创建socket对象。调用socket构造函数
#AF_INET为ip地址族，SOCK_STREAM为流套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#设置要连接的服务器的ip号和端口号
    sock.connect((host, port))
#客户端输入一个字符串给服务器
    msg_str = str(message)
    sock.send(msg_str)
    if message[0] == 0:
        print 'GET: '+ sock.recv(2048)
    elif message[0] == 1:
        print 'Set to: '+ sock.recv(2048)
#关闭与服务器的连接
    sock.close()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit(usage())

    ip_addr = sys.argv[1]
    command = sys.argv[2]

    if command == "GET":
        message = [0,'']
    elif command == "SET":
        new_message = sys.argv[3]
        message = [1,new_message]
    else:
        sys.exit(usage())

    main()


