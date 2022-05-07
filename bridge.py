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


# def can_to_udp_mes(can_mess,dst_ip,dst_port):
# 	udp_mess=message_class.message_data(payload=can_mess.data,size=len(can_mess.data),ip=dst_ip,port=dst_port)
# 	return udp_mess

# def udp_to_can_mes(udp_mess):
# 	can_mess=can.Message(data=udp_mess.payload)
# 	return can_mess


def main_fun(init_parameters,sock,bus_can, can_timeout=0.01):
	while True:
		#print('ok\n')
        
        # приняли сообщение от vcan
		try:
			message = bus_can.recv(can_timeout)			
		except OSError:
			print('bus reciev error\n')
			host_sock.close()
			sys.exit(0)		
		else:
			#если приняли сообщение, то шлем его Real CAN dev
			if message!=None:		
				print('rec from vcan0 \n')
				print(message)

				mes_send=can_to_udp_mes(message,init_parameters[2],init_parameters[3])			
				sock.send_message(mes_send)

		# принимаем датаграму от Real CAN device
		try:
			message_from_real_can_dev=sock.rec_message(2048)
		except errors.Nothing_Recieved_due_timeoout as e:
			pass
		else:
			print('meg drom can dev')
			mes = udp_to_can_mes(message_from_real_can_dev.payload)		
			print('rec from udp \n')
			print(message)
			
			bus_can.send(mes)	


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
	host_sock=udp_class.udp_socket(host=init_params[0],port=init_params[1],is_server=True,is_blocking=False,time_out=0.1) 
	
	#инициализируем доступ к шине 
	try:
		bus = can.Bus(channel=init_params[4], interface='socketcan')
	except OSError:
		print('bus init error\n')
		host_sock.close()
		sys.exit(0)


	try:
		main_fun(init_params,host_sock,bus)
	except KeyboardInterrupt:
		print('exitting\n')
		host_sock.close()
		sys.exit(0)



	

	

	




	