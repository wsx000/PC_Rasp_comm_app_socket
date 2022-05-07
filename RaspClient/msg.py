# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/10 12:40
# @Author: wsx
# @File  : msg.py

import json


class MsgSendToPC(object):
    # 需要发送的数据
    imglist = list()  # 创建空列表
    depth = 10.0  # 深度
    voltage = 3.3  # 电压
    yaw = 20.0  # 欧拉角 航向
    roll = 30.0  # 欧拉角 翻滚
    pitch = 40.0  # 欧拉角 俯仰

    def __init__(self):
        self.msg = {}

    def integrate_msg(self):
        """
        brief: 整合要发送给上位机的数据，并转换为json格式。
               msg中每个key对应的可选values分别如下：
               imglist： 列表格式——将图像数据保存为列表格式存储，以便转换为json格式
               depth： 机器人水下深度
               voltage： 机器人电源电压
               yaw： 机器人航向角
               roll： 机器人翻滚角
               pitch： 机器人俯仰角
        :return: json数据
        """
        self.msg = {
            "imglist": MsgSendToPC.imglist,  # 列表类型的图像数据，接收后需转换为图像数据
            "statement": {
                "depth": MsgSendToPC.depth,
                "voltage": MsgSendToPC.voltage,
                "yaw": MsgSendToPC.yaw,
                "roll": MsgSendToPC.roll,
                "pitch": MsgSendToPC.pitch
            }
        }
        # 将字典类型转换为json数据格式
        self.msg = json.dumps(self.msg)
        return self.msg


"""--------------------------------------------------------------------------------
brf: 创建处理接收消息的类，发送时以json形式发送，msg中每个key对应的可选values分别如下：
    move: stop/停止, front/前进, back/后退, left/向左, right/向右, up/向上, down/向下
    depthKeep: 定深模式 值为0时即取消定深模式
    speed: 0~400的整数值，代表占空比
    mode: auto/自动, manual/手动
    pid: p-比例值
         i-积分值
         d-微分值
    接收到的数据格式为：
            msg = {
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
--------------------------------------------------------------------------------"""
class MsgRevFromPC():
    mode = "auto"
    move = "stop"
    # 定深值，为0时即取消定深功能
    depthKeep = 0
    # 速度值
    speed = 0
    # pid参数设置
    p = 0
    i = 0.0
    d = 0.0

    def __init__(self):
        self.msg = {}

    def decode_revPCmsg(self, BytesMsgRev):
        """
        brf: 解析收到的数据
        :param BytesMsgRev:
        :return: None
        """
        # 将接收到的bytes数据转换成字符串（json）
        jsonMsg = BytesMsgRev.decode('utf-8')
        print('已接收: ', jsonMsg)
        # 将json数据解析成dict数据
        self.msg = json.loads(jsonMsg)
        # 赋值
        MsgRevFromPC.mode = self.msg['mode']
        MsgRevFromPC.move = self.msg['move']
        MsgRevFromPC.speed = self.msg['speed']
        MsgRevFromPC.depthKeep = self.msg['depthKeep']
        MsgRevFromPC.p = self.msg['pid']['p']
        MsgRevFromPC.i = self.msg['pid']['i']
        MsgRevFromPC.d = self.msg['pid']['d']

    def get_mode(self):
        return MsgRevFromPC.mode

    def get_move(self):
        return MsgRevFromPC.move

    def get_speed(self):
        return MsgRevFromPC.speed

    def get_depthKeep(self):
        return MsgRevFromPC.depthKeep

    def get_p(self):
        return MsgRevFromPC.p

    def get_i(self):
        return MsgRevFromPC.i

    def get_d(self):
        return MsgRevFromPC.d



