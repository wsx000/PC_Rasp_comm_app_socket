# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/6 17:58
# @Author: wsx
# @File  : msgSend.py

import json

"""--------------------------------------------------------------------------------
brf: 创建处理要发送的消息的类，发送时以json形式发送，msg中每个key对应的可选values分别如下：
    move: stop/停止, front/前进, back/后退, left/向左, right/向右, up/向上, down/向下
    depthKeep: 定深模式 值为0时即取消定深模式
    speed: 0~400的整数值，代表占空比
    mode: auto/自动, manual/手动
    pid: p-比例值
         i-积分值
         d-微分值
--------------------------------------------------------------------------------"""
class msgSend():
    # mode = "auto"
    # move = "stop"
    # # 定深值，为0时即取消定深功能
    # depthKeep = 0
    # # 速度值
    # speed = 0
    # # pid参数设置
    # p = 0.0
    # i = 0.0
    # d = 0.0

    def __init__(self):
        self.mode = "auto"
        self.move = "stop"
        # 定深值，为0时即取消定深功能
        self.depthKeep = 0
        # 速度值
        self.speed = 0
        # pid参数设置
        self.p = 10.0
        self.i = 0.1
        self.d = 30.0
        self.msg = {
            "mode": self.mode,  # 手动/自动模式
            "move": self.move,        # 运动方向设置
            "speed": self.speed,   # 运动速度设置
            "depthKeep": self.depthKeep,  # 定深模式使能/失能
            "pid": {               # pid参数
                "p": self.p,
                "i": self.i,
                "d": self.d
            }
        }

    def set_mode(self, value):
        self.mode = value

    def set_depthKeep(self, value):
        self.depthKeep = value

    def set_move(self, value):
        self.move = value

    def set_speed(self, value):
        self.speed = value

    def set_pid_p(self, value):
        self.p = value

    def set_pid_i(self, value):
        self.i = value

    def set_pid_d(self, value):
        self.d = value

    def msgTojson(self):
        """
        brf: 将dict数据类型转换为json数据
        :return: msg
        """
        self.msg = {
            "mode": self.mode,  # 手动/自动模式
            "move": self.move,        # 运动方向设置
            "speed": self.speed,   # 运动速度设置
            "depthKeep": self.depthKeep,  # 定深模式使能/失能
            "pid": {               # pid参数
                "p": self.p,
                "i": self.i,
                "d": self.d
            }
        }
        msg = json.dumps(self.msg)
        return msg

