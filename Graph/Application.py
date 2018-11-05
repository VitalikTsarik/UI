import sys
from Graphics.Paint import *
from Graphics.ErrorWindow import ErrorWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    main_window_errors = ErrorWindow(Window)
    sys.exit(app.exec_())
