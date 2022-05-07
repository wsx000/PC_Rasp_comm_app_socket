# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/8 12:17
# @Author: wsx
# @File  : main.py
import socket
import serial
from scmSerial import ScmToRaspThread, RaspToScmThread
from clientSocket import PCToRaspThread, RaspToPCThread


class Main(object):
    def __init__(self):
        # socket与服务器连接
        self.socket = self.connect_server()
        # 初始化串口
        # self.ser = self.serial_init()
        # Rasp->PC线程
        self.DataRaspToPC = RaspToPCThread(self.socket)
        self.DataRaspToPC.start()
        # PC->Rasp线程
        self.DataPCToRasp = PCToRaspThread(self.socket)
        self.DataPCToRasp.start()
        # SCM->Rasp线程
        # self.DataRaspToScm = RaspToScmThread(self.ser)
        # self.DataRaspToScm.start()
        # Rasp->SCM线程
        # self.DataScmToRasp = ScmToRaspThread(self.ser)
        # self.DataScmToRasp.start()

    def connect_server(self):
        host_port = ('192.168.0.11', 6666)
        # socket.AF_INET用于服务器与服务器之间的网络通信
        # socket.SOCK_STREAM代表基于TCP的流式socket通信
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 链接服务器
        client_socket.connect(host_port)
        return client_socket

    # 串口初始化，使用Rasp的GPIO串口
    def serial_init(self):
        # 使用树莓派的GPIO口连接串行口
        ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.5)
        # 打开串口
        ser.open()
        return ser


if __name__ == '__main__':
    s = Main()
    while True:
        pass




