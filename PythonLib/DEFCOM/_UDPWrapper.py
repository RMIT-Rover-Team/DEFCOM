#!/usr/bin/env python3
#All you have to worry about is the Data,Port and IP
#Buffer has a default value
#One Way, Open Two Sockets for two way
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, SO_SNDBUF, SOL_SOCKET


__author__ = 'Kaelan Grainger'
__version__ = '2.0'


def version():
    print('Version: ' + __version__ + ' By: ' + __author__)
    print('Library Name: ' + str(__name__))
    return [__author__,__version__,__name__]


class udpsend:
    def __init__(self,IP=None, PORT = None, BUFF_SIZE=1024):
        self.SOCK = socket(AF_INET, SOCK_DGRAM)
        self.SOCK.setsockopt(SOL_SOCKET, SO_SNDBUF, BUFF_SIZE)
        self.buffs = BUFF_SIZE
        self.addr = (IP,PORT)

    def senddat(self,DATA,IP=None,PORT=None):
        if self.addr == (None,None):
            pass
        else:
            IP, PORT = self.addr

        self.SOCK.sendto(DATA,(IP,PORT))

    def close(self):
        self.SOCK.close()

class udpget:
    def __init__(self,IP,PORT,BUFF_SIZE=1024):
        self.addr = (IP,PORT)
        self.buffs = BUFF_SIZE
        self.SOCK = socket(AF_INET,SOCK_DGRAM)
        self.SOCK.bind(self.addr)

    def getdat(self):
        return self.SOCK.recvfrom(self.buffs)[0]

    def getaddrdat(self):
        return self.SOCK.recvfrom(self.buffs)

    def close(self):
        self.SOCK.close()


#IP
def get_ip_address():
    return gethostbyname( '0.0.0.0' )
