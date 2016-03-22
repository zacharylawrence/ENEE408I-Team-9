import socket
import threading
import time

def web_interface_thread(event_kill):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 10000)
	sock.bind(server_address)
	sock.listen(0)
	while not event_kill.isSet():
		print('Waiting for a connection...')
		conn, client_address = sock.accept()
		amount_received = 0
		data = ''
		while True:
			num_to_add = 16
			newdata = conn.recv(num_to_add).decode()
			if (len(newdata) > 0):
				amount_received += len(newdata)
				data += newdata
			else:
				break
		print(data)
		conn.close()
	return

wt_kill = threading.Event()

wt = threading.Thread(target=web_interface_thread, args=(wt_kill,))
wt.setDaemon(True)
wt.start()

time.sleep(60)
wt_kill.set()
print('Program Closed!')