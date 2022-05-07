# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/1/16 13:25
# @Author: wsx
# @File  : appMain.py


import sys
from PyQt5.QtWidgets import QWidget, QApplication
from UWR.ui_win import Ui_Widget
from PyQt5.QtCore import pyqtSignal, QObject,  pyqtSlot
import time
from appServer.MyThread import SocketRevThread, SocketSendThread
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread, QObject, QSize
from PyQt5.Qt import QIcon
import numpy as np


class myWindow(QWidget, QObject):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Widget()  # 创建UI对象
        self.ui.setupUi(self)      # 构造UI
        # 自定义槽函数
        self.ui.sliderSpeedSet.valueChanged.connect(self.do_speedChanged)
        self.ui.sliderDepthNum.valueChanged.connect(self.do_depthChanged)
        # 创建socket接收线程
        self.socRevThread = SocketRevThread()
        self.socRevThread.signal_revMsg_deal.connect(self.revMsg_deal)
        # 创建socket发送线程
        self.socSendThread = SocketSendThread()
        self.socSendThread.signal_sendMsg_once.connect(self.sendMsgOnce)

    # 搁这儿放个装饰器，可以防止on_btnLinkConn_clicked函数执行两遍，具体为啥有待深究
    @pyqtSlot()
    def on_btnLinkConn_clicked(self):
        """
        brf: 实现"建立连接"按键程序
        :return:
        """
        # 获取输入的端口号
        port = int(self.ui.lineEditPortNum.text())
        # 连接客户端
        self.socRevThread.tcp_server_start(port)
        self.ui.imgLable.setText('TCP已连接')
        # 开启接收线程
        self.socRevThread.start()
        # 发送线程在后面每次有信息改变时开启

    @pyqtSlot()
    def on_btnManual_clicked(self):
        """
        brief: "手动"按钮处理函数
        :return: None
        """
        # 失能该控制按钮,并使能"自动"按钮及运动按钮
        self.ui.btnManual.setEnabled(False)
        self.ui.btnAuto.setEnabled(True)
        self.ui.btnGoForward.setEnabled(True)
        self.ui.btnGoBack.setEnabled(True)
        self.ui.btnGoLeft.setEnabled(True)
        self.ui.btnGoRight.setEnabled(True)
        self.ui.btnGoStop.setEnabled(True)
        self.ui.btnGoUp.setEnabled(True)
        self.ui.btnGoDown.setEnabled(True)
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_mode("manual")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnAuto_clicked(self):
        """
        brief: "自动"按钮处理函数
        :return: None
        """
        # 失能该控制按钮及运动按钮,并使能"自动"按钮
        self.ui.btnAuto.setEnabled(False)
        self.ui.btnManual.setEnabled(True)
        self.ui.btnGoForward.setEnabled(False)
        self.ui.btnGoBack.setEnabled(False)
        self.ui.btnGoLeft.setEnabled(False)
        self.ui.btnGoRight.setEnabled(False)
        self.ui.btnGoStop.setEnabled(False)
        self.ui.btnGoUp.setEnabled(False)
        self.ui.btnGoDown.setEnabled(False)
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_mode("auto")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoForward_clicked(self):
        """
        brief: 手动模式下前进按钮事件处理函数
        :return: None
        """
        # # 更改按钮显示，下次再按一下则表示"停"
        # self.ui.btnGoForward.setText('停')
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("front")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoBack_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("back")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoLeft_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("left")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoRight_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("right")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoStop_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("stop")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoUp_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("up")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnGoDown_clicked(self):
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_move("down")
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnPIDsend_clicked(self):
        """
        brief: pid参数发送按钮
        :return: None
        """
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_pid_p(eval(self.ui.lineEditP.text()))
        self.socSendThread.msgsend.set_pid_i(eval(self.ui.lineEditI.text()))
        self.socSendThread.msgsend.set_pid_d(eval(self.ui.lineEditD.text()))
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnModeDepthkeep_clicked(self):
        """
        brief: 定深模式下的按钮
        :return: None
        """
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_depthKeep(self.ui.sliderDepthNum.value())
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    @pyqtSlot()
    def on_btnSpeedSet_clicked(self):
        """
        brief: 设置速度值按钮
        :return: None
        """
        # 修改数据发送数据体内相应的参数
        self.socSendThread.msgsend.set_speed(self.ui.sliderSpeedSet.value())
        # 开启发送消息线程，发送一次信息
        self.sendMsgOnce()

    def do_speedChanged(self, value):
        """
        brief: 显示速度滑块的当前值
        :param value: 速度滑块的当前值
        :return:
        """
        self.ui.labelSpeedNum.setText(str(value))

    def do_depthChanged(self, value):
        """
        brief: 显示定深滑块的当前值
        :param value: 定深滑块的当前值
        :return:
        """
        self.ui.labelDepthNum.setText(str(value)+'cm')

    def revMsg_deal(self):
        """
        brf: 处理接受的数据
        :param msg: 由接收server接收端发射来的图片数据
        :return: None
        """
        # print("接收到发射信号")
        # 提取图片数据
        img = np.array(self.socRevThread.msgrev.get_imglist(), dtype=np.uint8)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        QtImg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888)
        # 调整显示框的大小
        self.ui.imgLable.resize(QSize(img_rgb.shape[1], img_rgb.shape[0]))
        # 显示图片到label中
        self.ui.imgLable.setPixmap(QPixmap.fromImage(QtImg))
        # 显示其他数据
        self.ui.textBrowserVoltage.setText(str(self.socRevThread.msgrev.get_voltage()) + 'V')
        self.ui.textBrowserDepth.setText(str(self.socRevThread.msgrev.get_depth()) + 'cm')
        self.ui.textBrowserYaw.setText(str(self.socRevThread.msgrev.get_yaw()) + '°')
        self.ui.textBrowserRoll.setText(str(self.socRevThread.msgrev.get_roll()) + '°')
        self.ui.textBrowserPitch.setText((str(self.socRevThread.msgrev.get_pitch())) + '°')

    def sendMsgOnce(self):
        self.socSendThread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = myWindow()
    myApp.setWindowTitle('MIN')
    # icon = QIcon
    myApp.setWindowIcon(QIcon("format.ico"))  # 设置软件图标，自己找一张.ico图片放进来即可
    myApp.show()
    sys.exit(app.exec_())


