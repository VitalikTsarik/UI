import sys
from Graphics.Paint import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_())
