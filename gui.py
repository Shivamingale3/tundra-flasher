import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from command_runner import run_command
from fastboot_flasher import get_fastboot_device_info, flash_custom_rom

class FlashThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, rom_path):
        super().__init__()
        self.rom_path = rom_path

    def run(self):
        logText = []

        def log(message):
            self.log_signal.emit(message)
            logText.append(message)

        flash_custom_rom(self.rom_path, logText, self.progress_signal)

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

        # Reboot buttons
        rebootSystemButton = QPushButton("Reboot to System")
        rebootSystemButton.clicked.connect(lambda: self.rebootDevice("system"))
        rebootRecoveryButton = QPushButton("Reboot to Recovery")
        rebootRecoveryButton.clicked.connect(lambda: self.rebootDevice("recovery"))
        rebootBootloaderButton = QPushButton("Reboot to Bootloader")
        rebootBootloaderButton.clicked.connect(lambda: self.rebootDevice("bootloader"))
        romLayout.addWidget(rebootSystemButton)
        romLayout.addWidget(rebootRecoveryButton)
        romLayout.addWidget(rebootBootloaderButton)

        # Log section
        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        self.logText.setStyleSheet("background-color: black; color: white;")
        saveLogButton = QPushButton("Save Log")
        saveLogButton.clicked.connect(self.saveLog)

        # Progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)

        # Combine all sections
        layout = QHBoxLayout()
        layout.addLayout(deviceInfoLayout)
        layout.addLayout(romLayout)
        mainLayout.addLayout(layout)
        mainLayout.addWidget(QLabel("Logs:"))
        mainLayout.addWidget(self.logText)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addWidget(saveLogButton)

        self.setLayout(mainLayout)

        self.setWindowTitle("Tundra Flasher")
        self.resize(800, 600)

        # Get device info on startup
        get_fastboot_device_info(self.logText, self.deviceInfoText)

    def browseRom(self):
        romPath = QFileDialog.getExistingDirectory(self, "Select ROM Directory")
        if romPath:
            is_valid, missing_file = self.validate_rom_path(romPath)
            if is_valid:
                self.romPathLabel.setText(f"ROM Path: {romPath}")
                self.flashButton.setEnabled(True)
                self.romPath = romPath
            else:
                QMessageBox.warning(self, "Invalid ROM Path", f"Missing required file: {missing_file}")
                self.flashButton.setEnabled(False)

    def validate_rom_path(self, rom_path):
        required_files = [
            "boot.img", "dtbo.img", "vendor_boot.img", "vbmeta.img",
            "vbmeta_system.img", "super_empty.img", "system.img",
            "system_ext.img", "product.img", "vendor.img"
        ]
        for file in required_files:
            if not os.path.exists(os.path.join(rom_path, file)):
                return False, file
        return True, ""

    def flashRom(self):
        self.flash_thread = FlashThread(self.romPath)
        self.flash_thread.log_signal.connect(self.logText.append)
        self.flash_thread.progress_signal.connect(self.updateProgressBar)
        self.flash_thread.start()

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def rebootDevice(self, mode):
        if mode == "system":
            run_command("fastboot reboot")
        elif mode == "recovery":
            run_command("fastboot reboot recovery")
        elif mode == "bootloader":
            run_command("fastboot reboot bootloader")
        self.logText.append(f"Rebooting to {mode} mode...")

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
