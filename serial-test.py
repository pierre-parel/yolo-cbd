import serial
import time
# import serial.tools.list_ports as port_list
# ports = list(port_list.comports())
# for p in ports:
#     print(p)

arduino = serial.Serial(port="COM6", timeout=.1)

def write_read(x):
    num_bytes_written = arduino.write(bytes(x, 'utf-8'))
    print(f"Number of bytes written: {num_bytes_written}")
    time.sleep(0.05)
    data = arduino.readline()
    return data

def read_serial():
    data = arduino.readline()
    return data

while True:
    print(read_serial())
    if read_serial() == b'1\r\n':
        print("No beans")
    else:
        print("Bean detected")
        num = input("Enter a number: ")
        value = write_read(num)
        print(value)