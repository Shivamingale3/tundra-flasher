import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox
from fastboot_flasher import get_fastboot_device_info, flash_custom_rom

class TundraFlasher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Device info section
        self.deviceInfoLabel = QLabel("Device Info:")
        self.deviceInfoText = QTextEdit()
        self.deviceInfoText.setReadOnly(True)
        deviceInfoLayout = QVBoxLayout()
        deviceInfoLayout.addWidget(self.deviceInfoLabel)
        deviceInfoLayout.addWidget(self.deviceInfoText)

        # ROM selection and flash section
        self.romPathLabel = QLabel("ROM Path: None selected")
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browseRom)
        self.flashButton = QPushButton("Flash ROM")
        self.flashButton.setEnabled(False)
        self.flashButton.clicked.connect(self.flashRom)
        romLayout = QVBoxLayout()
        romLayout.addWidget(self.romPathLabel)
        romLayout.addWidget(self.browseButton)
        romLayout.addWidget(self.flashButton)

        # Log section
        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        self.logText.setStyleSheet("background-color: black; color: white;")
        saveLogButton = QPushButton("Save Log")
        saveLogButton.clicked.connect(self.saveLog)

        # Combine all sections
        layout = QHBoxLayout()
        layout.addLayout(deviceInfoLayout)
        layout.addLayout(romLayout)
        mainLayout.addLayout(layout)
        mainLayout.addWidget(QLabel("Logs:"))
        mainLayout.addWidget(self.logText)
        mainLayout.addWidget(saveLogButton)

        self.setLayout(mainLayout)

        self.setWindowTitle("Tundra Flasher")
        self.resize(800, 600)

        # Get device info on startup
        get_fastboot_device_info(self.logText, self.deviceInfoText)

    def browseRom(self):
        romPath = QFileDialog.getExistingDirectory(self, "Select ROM Directory")
        if romPath:
            self.romPathLabel.setText(f"ROM Path: {romPath}")
            self.flashButton.setEnabled(True)
            self.romPath = romPath

    def flashRom(self):
        flash_custom_rom(self.romPath, self.logText)

    def saveLog(self):
        logPath, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt);;All Files (*)")
        if logPath:
            with open(logPath, 'w') as logFile:
                logFile.write(self.logText.toPlainText())
            QMessageBox.information(self, "Success", "Log saved successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TundraFlasher()
    ex.show()
    sys.exit(app.exec_())
