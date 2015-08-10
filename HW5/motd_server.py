#coding=utf-8
__author__ = 'Hengzhi'


import socket
import sys
from threading import Thread, Semaphore

MOTD = "message of the day"  # protected by sema
sema = Semaphore()

num_connections=10
port=44100

def usage():
    print """
    -h --help             print the help
    """

class ThreadedWorker(Thread):
    def __init__(self,client,address):
        Thread.__init__(self)
        self.count = 0
        self.client = client
        self.address = address

    def run(self):
        global MOTD

        while True:
            buf = self.client.recv(2048)  #接收数据的大小
            print 'buf:', buf

            msg_list = buf.split()
            print msg_list

            if msg_list[0] == 'GET':
                self.client.send(MOTD)
                break
            elif msg_list[0] == 'SET':
                MOTD = msg_list[1]
                print 'MOTD has been set to: ', MOTD
                self.client.send('OK')
                break
            else:
                print "error not parsed!"
                self.count += 1

                if self.count == 3:
                    self.client.send('ERROR')
                    break

                self.client.send('RETRY')

        self.client.close()

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))

    sock.listen(num_connections)  #设置最多连接数量

    while True:
    #服务器套接字通过socket的accept方法等待客户请求一个连接
        client,address = sock.accept()

        sema.acquire()

        # t = threading.Thread(target=thread_work, args=(client, address))
        t = ThreadedWorker(client, address)
        t.start()
        t.join()

        sema.release()


if __name__ == '__main__':


    main()





