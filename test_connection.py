import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)
mess = '0123456789101112131415161718192021222324252627282930'.encode()
sock.sendall(mess)
sock.close()