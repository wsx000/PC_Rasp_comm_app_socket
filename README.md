# PC_Rasp_comm_app_socket
an app based PyQT5 and Socket，it includes a server code running on PC and a client code running on RaspberryPi   
1、该工程是为水下机器人实现上下位机通信编写的。   
2、工程实现了 PC <--> Raspberrypi <--> 单片机 三者之间双向通信。   
3、appServer是上位机代码，运行于PC上，RaspClient是下位机的代码，运行于树莓派上，下位机还可以与单片机通过串口实现通信。   
4、下位机可以把摄像头获取的图片或其他传感器数据传输到上位机PC上，PC上位机可以读取手柄的状态传给下位机，还可以发送其他控制指令到下位机。   
5、上位机基于PyQT5制作界面，界面转换后的py代码保存在UWR文件中。上下位机之间使用Socket-UDP通信，上位机使用了多线程操作。
