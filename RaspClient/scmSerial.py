# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/10 13:17
# @Author: wsx
# @File  : scmSerial.py

import threading
import serial
from msg import MsgSendToPC, MsgRevFromPC
from clientSocket import PCToRaspThread
import json


# 接收  单片机发向树莓派的数据
class ScmToRaspThread(threading.Thread):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.lock = threading.Lock()
        self.jmsg = ""
        self.msg = {}

    def run(self):
        """
        brf: 接收来自单片机的数据
        :return:
        """
        while True:
            # 读取数据 readline是读一行，以\n结束，要是没有\n就一直读，阻塞。
            self.jmsg = self.ser.readline()
            self.lock.acquire()
            # 解析收到的json数据
            self.msg = json.loads(self.jmsg)
            self.lock.release()
            # 赋值
            MsgSendToPC.voltage = self.msg["V"]  # 电压
            MsgSendToPC.yaw = self.msg["Y"]  # yaw
            MsgSendToPC.roll = self.msg["R"]  # roll
            MsgSendToPC.pitch = self.msg["P"]  # pitch


# 发送  树莓派发向单片机的数据
class RaspToScmThread(threading.Thread):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.lock = threading.Lock()
        self.msg = {}
        self.move = MsgRevFromPC.move
        self.mode = MsgRevFromPC.mode
        self.depthKeep = MsgRevFromPC.depthKeep
        self.speed = MsgRevFromPC.speed
        self.p = MsgRevFromPC.p
        self.i = MsgRevFromPC.i
        self.d = MsgRevFromPC.d

    def run(self):
        while True:
            if PCToRaspThread.receive_flag:
                self.lock.acquire()
                self.ser.write(self.msg_sendTscm())
                self.lock.release()
            else:
                continue

    # 整合发向单片机的信息
    def msg_sendTscm(self):
        if MsgRevFromPC.move == 'up':
            self.move = "U"  # 上
        elif MsgRevFromPC.move == 'down':
            self.move = "D"  # 下
        elif MsgRevFromPC.move == 'front':
            self.move = "F"  # 前
        elif MsgRevFromPC.move == 'back':
            self.move = "B"  # 后
        elif MsgRevFromPC.move == 'left':
            self.move = "L"  # 左
        elif MsgRevFromPC.move == 'right':
            self.move = "R"  # 右
        else:
            self.move = "S"  # 停

        if MsgRevFromPC.mode == 'auto':
            self.mode = "A"  # 自动
        else:
            self.mode = "M"  # 手动

        self.speed = MsgRevFromPC.speed
        self.depthKeep = MsgRevFromPC.depthKeep
        self.p = MsgRevFromPC.p
        self.i = MsgRevFromPC.i
        self.d = MsgRevFromPC.d
        self.msg = {
            "move": self.move,
            "mode": self.mode,
            "speed": self.speed,
            "depth": self.depthKeep,
            "P": self.p,
            "I": self.i,
            "D": self.d
        }
        return json.dumps(self.msg)
