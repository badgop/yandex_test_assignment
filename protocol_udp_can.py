import can
import message_class
import struct

def bool_to_bytestr(in_bool):

	if in_bool:
		out=struct.pack('B',1)
	else:
		out=struct.pack('B',0)	
	return out

def bytestr_to_bool(in_bytestr):

	if in_bytestr==struct.unpack('B',1):
		out=True
	else:
		out=False
	return out

def can_to_udp_mes(can_mess,dst_ip,dst_port):	

	is_ext_byte=bool_to_bytestr(can_mess.is_extended_id)	
	dlc_bit = struct.pack('B',can_mess.dlc)
	is_error_frame_byte= bool_to_bytestr(can_mess.is_error_frame)
	is_remote_frame_byte = bool_to_bytestr(can_mess.is_remote_frame)
	byte_str = struct.pack('L',can_mess.arbitration_id)+is_ext_byte+is_error_frame_byte+is_remote_frame_byte+dlc_bit+can_mess.data		
	udp_mess= message_class.message_data(payload=byte_str,size=len(can_mess.data),ip=dst_ip,port=dst_port)
	return udp_mess

def udp_to_can_mes(udp_mes):
	can_mes=can.Message()	
	print(udp_mes)
	
	can_mes.arbitration_id, = struct.unpack_from('L',udp_mes,0)	
	can_mes.is_extended_id, = struct.unpack_from('B',udp_mes,8)
	can_mes.is_error_frame, = struct.unpack_from('B',udp_mes,9)
	can_mes.is_remote_frame,= struct.unpack_from('B',udp_mes,10)	
	dlc_bit ,= struct.unpack_from('B',udp_mes,11)
	#если длина пакета НЕ нулевая - достаем данные
	if (dlc_bit>0):
		can_mes.dlc = dlc_bit
		can_mes.data = udp_mes[13:]
		print('data ',can_mes.data)
	
	
	return can_mes