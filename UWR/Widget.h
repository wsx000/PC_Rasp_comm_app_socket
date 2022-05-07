#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

private slots:
    void on_btnLinkConn_clicked();

    void on_btnManual_clicked();

    void on_btnAuto_clicked();

    void on_btnGoForward_clicked();

    void on_btnGoBack_clicked();

    void on_btnGoLeft_clicked();

    void on_btnGoRight_clicked();

    void on_btnGoStop_clicked();

    void on_btnGoUp_clicked();

    void on_btnGoDown_clicked();

    void on_btnPIDsend_clicked();

    void on_btnModeDepthkeep_clicked();

    void on_btnSpeedSet_clicked();

private:
    Ui::Widget *ui;
};
#endif // WIDGET_H
