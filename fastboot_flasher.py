from command_runner import run_command

def get_fastboot_device_info(logText, deviceInfoText):
    logText.append("Getting device information in Fastboot mode...")
    output = run_command("fastboot devices")
    if not output or output.strip() == "":
        deviceInfoText.setPlainText("No devices found in Fastboot mode.")
        logText.append("No devices found in Fastboot mode.")
        return
    deviceInfoText.setPlainText(output)

    logText.append("Device(s) found in Fastboot mode:")
    logText.append(output)

    logText.append("Getting detailed device information...")
    device_info = run_command("fastboot getvar all")
    deviceInfoText.append(device_info)
    logText.append(device_info)

def flash_custom_rom(rom_path, logText, progress_signal):
    logText.append(f"Flashing custom ROM from {rom_path}...")

    # Ensure the device is connected in Fastboot mode
    output = run_command("fastboot devices")
    if not output or output.strip() == "":
        logText.append("No devices found in Fastboot mode. Please connect a device.")
        return

    # Flash the custom ROM (example commands, may vary depending on the ROM)
    commands = [
        f"fastboot flash boot {rom_path}/boot.img",
        f"fastboot flash dtbo {rom_path}/dtbo.img",
        f"fastboot flash vendor_boot {rom_path}/vendor_boot.img",
        f"fastboot flash vbmeta {rom_path}/vbmeta.img",
        f"fastboot flash vbmeta_system {rom_path}/vbmeta_system.img",
        "fastboot reboot fastboot",
        f"fastboot flash super {rom_path}/super_empty.img",
        f"fastboot flash system {rom_path}/system.img",
        f"fastboot flash system_ext {rom_path}/system_ext.img",
        f"fastboot flash product {rom_path}/product.img",
        f"fastboot flash vendor {rom_path}/vendor.img",
        "fastboot reboot"
    ]

    total_commands = len(commands)
    for i, command in enumerate(commands):
        logText.append(run_command(command))
        progress_signal.emit(int((i+1) / total_commands * 100))

    logText.append("Flashing complete. Device is rebooting...")
