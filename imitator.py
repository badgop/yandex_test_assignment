import udp_class
import message_class
import errors
import sys
import socket
import string
import time
import can
from protocol_udp_can import *

def check_ip_value(ip_str):
	try:
		ip_addr = socket.inet_aton(ip_str)
	except OSError as error:
		print(error)
		sys.exit(0)	

def check_port_value(port_value):
	if port_value.isnumeric():
		port_value =int(port_value)
		# проверка того, что порт находится в заданом диапазоне
		# о диапазонах см. RFC
		if (not(port_value>4096)&(port_value<65536)):
			print('port value is wrong')
	else:
		print ('port value is not numeric')
		sys.exit(0)


def check_args():
	"""
	Валидация аргументов командной строки
	аргументы командной строки
 	
 	ip_host  - ip хоста 
 	port_host -  порт хоста
 	ip_dev  - ip устройства Real CAN dev 	
 	port_dev -  порт устройства Real CAN dev 	
 	interface - идентификатор интерфейса vcan в системе	
	"""
	
	if(len(sys.argv)<6):
		print('не хватает аргументов!')
		sys.exit()

	ip_host_str = sys.argv[1]	
	if ip_host_str!='localhost':
		check_ip_value(ip_host_str)

	ip_dev_str = sys.argv[3]	
	if ip_dev_str!='localhost':
		check_ip_value(ip_dev_str)

	port_host = (sys.argv[2])
	check_port_value(port_host)
	port_host=int(port_host)

	port_dev = (sys.argv[4])
	check_port_value(port_dev)
	port_dev=int(port_dev)
	
	vcan_int_name = sys.argv[5]

	return(ip_host_str,port_host,ip_dev_str,port_dev,vcan_int_name)



def main_fun(init_parameters,sock, can_timeout=0.01):
	while True:
		#print('ok\n')
        
        # приняли сообщение от хоста
		try:
			message_from_host=sock.rec_message(2048)
		except errors.Nothing_Recieved_due_timeoout as e:
			pass
		else:
			#если приняли сообщение, то шлем его обратно
			if message_from_host!=None:		
				print(message_from_host.payload)			

						
				sock.send_message(message_from_host)
	

if __name__ == '__main__':
	
	init_params = check_args()
	#0 ip_host  - ip хоста 
 	#1 port_host -  порт хоста
 	#2 ip_dev  - ip устройства Real CAN dev 	
 	#3 port_dev -  порт устройства Real CAN dev 	
 	#4 vcan name
	print (init_params)

	# создаем сокет для приема данных  НЕБЛОКИРУЮЩЕМ режиме,
    # с временем ожидания 0.01 c
	host_sock=udp_class.udp_socket(host=init_params[2],port=init_params[3],is_server=True,is_blocking=False,time_out=0.1) 
	
	
	try:
		main_fun(init_params,host_sock)
	except KeyboardInterrupt:
		print('exitting\n')
		host_sock.close()
		sys.exit(0)



	

	

	




	