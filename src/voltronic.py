import serial


def device_mode(letter):
    device_modes = {
        "P": "Power On Mode",
        "S": "Standby Mode",
        "L": "Line Mode",
        "B": "Battery Mode",
        "F": "Fault Mode",
        "H": "Power Saving Mode",
    }
    return device_modes.get(letter, "Unknown")


class Sensors:

    def unpack_data(self, query, data):
        try:
            data = data.decode().split(" ")
            print("👉data", data)

            if query == 'QMOD':
                self.mode = chr(data[0])
            elif query == 'QPIGS':
                self.grid_voltage = float(data[0])
                self.grid_frequency = float(data[1])
                self.output_load_watt = int(data[5])
                self.battery_capacity = int(data[10])
                self.heatsink_temperature = int(data[11])
                self.pv_input_current = int(data[12])
                self.scc_voltage = int(data[14])
                self.pv_input_watts = int(self.scc_voltage*self.pv_input_current)
            elif query == 'QPIRI':
                self.grid_voltage = float(data[0])
                self.output_load_watt = int(data[6])
            elif query == 'QPIWS':
                self.warnings = str(data[0])
            else:
                print(f"Unknown query: {query}, response: {str(data[0])}")

        except Exception as e:
            print(f"Error unpacking data: {e}, query: {query}, data: {data}")

    def print(self):
        for sensor in self.__dict__:
            print(f"{sensor}: {self.__dict__[sensor]}")


class Voltronic:
    def __init__(self, config):
        self.sensors = Sensors()
        self.port = serial.Serial(config['SERIAL_PORT'], 2400, timeout=0.5)

        self.port.open()
        self.port.reset_input_buffer()

    def get(self, query):
        response = self.require(query)

        is_valid, errors = self.check_response_valid(response)
        if not is_valid:
            print("errors", errors)
            return
        self.sensors.unpack_data(query, response[0])

    def require(self, query):
        self.port.reset_input_buffer()
        query_bytes = self._query_to_bytes(query)
        self.port.write(query_bytes)
        response = self.port.readlines(None)
        return response

    def _query_to_bytes(self, query):
        command_bytes = bytearray(query.encode())
        crc_high, crc_low = crc(command_bytes)
        ba = bytearray([crc_high, crc_low, 13])
        command_bytes.extend(ba)
        return command_bytes

    def check_response_valid(self, response):
        if response is None:
            return False, {"validity check": ["Error: Response was empty", ""]}
        if type(response) is dict:
            response["validity check"] = ["Error: incorrect response format", ""]
            return False, response
        if len(response) <= 3:
            return False, {"validity check": ["Error: Response to short", ""]}

        if type(response) is str:
            if "(NAK" in response:
                return False, {"validity check": ["Error: NAK", ""]}
            crc_high, crc_low = crc(response[:-3])
            if [ord(response[-3]), ord(response[-2])] != [crc_high, crc_low]:
                return False, {"validity check": ["Error: Invalid response CRCs", ""]}
        elif type(response) is bytes:
            if b"(NAK" in response:
                return False, {"validity check": ["Error: NAK", ""]}

            crc_high, crc_low = crc(response[:-3])
            if response[-3:-1] != bytes([crc_high, crc_low]):
                return False, {"validity check": ["Error: Invalid response CRCs", ""]}

        return True, {}


def crc(data_bytes):
    """
    Calculates CRC for supplied data_bytes
    """
    crc = 0
    da = 0
    crc_ta = [
        0x0000,
        0x1021,
        0x2042,
        0x3063,
        0x4084,
        0x50A5,
        0x60C6,
        0x70E7,
        0x8108,
        0x9129,
        0xA14A,
        0xB16B,
        0xC18C,
        0xD1AD,
        0xE1CE,
        0xF1EF,
    ]

    for c in data_bytes:
        if type(c) == str:
            c = ord(c)
        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c >> 4)
        crc ^= crc_ta[index]

        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c & 0x0F)
        crc ^= crc_ta[index]

    crc_low = crc & 0xFF
    crc_high = (crc >> 8) & 0xFF

    if crc_low == 0x28 or crc_low == 0x0D or crc_low == 0x0A or crc_low == 0x00:
        crc_low += 1
    if crc_high == 0x28 or crc_high == 0x0D or crc_high == 0x0A or crc_high == 0x00:
        crc_high += 1

    crc = crc_high << 8
    crc += crc_low
    return [crc_high, crc_low]
