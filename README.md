# STM32 Secure Bootloader with CRC Validation & UART Firmware Update

##  Overview
This project implements a production-style custom bootloader for STM32 microcontrollers that supports UART-based firmware updates, CRC32 integrity verification, and safe application jumping. The system simulates a real embedded firmware lifecycle used in industrial, automotive, IoT, and robotics products.

The bootloader receives a firmware binary via UART, writes it to flash memory, verifies its integrity using CRC32, and safely jumps to the application firmware only if validation is successful. If the firmware is invalid or corrupted, the system remains in bootloader mode to prevent unsafe execution.

This project focuses on:
- Firmware lifecycle management
- Flash memory partitioning
- Boot sequence control
- Embedded communication protocols
- Reliability and fault-safe firmware design

---

## Key Features
- Custom bootloader written in Embedded C (STM32 HAL)
- UART-based firmware update protocol
- CRC32 integrity verification after flash programming
- Flash erase and programming using internal flash
- Application validity flag mechanism
- Safe jump to application firmware
- Python-based firmware uploader tool
- Real hardware testing on STM32 board
- Structured boot flow logging via UART

---

##  System Architecture
PC (Firmware.bin)  
        ↓ (UART Serial Protocol)  
STM32 Bootloader (Flash Sector 0)  
        ↓  
Flash Memory (Application Region)  
        ↓  
CRC Verification + Validity Flag Check  
        ↓  
Jump to Application Firmware (if valid)    

---

##  Flash Memory Layout (Example)
| Region      | Address Range        | Description                  |
|-------------|----------------------|------------------------------|
| Bootloader  | 0x08000000 - 0x0800FFFF | Bootloader firmware       |
| Application | 0x08010000 - 0x0801FFFB | Main application firmware |
| Validity Flag | 0x0801FFFC          | Firmware validity marker     |

Note: Flash addresses may vary depending on the STM32 microcontroller used.

---

## Hardware Used
- STM32 Development Board (Nucleo STM32f412ZG)
- ST-Link Debugger (on-board or external)
- USB Cable (for programming and UART communication)
- PC / Laptop (for firmware upload)
- Optional: External UART adapter (if needed)

---

##  Software & Tools
- STM32CubeIDE
- STM32 HAL Drivers
- Python 3.x
- PySerial Library
- GCC ARM Toolchain
- Serial Terminal (PuTTY / TeraTerm / CoolTerm)
- Git & GitHub
- stmCUbePrograme

---

## Boot Process Flow
1. MCU resets and starts execution from Bootloader (0x08000000)
2. Bootloader initializes peripherals (UART, Flash, CRC)
3. Bootloader checks firmware validity flag
4. If firmware is valid:
   - Compute CRC of application region
   - Compare with expected CRC
   - Jump to application firmware
5. If firmware is invalid or CRC fails:
   - Enter UART firmware update mode

---

##  Firmware Update Flow
START Command → Receive Firmware Header →  Flash Erase → Chunked Firmware Write →  CRC Verification → Set Valid Flag → System Reset → Jump to Application  

---

##  Bootloader Build Instructions
1. Open STM32CubeIDE
2. Import the Bootloader project
3. Select the correct STM32 board configuration
4. Verify flash memory settings and linker configuration
5. Build the project (Ctrl + B)
6. Flash the bootloader using ST-Link debugger
7. Open serial terminal to monitor UART logs

---

##  Application Firmware Configuration
The application firmware must be compiled with a custom linker script.

Set the application start address to:
0x08010000

This ensures:
- Bootloader and application do not overlap in flash
- Safe memory partitioning
- Correct vector table relocation during boot

---

## 📷 Hardware Setup

![Hardware](docs/hardware(application).jpg)
![Hardware](docs/hardware(boot).jpg)

##  Flash Memory Layout Verification

### Bootloader @ 0x08000000
![Bootloader Flash](docs/Flash_bootloader.png)

### Application @ 0x08010000
![Application Flash](docs/Flash_application.png)

##  Firmware Upload Tool (Python Script)
A Python script is provided to send the compiled firmware (.bin) file via UART.

## Install Dependencies
```bash
pip install pyserial
```
python firmware_sender.py firmware.bin /dev/ttyUSB0

##  CRC Integrity Verification

- CRC32 is calculated after firmware is written to flash memory  
- Ensures firmware integrity before execution  
- Prevents execution of corrupted or incomplete firmware  
- Improves system reliability and robustness  

> Note: CRC provides integrity verification only. Cryptographic signatures (RSA/ECDSA) would be required for full secure boot authentication.

---

##  Failure Handling & Safety Behavior

- If CRC validation fails → Bootloader remains in update mode  
- If firmware validity flag is not set → Application is not executed  
- Prevents jumping to corrupted firmware images  
- Ensures safe and deterministic boot behavior  

(Current version uses a single application slot without rollback mechanism.)

---

##  Testing & Validation

- Successfully tested on real STM32 hardware  
- Verified UART-based firmware update process  
- Stable flash erase and programming operations  
- Correct CRC validation before application jump  
- Serial debugging logs used to trace boot sequence  

*(Add UART log screenshot here for visual proof)*

---

---

##  Key Learning Outcomes

- Bootloader architecture design  
- Flash memory partitioning & management  
- Embedded firmware update mechanisms  
- CRC-based firmware integrity validation  
- UART communication protocol design  
- Safe application jumping and boot flow control  
- Real-world embedded system reliability concepts  

---

##  Current Limitations

- No dual-slot firmware rollback (single-slot architecture)  
- No cryptographic signature verification (CRC only)  
- UART-only firmware update interface  
- No OTA or CAN-based update support  

---

##  Future Improvements

- Dual-bank firmware rollback mechanism (A/B slots)  
- Secure boot with digital signature (RSA/ECDSA)  
- CAN bus firmware update (automotive use-case)  
- Encrypted firmware transmission  
- External flash support (QSPI / NOR Flash)  
- OTA update via Embedded Linux gateway  

---

##  Author

**Farhan Mohammad Shaikh**  
M.Sc. Microelectronics & Embedded Systems – TU Hamburg  
Embedded Firmware | RTOS | Embedded Linux | Low-Level Drivers  

GitHub: https://github.com/Farhan-mohammad-shaikh
