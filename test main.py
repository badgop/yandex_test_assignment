# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:29:56 2021

@author: Mouse
"""

import udp_class
import message_class 
import struct
import errors



def test_point_to_point(ip, port, size, payload):
    
    """
    
    функция для теста работы в режиме клиент посылает на сервер сообщение
    
    size : int - размер принимаемого сообщения
    payload : int - полезная нагрузка передаваемого сообщения, в виде числа 
    (исключательно в целях примера)
    
    """
    #  создаеем нагрузку
    payload = struct.pack('i', payload)      
    # формируем передаваемое сообщение
    mes = message_class.message_data(payload,size,ip,port) 
    # создаем совет для работы сервера, в  НЕБЛОКИРУЮЩЕМ режиме,
    # с временем ожидания 0.5 c
    first_sock  = udp_class.udp_socket(ip, port, True, False,0.5) 
    # создаем второй сокет для клиента 
    second_sock = udp_class.udp_socket() 
    
    # посылаем сообщение
    second_sock.send_message(mes)
    
    # пробуем принять 
    try:
        ans = first_sock.rec_message(1024)
    except errors.Nothing_Recieved_due_timeoout as e:
        print (e)
    else:          
        print (payload)
        print (ans.payload)
        # если передаваемое сообщение соответствует переданному все отлично
        if (payload == ans.payload):
            print ('Данные приняты верно\n')
            
    # обязательно закрываем сокеты, иначе при повторном вызове будет ошибка 
    first_sock.close()
    second_sock.close()     
    
def test_point_to_point_timeout_error(ip, port, size, payload):
    
    """
    
    функция для теста обработки исключения, если сервер ничего не получил за время
    timeout
    
    size : int - размер принимаемого сообщения
    payload : int - полезная нагрузка передаваемого сообщения, в виде числа 
    (исключательно в целях примера)
    
    """
    #  создаеем нагрузку
    payload = struct.pack('i', payload)      
    # формируем передаваемое сообщение
    mes = message_class.message_data(payload,size,ip,port) 
    # создаем совет для работы сервера, в  НЕБЛОКИРУЮЩЕМ режиме,
    # с временем ожидания 0.5 c
    first_sock  = udp_class.udp_socket(ip, port, True, False,0.5) 
    # создаем второй сокет для клиента 
    second_sock = udp_class.udp_socket() 
    
    # НЕ посылаем сообщение
    # second_sock.send_message(mes)
    pass
    
    # пробуем принять 
    try:
        ans = first_sock.rec_message(1024)
    except errors.Nothing_Recieved_due_timeoout as e:
        print (e)
        print('Время ожидания истекло\n')
    else:          
        print (payload)
        print (ans.payload)
        # если передаваемое сообщение соответствует переданному все отлично
        if (payload == ans.payload):
            print ('Данные приняты верно\n')
            
    # обязательно закрываем сокеты, иначе при повторном вызове будет ошибка 
    first_sock.close()
    second_sock.close()    
        
    
def test_point_to_point_socket_is_used(ip, port, size, payload):
    
     """
    
     функция для теста работы обработки ошибки, которая происходит если сокет
     уже открыт
    
     size : int - размер принимаемого сообщения
     payload : int - полезная нагрузка передаваемого сообщения, в виде числа 
     (исключательно в целях примера)
    
     """    
     # создаем совет для работы сервера, в  НЕБЛОКИРУЮЩЕМ режиме,
     # с временем ожидания 0.5 c
     first_sock  = udp_class.udp_socket(ip, port, True, False,0.5) 
     #  повторно создаем такой же сокет и ожидаем прекращения программы
     first_sock  = udp_class.udp_socket(ip, port, True, False,0.5) 
    


if __name__ == '__main__':
    
    
    
    ip = 'localhost'
    port = 8008
    size = 1024
    payload = 65536
    
    print ('test   test_point_to_point(ip, port, size, payload)\n')
    test_point_to_point(ip, port, size, payload)
    print ('-----------------------------------------------------\n')
    print ('test_point_to_point_timeout_error(ip, port, size, payload)\n')
    test_point_to_point_timeout_error(ip, port, size, payload)
    print ('-----------------------------------------------------\n') 
    
    
    print ('test   test_point_to_point_socket_is_used(ip, port, size, payload)\n')
    test_point_to_point_socket_is_used(ip, port, size, payload) 
    print ('-----------------------------------------------------\n')
    
