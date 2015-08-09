#coding=utf-8
__author__ = 'Hengzhi'


import socket
import threading,sys

MOTD = "message of the day"  # protected by sema
sema = threading.Semaphore()

num_connections=10
port=44100

def usage():
    print """
    -h --help             print the help
    """

def thread_work(client, address):
    global MOTD
    try:
    #设置超时时间
        client.settimeout(100)
    #接收数据的大小
        buf = client.recv(2048)
        print 'buf:', buf

    #将接收到的信息原样的返回到客户端中
        # msg = []
        # import csv
        # parser = csv.reader(buf)
        # for fields in parser:
        #     for i,f in enumerate(fields):
        #         msg.append(f)
        #         print f

        import ast
        msg = ast.literal_eval(buf)
        print 'msg:', msg
        # print msg
        if msg[0] == 0:
            print msg[0]
            client.send(MOTD)
        elif msg[0] == 1:
            MOTD = msg[1]
            print 'MOTD has been set to: ',MOTD
            client.send(MOTD)
        else:
            print "error not parsed!"

    #超时后显示退出
    except socket.timeout:
        print 'time out'
    #关闭与客户端的连接
    client.close()

def main():
    #创建socket对象。调用socket构造函数
    #AF_INET为ip地址族，SOCK_STREAM为流套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #将socket绑定到指定地址，第一个参数为ip地址，第二个参数为端口号
    sock.bind(('localhost', port))
    #设置最多连接数量
    sock.listen(num_connections)
    while True:
    #服务器套接字通过socket的accept方法等待客户请求一个连接
        client,address = sock.accept()

        sema.acquire()
        thread = threading.Thread(target=thread_work, args=(client, address))
        thread.start()
        thread.join()

        sema.release()


if __name__ == '__main__':


    main()





