#include "Widget.h"
#include "ui_win.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}


void Widget::on_btnLinkConn_clicked()
{

}

void Widget::on_btnManual_clicked()
{

}

void Widget::on_btnAuto_clicked()
{

}

void Widget::on_btnGoForward_clicked()
{

}

void Widget::on_btnGoBack_clicked()
{

}

void Widget::on_btnGoLeft_clicked()
{

}

void Widget::on_btnGoRight_clicked()
{

}

void Widget::on_btnGoStop_clicked()
{

}

void Widget::on_btnGoUp_clicked()
{

}

void Widget::on_btnGoDown_clicked()
{

}

void Widget::on_btnPIDsend_clicked()
{

}

void Widget::on_btnModeDepthkeep_clicked()
{

}

void Widget::on_btnSpeedSet_clicked()
{

}
