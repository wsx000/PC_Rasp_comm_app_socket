# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/10 13:28
# @Author: wsx
# @File  : clientSocket.py

import threading
import cv2
import socket
from msg import MsgRevFromPC, MsgSendToPC
# from scmSerial import ScmToRaspThread, RaspToScmThread


# 树莓派接收上位机消息线程
class PCToRaspThread(threading.Thread):
    # 接收标志位
    receive_flag = False

    def __init__(self, client_socket):
        super().__init__()
        self.msgFromPC = MsgRevFromPC()
        self.lock = threading.Lock()
        self.socket = client_socket

    def run(self):
        while True:
            # 帧头，内容为后续数据包的长度,帧头第一个数据是数据长度的位数
            length = self.socket.recv(8)
            # print('收到!' + str(length))
            # 提取有效数据长度信息，注意str(length)的结果为 b'...'
            length = str(length)[3:(3 + eval(str(length)[2]))]
            if length:
                # 接收后续的数据
                revData = self.socket.recv(eval(length))
                # 解析收到的数据,后续在RaspToScmThread线程中发送给单片机
                self.msgFromPC.decode_revPCmsg(revData)
                # 置位标志位，接收完成，Rasp可向SCM发送数据一次
                PCToRaspThread.receive_flag = True


capture_frame_width = 218
capture_frame_height = 218


# 树莓派向上位机发送消息线程
class RaspToPCThread(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        # 获取socket
        self.socket = client_socket
        # 要发送的数据
        self.msgToPC = MsgSendToPC()
        # 参数为视频设备的id ，如果只有一个摄像头可以填0，表示打开默认的摄像头
        self.capture = cv2.VideoCapture(0)
        # 设置图像的宽高
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_frame_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_frame_height)
        # 初始化线程锁
        self.lock = threading.Lock()

    def run(self):
        print(self.socket)
        while True:
            # 从摄像头获取图片
            ret, frame = self.capture.read()
            # cv2.imshow('hh', frame)
            # cv2.waitKey(1)
            # 首先对图片进行链表化，用于存放于msg字典中并生成json数据

            img_list = frame.tolist()
            # print('图大小：' + str(len(str(img_list))))
            # 赋值
            MsgSendToPC.imglist = img_list

            # 上锁
            # self.lock.acquire()
            # 获取json数据
            jsonData = self.msgToPC.integrate_msg()
            # print('jsonData大小：' + str(len(jsonData)))
            # 解锁
            # self.lock.release()

            # 获取json数据的长度
            lengthOFdata = len(jsonData)
            # 获取json数据的长度的位数
            bitsOFlenth = len(str(lengthOFdata))
            # 得到帧头,字符串格式
            fh = str(bitsOFlenth) + str(lengthOFdata)
            # 首先发送图片编码后的长度,8位指定长度补零填充,编码为bytes格式发送
            # print(bytes( str(len(stringData)).ljust(8,'0'), 'UTF-8'))
            self.socket.send((fh.ljust(8, '0')).encode())
            # 接着发送数据体
            self.socket.send(jsonData.encode())



