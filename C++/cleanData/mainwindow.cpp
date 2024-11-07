#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>
#include <QFileDialog>
#include <QFileInfo>
#include <QDebug>
#include <QMessageBox>
#include <QRegularExpression>
#include <QHash>
#include <QPair>
#include <QCollator>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->uploadButton, &QPushButton::clicked, this, [this](){
        filePath = QFileDialog::getOpenFileName(this, tr("选择文件"), "", tr("文件 (*.txt)"));
        ui->filenameLabel->setText(QFileInfo(filePath).fileName());
    });

    connect(ui->okButton, &QPushButton::clicked, this, [this](){
        QString saveFilePath = QFileDialog::getSaveFileName(nullptr, "保存CSV文件", "", "CSV Files (*.csv)");
        if (saveFilePath.isEmpty()) {
            return;
        }
        convertTxtToCsv(filePath, saveFilePath);
    });
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::convertTxtToCsv(const QString &txtFile, const QString &csvFile)
{
    // 加载礼物价格表
    QHash<QString, int> giftValues;
    giftValues = loadGiftValues(giftValues);
    //qDebug()<<giftValues;

    QFile txt(txtFile);
    QFile csv(csvFile);

    if (!txt.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Failed to open the file";
        return;
    }

    if (!csv.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() << "Failed to create the file";
        return;
    }

    // 写入 UTF-8 BOM 以支持中文显示
    csv.write("\xEF\xBB\xBF");

    QTextStream txtStream(&txt);
    QTextStream csvStream(&csv);

    QString filterZhuBo = ui->zhubo->text();
    QString filterFans = ui->fans->text();
    QString filterGifts = ui->giftName->text();
    QString filterNoGifts = ui->noGiftName->text();

    // 匹配信息：时间、性别、用户名、礼物名、数量、增量和送礼对象
    QRegularExpression regex(R"((\d{2}:\d{2}:\d{2}) \[礼物消息\] \[(.*?)\] (.*?) 送出 (.*?)(?:\s*\(可连击\))? x \d+个，增量(\d+)个(?:，给(.*?))?$)");

    // 累计增量和价值的哈希表
    QHash<QPair<QString, QString>, QPair<int, QString>> cumulativeGifts;
    QHash<QString, int> cumulativeAllValues;

    while (!txtStream.atEnd()) {
        QString line = txtStream.readLine();
        QRegularExpressionMatch match = regex.match(line);

        if (match.hasMatch()) {
            QString userName = match.captured(3).trimmed();
            QString giftName = match.captured(4).trimmed();
            giftName = giftName.replace("(可连击)", "").trimmed();
            int giftIncrement = match.captured(5).toInt();
            QString recipient = match.captured(6).trimmed();

            // 根据筛选条件，跳过不符合的行
            if ((!filterFans.isEmpty() && !userName.contains(filterFans)) ||
                (!filterZhuBo.isEmpty() && (recipient.isEmpty() || !recipient.contains(filterZhuBo))) ||
                (!filterGifts.isEmpty() && !filterGifts.contains(giftName)) ||
                (!filterNoGifts.isEmpty() && filterNoGifts.contains(giftName))) {
                continue;
            }

            if (recipient.isEmpty()) {
                recipient = "无";
            }

            // 生成用于累计增量的键
            QPair<QString, QString> key(userName, giftName);

            // 获取礼物的单价
            int giftValue = giftValues.value(giftName, 0);  // 默认为 0，如果礼物名称不在 price 表中
            if(giftValue==0){
                QMessageBox::information(this, "不存在", giftName);
            }
            int totalValue = giftValue * giftIncrement;

            // 累加增量
            if (cumulativeGifts.contains(key)) {
                cumulativeGifts[key].first += giftIncrement;
                cumulativeGifts[key].second = recipient;
            } else {
                cumulativeGifts[key] = qMakePair(giftIncrement, recipient);
            }

            // 累加总价值
            cumulativeAllValues[userName] += totalValue;
        }
    }

    // 将累计数据存储到一个向量中
    QVector<QVector<QString>> outputData;
    for (auto it = cumulativeGifts.begin(); it != cumulativeGifts.end(); ++it) {
        QVector<QString> row;
        row.append(it.key().first);  // 用户名
        row.append(it.key().second); // 礼物名
        row.append(QString::number(it.value().first));  // 数量

        int giftValue = giftValues.value(it.key().second,0); //礼物单价
        row.append(QString::number(giftValue));

        row.append(it.value().second);  // 送礼对象
        outputData.append(row);
    }

    if (ui->checkBox->isChecked()) {
        QCollator collator;
        collator.setLocale(QLocale::Chinese);
        std::sort(outputData.begin(), outputData.end(), [&collator](const QVector<QString>& a, const QVector<QString>& b) {
            return collator.compare(a[0].trimmed(), b[0].trimmed()) < 0;
        });
    }

    bool calculateTotal = ui->numCheckBox->isChecked();
    if (calculateTotal) {
        QList<QPair<QString,int>> sortedGifts;
        for (auto it = cumulativeAllValues.begin(); it != cumulativeAllValues.end(); ++it) {
            sortedGifts.append(qMakePair(it.key(), it.value()));
        }

        std::sort(sortedGifts.begin(), sortedGifts.end(), [](const QPair<QString, int>& a, const QPair<QString, int>& b) {
            return a.second > b.second;
        });

        csvStream << "用户名,礼物名,总价值\n";
        for (const auto& userGift : sortedGifts) {
            QString userName = userGift.first;
            int total = userGift.second;

            QString giftColumn = filterGifts.isEmpty() ? "所有礼物" : filterGifts;
            csvStream << QString("%1,%2,%3\n").arg(userName).arg(giftColumn).arg(total);
        }
    } else {
        csvStream << "用户名,礼物名,数量,礼物价值,送礼对象\n";
        for (const auto& row : outputData) {
            csvStream << row.join(",") << "\n";
        }
    }

    txt.close();
    csv.close();

    QMessageBox::information(this, "提示", "保存成功");
}

// 读取 gift_values.txt 文件，加载礼物名及其对应的价值到 giftValues 中
QHash<QString, int> MainWindow::loadGiftValues(QHash<QString, int> &giftValues)
{
    QString giftPath = QFileDialog::getOpenFileName(this, tr("选择礼物信息文件"), "", tr("文件 (*.txt)"));
    QFile giftFile(giftPath);
    if(!giftFile.exists()){
        qDebug()<<"文件不存在";
    }
    if (!giftFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Failed to open gift_values.txt";
        return {};
    }

    QTextStream in(&giftFile);
    QString giftName;
    int lineNumber = 0;

    while (!in.atEnd()) {
        // 读取礼物名
        giftName = in.readLine().trimmed();
        giftName = giftName.replace("(可连击)", "").trimmed();
        lineNumber++;

        // 检查礼物名是否为空
        if (giftName.isEmpty()) {
            //qDebug() << "Empty gift name at line" << lineNumber;
            continue; // 跳过空行
        }

        // 读取礼物的价值
        QString valueStr = in.readLine().trimmed();
        lineNumber++;

        bool ok;
        double giftValue = valueStr.toDouble(&ok);
        if (ok) {
            giftValues[giftName] = giftValue;
            //qDebug() << "Loaded gift:" << giftName << "with value:" << giftValue;
        } else {
            qDebug() << "Invalid value for gift" << giftName << "at line" << lineNumber;
        }
    }

    giftFile.close();

    return giftValues;
}
