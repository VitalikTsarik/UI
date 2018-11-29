import sys
from PyQt5.QtWidgets import QApplication
from source.graphics.paint import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_())
