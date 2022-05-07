# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/9 19:31
# @Author: wsx
# @File  : ui_EventDeal.py

# from UWR.ui_win import Ui_Widget
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtCore import pyqtSignal, QObject,  pyqtSlot
# from app.msgSend import msgSend
#
#
# class EventDeal(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.__ui = Ui_Widget()  # 创建UI对象
#         self.__ui.setupUi(self)  # 构造UI
#         self.msg = msgSend()  # 创建消息发送对象
#
#     # 搁这儿放个装饰器，可以防止on_btnLinkConn_clicked函数执行两遍，具体为啥有待深究
#     @pyqtSlot()
#     def on_btnLinkConn_clicked(self):
#         """
#         brf: 实现“建立连接”按键程序
#         :return:
#         """
#         # 获取输入的端口号
#         port = int(self.__ui.lineEditPortNum.text())
#         self.socThread.tcp_server_start(port)
#         # 开启线程
#         self.socThread.start()
#         print('ok')
#         # self.__ui.btnLinkConn.setEnabled(False)  # 失能按钮
#
#     def on_btnManual_clicked(self):
#         # 失能自动控制按钮
#         self.__ui.btnAuto.setEnabled(False)


