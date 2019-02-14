# -*- coding:utf-8 -*-

import sys
import os
import qtawesome
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import  QSettings, QUrl, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QMessageBox,
        QPushButton,QTextEdit)
from PyQt5.QtNetwork import (QAbstractSocket, QHostInfo, QNetworkConfiguration,
        QNetworkConfigurationManager, QNetworkInterface, QNetworkSession,
        )




class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.networkSession = None
        self.blockSize = 0
        self.currentFortune = ''
        self.title = "动漫日剧通知下载程序"

        hostLabel = QLabel('IP：')
        hostLabel.setFont(qtawesome.font('fa', 14))

        portLabel = QLabel('端口：')
        portLabel.setFont(qtawesome.font('fa', 14))

        self.serverMsgLable = QLabel( '来自服务端的消息：')
        self.serverMsgLable.setFont(qtawesome.font('fa', 14))

        self.sendMsgLabel = QLabel( '将要发送的消息：')
        self.sendMsgLabel.setFont(qtawesome.font('fa', 14))

        self.hostCombo = QComboBox()
        self.hostCombo.setEditable(True)

        name = QHostInfo.localHostName()
        if name != '':
            self.hostCombo.addItem(name)
            self.hostCombo.addItem('111.231.82.173')

            domain = QHostInfo.localDomainName()
            if domain != '':
                self.hostCombo.addItem(name + '.' + domain)


        ipAddressesList = QNetworkInterface.allAddresses()

        for ipAddress in ipAddressesList:
            if not ipAddress.isLoopback():
                self.hostCombo.addItem(ipAddress.toString())

        for ipAddress in ipAddressesList:
            if ipAddress.isLoopback():
                self.hostCombo.addItem(ipAddress.toString())

        self.portLineEdit = QLineEdit()
        self.portLineEdit.setValidator(QIntValidator(1, 65535, self))
        self.portLineEdit.setPlaceholderText("请输入端口")

        # self.taskLineEdit = QLineEdit()
        # self.taskLineEdit.setPlaceholderText("请向组长询问后输入任务码")
        # self.taskLineEdit.setValidator(QIntValidator(1, 9999, self))

        #self.serverLineEdit = QTextEdit()
        #self.serverLineEdit.setPlaceholderText('服务器发送的消息会显示在这里')
        self.serverLineEdit = QComboBox()
        self.serverLineEdit.setEditable(True)

        self.sendTextEdit = QComboBox()
        self.sendTextEdit.setEditable(True)
        #self.sendTextEdit = QTextEdit()
        #self.sendTextEdit.setPlaceholderText('请输入先要发送给服务器的消息')

        hostLabel.setBuddy(self.hostCombo)
        portLabel.setBuddy(self.portLineEdit)
        # taskCodeLabel.setBuddy(self.taskLineEdit)
        self.serverMsgLable.setBuddy(self.serverLineEdit)
        self.sendMsgLabel.setBuddy(self.sendTextEdit)

        self.statusLabel = QLabel("状态：尚未连接")
        self.statusLabel.setAutoFillBackground(True)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        palette = QPalette()  # 新建一个调色板
        palette.setColor(QPalette.Window, Qt.red)  # 设置颜色
        self.statusLabel.setPalette(palette)
        self.statusLabel.setStyleSheet('''
                color:#ffffff;
                font-size:18px;
                font-weight:bold;
        ''')

        self.getFortuneButton = QPushButton("启动连接")
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)

        quitButton = QPushButton("退出")
        self.stopButton = QPushButton("中止连接")
        self.stopButton.setDefault(True)
        self.stopButton.setEnabled(False)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.stopButton, QDialogButtonBox.AcceptRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)
        self.sendMsgbutton = QPushButton('发送消息')
        self.webSocket = QWebSocket()
        self.changeMsg = QWebSocket()

        self.hostCombo.editTextChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        # self.taskLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.CreateNewConn)
        self.stopButton.clicked.connect(self.stopCurrentConn)
        quitButton.clicked.connect(self.close)
        self.webSocket.connected.connect(self.websocketConnect)
        self.webSocket.disconnected.connect(self.webSocketDisconnect)
        self.webSocket.error.connect(self.displayError)
        self.webSocket.textMessageReceived.connect(self.webSocketMessageReceived)
        self.changeMsg.connected.connect(self.websocketConnect)
        self.changeMsg.disconnected.connect(self.webSocketDisconnect)
        self.changeMsg.error.connect(self.displayError)
        # self.sendTextEdit.textChanged.connect(self.enableSendMessageButton)
        self.sendTextEdit.editTextChanged.connect(self.enableSendMessageButton)
        self.sendMsgbutton.clicked.connect(self.sendMsgToServer)

        mainLayout = QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostCombo, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        # mainLayout.addWidget(taskCodeLabel, 2, 0)
        # mainLayout.addWidget(self.taskLineEdit, 2, 1)
        mainLayout.addWidget(self.statusLabel, 3, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 4, 0, 1, 2)
        mainLayout.addWidget(self.serverMsgLable,5,0)
        mainLayout.addWidget(self.serverLineEdit, 5, 0, 5, 5)
        mainLayout.addWidget(self.sendMsgLabel,10,0)
        mainLayout.addWidget(self.sendTextEdit,10,0,5,5)
        mainLayout.addWidget(self.sendMsgbutton, 15, 0,6,6)
        self.serverLineEdit.setEnabled(True)
        self.serverMsgLable.setVisible(False)
        self.serverLineEdit.setVisible(False)
        self.sendMsgLabel.setVisible(False)
        self.sendTextEdit.setVisible(False)
        self.sendMsgbutton.setEnabled(False)
        self.sendMsgbutton.setVisible(False)
        self.setLayout(mainLayout)
        mainLayout.setSpacing(10)
        self.setWindowTitle(self.title)
        self.portLineEdit.setFocus()
        manager = QNetworkConfigurationManager()
        if manager.capabilities() & QNetworkConfigurationManager.NetworkSessionRequired:
            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            id = settings.value('DefaultNetworkConfiguration')
            settings.endGroup()

            config = manager.configurationFromIdentifier(id)
            if config.state() & QNetworkConfiguration.Discovered == 0:
                config = manager.defaultConfiguration()

            self.networkSession = QNetworkSession(config, self)
            self.networkSession.opened.connect(self.sessionOpened)

            self.getFortuneButton.setEnabled(False)
            self.statusLabel.setText("Opening network session.")
            self.networkSession.open()

    def enableSendMessageButton(self):
        # self.sendMsgbutton.setEnabled(self.sendTextEdit.toPlainText()!= '')
        self.sendMsgbutton.setEnabled(
            (self.networkSession is None or self.networkSession.isOpen())
            # and self.hostCombo.currentText() != ''
            # and self.portLineEdit.text() != ''
            # and self.taskLineEdit.text() != ''
        )

    def sendMsgToServer(self):
        # message =self.sendTextEdit.toPlainText()
        message =self.sendTextEdit.currentText()
        msg = message.split('|')[1]
        # url = QUrl('ws://0.0.0.0:5000/')
        # self.changeMsg.open(url)
        self.changeMsg.sendTextMessage(msg)
        # self.webSocket.sendTextMessage(message)

    def CreateNewConn(self):
        '''
        连接按钮点击事件，尝试进行连接 QWebSocket
        :return:
        '''
        self.getFortuneButton.setText("连接中，请等待")
        self.getFortuneButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.webSocket.abort()
        host = self.hostCombo.currentText()
        port = self.portLineEdit.text()
        # task_code = self.taskLineEdit.text()
        # format_url = 'ws://{}:{}/websocket/master/{}/{}'.format(host,port,'xiangjqjngkljjkl12345',task_code)
        format_url = 'ws://{}:{}/'.format(host,port)
        request_url = QUrl(format_url)
        url = QUrl('ws://0.0.0.0:4000/')
        self.changeMsg.open(url)
        self.webSocket.open(request_url)

    def stopCurrentConn(self):
        if self.webSocket is not None and self.webSocket.isValid():
            print('终止连接')
            self.getFortuneButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.webSocket.close(QWebSocketProtocol.CloseCodeNormal,reason='终止连接')
            self.webSocket.close()

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self,self.title,"找不到主机。请检查主机名和端口设置")
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, self.title,'''
            连接被同伴拒绝了。确保服务器正在运行，并检查主机名端口设置正确
            ''')
        else:
            QMessageBox.information(self, self.title,"出现下列错误: %s." % self.webSocket.errorString())

        self.getFortuneButton.setEnabled(True)
        self.getFortuneButton.setText("重新连接")

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(
                (self.networkSession is None or self.networkSession.isOpen())
                and self.hostCombo.currentText() != ''
                and self.portLineEdit.text() != ''
                # and self.taskLineEdit.text() != ''
        )

    def sessionOpened(self):
        config = self.networkSession.configuration()

        if config.type() == QNetworkConfiguration.UserChoice:
            id = self.networkSession.sessionProperty('UserChoiceConfiguration')
        else:
            id = config.identifier()

        settings = QSettings(QSettings.UserScope, 'QtProject')
        settings.beginGroup('QtNetwork')
        settings.setValue('DefaultNetworkConfiguration', id)
        settings.endGroup()

        self.statusLabel.setText("This examples requires that you run the "
                            "Fortune Server example as well.")
        self.enableGetFortuneButton()

    def websocketConnect(self):
        print("websocketConnect")
        self.statusLabel.setText('连接成功')
        self.serverMsgLable.setVisible(True)
        self.serverLineEdit.setVisible(True)
        self.sendMsgLabel.setVisible(True)
        self.sendTextEdit.setVisible(True)
        self.sendMsgbutton.setVisible(True)

    def webSocketDisconnect(self):
        self.statusLabel.setText('连接退出')
        self.getFortuneButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.serverMsgLable.setVisible(False)
        self.serverLineEdit.setVisible(False)
        self.sendMsgLabel.setVisible(False)
        self.sendTextEdit.setVisible(False)
        self.sendMsgbutton.setVisible(False)
        self.getFortuneButton.setText('重新连接')
        print("disconnected")

    def webSocketMessageReceived(self,p_str):
        if p_str:
            notify("关注的动漫日剧已更新", "关注的动漫日剧已更新")
        self.serverLineEdit.clear()
        self.sendTextEdit.clear()
        for i in p_str.split(','):
            self.serverLineEdit.addItem(i)
            self.sendTextEdit.addItem(i)
        # self.serverLineEdit.setText(p_str)
        # self.statusLabel.setText('接收到消息'+p_str)
        print ("webSocketMessageReceived"+p_str)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def mainUI():
    app = QApplication(sys.argv)
    app.addLibraryPath('./plugins')
    client = Client()
    client.show()
    sys.exit(client.exec_())


if __name__ == '__main__':
    mainUI()