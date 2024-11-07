#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

    QString filePath;

    void convertTxtToCsv(const QString &txtFile, const QString &csvFile);

    QHash<QString, int> loadGiftValues(QHash<QString, int> &giftValues);

};
#endif // MAINWINDOW_H
