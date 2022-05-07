# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/1/16 13:15
# @Author: wsx
# @File  : MyThread.py

import sys
import socket
from PyQt5.QtCore import pyqtSignal, QThread, QObject, QSize, QMutex
from PIL import Image
from appServer.msgRev import msgRev
from appServer.msgSend import msgSend
import time


# ================================================#
#                 数据接收线程类                    #
# ================================================#
class SocketRevThread(QThread, QObject):
    # 定义一个处理接收的数据（含图片）的信号
    signal_revMsg_deal = pyqtSignal()
    conn = None
    addr = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.msgrev = msgRev()
        self.server_socket = None

    def run(self):
        """
        brf: 重写run函数，数据接收线程，一直循环接收
        :return:
        """
        while True:
            # 帧头，内容为后续数据包的长度,帧头第一个数据是数据长度的位数
            length = self.recv_size(SocketRevThread.conn, 8)
            # 提取有效数据长度信息，注意str(length)的结果为 b'...'
            length = str(length)[3:(3+eval(str(length)[2]))]
            if length:
                # 接收后续的数据
                revData = self.recv_all(SocketRevThread.conn, eval(length))
                # 解析收到的数据
                self.msgrev.decode_msgRev(revData)
                # 向槽函数发射图片信息
                self.signal_revMsg_deal.emit()

    def tcp_server_start(self, port):
        """
        brf: 开启并建立TCP连接
        :return: None
        """
        # socket.AF_INET用于服务器与服务器之间的网络通信
        # socket.SOCK_STREAM代表基于TCP的流式socket通信
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次挥手后的TIME_WAIT状态
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置套接字为非阻塞式
        # self.server_socket.setblocking(False)
        # 尝试连接
        try:
            self.server_socket.bind(('', port))  # 绑定socket
        except Exception as ret:
            pass
        # 只有在try中的语句正常执行时才执行else中的语句
        else:
            self.server_socket.listen(1)  # 监听窗口数设置
            SocketRevThread.conn, SocketRevThread.addr = self.server_socket.accept()  # 接收来自客户端的连接请求
            print('已连接')
            print(SocketRevThread.conn)

    def recv_size(self, sock, count):
        """
        rbf: 接收图片大小信息
        :param sock:
        :param count: 接收帧头数据的长度
        :return:
        """
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def recv_all(self, sock, count):
        """
        brf: 接收图片数据
        :param sock:
        :param count: 由帧头解析出来的图片数据的长度
        :return:
        """
        buf = b''
        while count:
            # s.recv(bufsize[,flag]) 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。
            newbuf = sock.recv(count)
            if not newbuf:
                print('exit')
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf


# ================================================#
#                 数据发送线程类                    #
# ================================================#
class SocketSendThread(QThread, QObject):
    # 定义消息发送信号，消息状态每改变一次就启动一次该信号
    signal_sendMsg_once = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.msgsend = msgSend()
        self.lock = QMutex()

    def run(self):
        """
        brief: 数据发送线程，每当上位机中要发送的数据改变一次就触发一次
        :return:
        """
        # 数据发送
        # self.lock.lock()
        jsonData = self.msgsend.msgTojson()
        # self.lock.unlock()
        print('发送: ', jsonData)
        # 获取json数据的长度
        lengthOFdata = len(jsonData)
        # 获取json数据的长度的位数
        bitsOFlenth = len(str(lengthOFdata))
        # 得到帧头,字符串格式
        fh = str(bitsOFlenth) + str(lengthOFdata)
        # 首先发送图片编码后的长度,8位指定长度补零填充,编码为bytes格式发送
        SocketRevThread.conn.send((fh.ljust(8, '0')).encode())
        # 接着发送数据体
        SocketRevThread.conn.send(jsonData.encode())








