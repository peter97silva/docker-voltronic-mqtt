import serial
import os

SERIAL_PORT = os.getenv('SERIAL_PORT')


class SerialPort:
    def __init__(self):
        self.port = serial.Serial(SERIAL_PORT, 2400, timeout=0.5)
        self.port.reset_input_buffer()

    def write(self, query_bytes):
        self.port.reset_input_buffer()
        self.port.write(query_bytes)

    def read(self):
        response = self.port.readlines(None)
        return response


# tests
class MockSerialPort:

    def __init__(self):
        self.query_bytes = None

    def write(self, query_bytes):
        self.query_bytes = query_bytes

    def read(self):
        print(self.query_bytes)

        if self.query_bytes == b'QMODI\xc1\r':
            return b"(S\x64\x39\r"

        if self.query_bytes == b'QPIGS\xb7\xa9\r':
            return b"(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010\x24\x8C\r"

        if self.query_bytes == b'QPIRI\xf8T\r':
            return b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1 60\x83\xAA\r"

        if self.query_bytes == b'QPIWS\xb4\xda\r':
            return b"(00000100000000001000000000000000\x56\xA6\r"

        return b'Default response'
