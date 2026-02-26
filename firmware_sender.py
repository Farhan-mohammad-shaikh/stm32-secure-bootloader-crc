import serial
import struct
import time
import sys
import zlib

PORT = '/dev/ttyACM0'
BAUD = 115200
BIN_FILE = '/home/farhan/test_project/Bootloader_project/application/Debug/application.bin'

try:
    print("Opening serial port...")
    ser = serial.Serial(PORT, BAUD, timeout=2)
except Exception as e:
    print("Failed to open serial:", e)
    sys.exit(1)

time.sleep(2)

# Clear any old data
ser.reset_input_buffer()
ser.reset_output_buffer()

print("Sending START...")
ser.write(b'START\n')

print("Waiting for bootloader response...")

# Wait until bootloader says READY
while True:
    line = ser.readline()
    if not line:
        continue

    decoded = line.decode(errors='ignore').strip()
    print("BOOT:", decoded)

    if "READY FOR FIRMWARE" in decoded:
        break

# Load firmware file
try:
    with open(BIN_FILE, 'rb') as f:
        firmware = f.read()
except Exception as e:
    print("Failed to open bin file:", e)
    ser.close()
    sys.exit(1)

size = len(firmware)
print("Firmware size:", size, "bytes")

# Send firmware size (little-endian 32-bit)
MAGIC = 0xDEADBEEF
VERSION = 1

crc = zlib.crc32(firmware) & 0xFFFFFFFF

header = struct.pack('<IIII',
                     MAGIC,
                     VERSION,
                     size,
                     crc)

ser.write(header)
time.sleep(0.1)

# Send firmware in chunks (more stable than sending all at once)
chunk_size = 256
sent = 0

while sent < size:
    chunk = firmware[sent:sent+chunk_size]
    ser.write(chunk)
    sent += len(chunk)
    print(f"Sent {sent}/{size} bytes")

print("Firmware sent successfully.")

# Optional: read final bootloader messages
time.sleep(1)
while ser.in_waiting:
    line = ser.readline()
    print("BOOT:", line.decode(errors='ignore').strip())

ser.close()
print("Done.")
