# stm32-secure-bootloader-crc

Secure UART bootloader for STM32F4 featuring sector-based flash programming, CRC32 firmware integrity verification, application validity flag management, and a Python-based firmware update utility.

---

## Overview

This project implements a custom production-style bootloader for the STM32F412 (Cortex-M4).  
It enables reliable firmware updates over UART while ensuring firmware integrity and controlled execution transfer.

The bootloader validates firmware before execution using CRC32 and a persistent application validity flag stored in Flash memory.

---

## Key Features

- UART-based firmware update (115200 baud)
- Sector-based Flash erase (STM32F4 architecture)
- 32-bit aligned Flash programming
- CRC32 integrity verification (polynomial 0xEDB88320)
- Application validity flag stored in Flash
- Stack pointer validation before execution
- Safe jump to application reset handler
- Python-based host firmware uploader

---

## Memory Layout

| Region        | Address        | Description |
|--------------|---------------|------------|
| Bootloader   | 0x08000000    | Bootloader firmware |
| Application  | 0x08010000    | User firmware |
| Valid Flag   | 0x0801FFFC    | Application validity marker |

The application firmware grows upward from `0x08010000`.  
The last 4 bytes of the allocated sector are reserved for metadata.

---

## Firmware Update Flow

1. Bootloader waits for `START` command via UART.
2. Application validity flag is cleared.
3. Flash sectors assigned to the application are erased.
4. Firmware header is received containing:
   - Magic number (0xDEADBEEF)
   - Version
   - Firmware size
   - CRC32 checksum
5. Firmware is written word-by-word to Flash.
6. CRC32 is calculated directly from Flash memory.
7. If CRC matches:
   - Validity flag is written (0xA5A5A5A5)
   - Bootloader jumps to application reset handler.
8. If CRC fails:
   - Update is rejected
   - Bootloader remains active.

---

## Application Validation

An application is considered valid only if:

- The initial stack pointer (first word of vector table) lies within SRAM range:
  
  0x20000000 – 0x20040000

- The validity flag equals:

  0xA5A5A5A5

This prevents execution of corrupted or incomplete firmware images.

---

## CRC32 Implementation

The firmware integrity check uses the standard CRC32 polynomial:

0xEDB88320

The CRC is computed over the flashed firmware region and compared with the transmitted header value before execution is allowed.

---

## Firmware Upload Tool

`firmware_sender.py`

The Python utility performs:

- Serial connection initialization
- START handshake transmission
- Firmware header transfer
- 32-bit aligned binary streaming
- Progress monitoring
- Bootloader response handling

---

## Hardware & Tools

- MCU: STM32F412ZG (ARM Cortex-M4 with FPU)
- IDE: STM32CubeIDE
- Framework: STM32 HAL
- Communication Interface: UART3
- Host Utility: Python 3 with pyserial

---

## Project Structure#

stm32-secure-bootloader-crc/
│
├── Bootloader/
├── application/
├── firmware_sender.py
├── README.md
├── LICENSE
├── .gitignore


---

## Design Objectives

- Reliable firmware update mechanism
- Clear Flash memory partitioning
- Controlled and safe execution transfer
- Firmware integrity assurance
- Production-oriented embedded architecture

---

## License

MIT License
