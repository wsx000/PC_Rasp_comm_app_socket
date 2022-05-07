# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/6 17:59
# @Author: wsx
# @File  : msgRev.py

import json


class msgRev(object):
    def __init__(self):
        # 定义需要从接收数据中解析出来的数据
        self.imglist = list()  # 创建空列表
        self.depth = 0.0  # 深度
        self.voltage = 0.0  # 电压
        self.yaw = 0.0  # 欧拉角 航向
        self.roll = 0.0  # 欧拉角 翻滚
        self.pitch = 0.0  # 欧拉角 俯仰

    def decode_msgRev(self, BytesMsgRev):
        """
        brf: 解析收到的数据
        :param BytesMsgRev:
        :return: None
        """
        # 将接收到的bytes数据转换成字符串（json）
        jsonMsg = BytesMsgRev.decode('utf-8')
        # 将json数据解析成dict数据
        Msg = json.loads(jsonMsg)
        # 赋值
        self.imglist = Msg['imglist']
        self.depth = Msg['statement']['depth']
        self.voltage = Msg['statement']['voltage']
        self.yaw = Msg['statement']['yaw']
        self.roll = Msg['statement']['roll']
        self.pitch = Msg['statement']['pitch']

    def get_imglist(self):
        return self.imglist

    def get_depth(self):
        return self.depth

    def get_voltage(self):
        return self.voltage

    def get_yaw(self):
        return self.yaw

    def get_roll(self):
        return self.roll

    def get_pitch(self):
        return  self.pitch



