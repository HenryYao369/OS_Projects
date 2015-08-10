from socket import *
from threading import Thread, Semaphore 
import sys

MOTD = "Initial msg"

class Server:
	def __init__(self):
		self.port = 44100
		self.ssocket = None
		self.threads = []
	"""
	def setserver(self):
		try:
			self.ssocket = socket(AF_INET, SOCK_STREAM)  #create server socket
			self.ssocket.bind((self.host,self.port))                      #bind socket to address
			self.ssocket.listen(5)                       #listen for connections
		except:
			if self.ssocket:
				self.ssocket.close()
			print "Error on open socket"
			sys.exit(1)
	"""
	def run(self):
		self.ssocket = socket(AF_INET, SOCK_STREAM)  #create server socket
		self.ssocket.bind(('localhost',self.port))                      #bind socket to address
		self.ssocket.listen(5)                     
		while True:
			c = Client(self.ssocket.accept())
			c.start()
			self.threads.append(c)

		self.ssocket.close()
		for c in self.threads:
			c.join()



class Client(Thread):
	def __init__(self,(csocket,caddr)):
		Thread.__init__(self)
		self.csocket = csocket
		self.caddr = caddr
		self.count = 3
	def run(self):
		global MOTD
		while True:
			data = self.csocket.recv(1024)
			if data == "GET":
				self.sem.acquire()
				self.csocket.send(MOTD)
				self.sem.release()
				break
			elif data.startswith("SET"):
				self.sem.acquire()
				MOTD = data[4:]
				self.csocket.send("OK")
				self.sem.release()
				break
			else:
				if self.count>0:
					self.count = self.count - 1
					self.csocket.send("RETRY")
				else:
					self.count = 3
					self.csocket.send("ERROR")
					break
		self.csocket.close()



if __name__ == "__main__": 
	s = Server()
	s.run()


