import sys
from PyQt5.QtWidgets import QApplication
from gui import TundraFlasher

def main():
    app = QApplication(sys.argv)
    ex = TundraFlasher()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
