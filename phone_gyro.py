import socket, traceback
import math



def getAcc():
    host = '192.168.1.103'
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))


    # sensor_data = str(message).split(',')[2:5]
    while True:
        message, address = s.recvfrom(8192)
        message = str(message).replace("'", "").replace("b", "")
        sensor_data = str(message).split(',')
        # print('Raw : ', message)
        if len(sensor_data)>10:
            break
    return  sensor_data


#while True :
#    print (">")
#    print('Readings : ',getAcc())