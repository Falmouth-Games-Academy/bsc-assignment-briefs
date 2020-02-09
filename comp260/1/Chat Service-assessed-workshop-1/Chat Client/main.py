import sys
import PyQt5.QtCore
import PyQt5.QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


import socket
import threading
import time
import json

currentBackgroundThread = None
isRunning = True

def backgroundThread():
    print('Starting backgroundThread')

    global isRunning
    while isRunning:
        print('backgroundThread')
        time.sleep(1)

class ChatClient(QWidget):

    def __init__(self):
        super().__init__()

        self.chatOutput = 0
        self.userInput = 0

        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

    def timerEvent(self):
        print('PyQt Timer Task')

    def OnSendMessage(self):
        entry = self.userInput.text()
        print('OnSendMessage: '+entry)

        self.userInput.setText('')

    def OnSetMessageTarget(self):
        entry = self.clientList.currentRow()
        print('OnSetMessageTarget: '+str(entry))

    def OnChangeName(self):
        entry = self.userName.text()
        print('OnChangeName: ' + entry)

    def initUI(self):
        self.userInput = QLineEdit(self)
        self.userInput.setGeometry(10, 360, 580, 30)
        self.userInput.returnPressed.connect(self.OnSendMessage)

        self.chatOutput = QPlainTextEdit(self)
        self.chatOutput.setGeometry(10, 10, 400, 335)
        self.chatOutput.setReadOnly(True)

        self.privateChatLabel = QLabel(self)
        self.privateChatLabel.setGeometry(420, 15, 150, 10)
        self.privateChatLabel.setText('Private Chat')

        self.clientList = QListWidget(self)
        self.clientList.setGeometry(420, 30, 170, 200)
        self.clientList.clicked.connect(self.OnSetMessageTarget)
        self.clientList.addItem('None')
        self.clientList.setCurrentRow(0)

        self.changeNameLabel = QLabel(self)
        self.changeNameLabel.setGeometry(420, 300, 150, 10)
        self.changeNameLabel.setText('User\'s Name')

        self.userName = QLineEdit(self)
        self.userName.setGeometry(420, 315, 170, 30)
        self.userName.returnPressed.connect(self.OnChangeName)
        self.userName.setText('Change Name')

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Chat Client')
        self.show()

    def closeEvent(self, event):
        global isRunning
        isRunning= False

        if currentBackgroundThread is not None:
            currentBackgroundThread.join()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ChatClient()

    currentBackgroundThread = threading.Thread(target=backgroundThread, args=())
    currentBackgroundThread.start()

    sys.exit(app.exec_())