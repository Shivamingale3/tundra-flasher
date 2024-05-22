import sys
from PyQt5.QtWidgets import QApplication
from gui import FastbootFlasher

def main():
    app = QApplication(sys.argv)
    ex = FastbootFlasher()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()