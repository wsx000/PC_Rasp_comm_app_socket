# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/11 10:56
# @Author: wsx
# @File  : Joystick.py

import pygame
from PyQt5.QtCore import QThread


class Joystick(QThread):
    ###############################
    # 状态 类属性 定义,需要根据功能需求实测补充
    pass
    ###############################

    def __init__(self):
        super().__init__()
        # 模块初始化
        pygame.init()
        pygame.joystick.init()
        # 若只连接了一个手柄，此处带入的参数一般都是0
        self.joystick = pygame.joystick.Joystick(0)
        # 手柄对象初始化
        self.joystick.init()
        # 获取Joystick按钮的数量
        self.buttons = self.joystick.get_numbuttons()
        # 获取Joystick操作轴的数量
        self.axes = self.joystick.get_numaxes()
        # 获取Joystick帽键的数量
        self.hats = self.joystick.get_numhats()

    def run(self):
        while True:
            for event in pygame.event.get():
                # 按键按下或弹起事件
                if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                    for i in range(self.buttons):
                        # 依次获取每个button的状态，状态值：True/False
                        button = self.joystick.get_button(i)
                        # 若第i个按键被按下，进入事件处理程序
                        if button:
                            pass  # 需要实测补充=======================================
                # 轴转动事件
                elif event.type == pygame.JOYAXISMOTION:
                    for i in range(self.axes):
                        # 依次获取每个axis的状态值，状态值：（-1 ~ 1）
                        axis = self.joystick.get_axis(i)
                        pass  # 需要实测补充=======================================
                # 方向键改变事件
                elif event.type == pygame.JOYHATMOTION:
                    # 获取所有方向键状态信息
                    for i in range(self.hats):
                        hat = self.joystick.get_hat(i)
                        if hat[0] == -1:
                            pass  # font/back/left/right# 需要实测补充=======================================
                        if hat[0] == 1:
                            pass  # font/back/left/right# 需要实测补充=======================================
                        if hat[1] == -1:
                            pass  # font/back/left/right# 需要实测补充=======================================
                        if hat[1] == 1:
                            pass  # font/back/left/right# 需要实测补充=======================================


