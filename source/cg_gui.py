#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
