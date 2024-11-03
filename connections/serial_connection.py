import serial

from connections.base_connection import ConnectionHandler


class SerialConnection(ConnectionHandler):
    def __init__(self, port, baudrate=9600, timeout=1):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def connect(self):
        try:
            self.serial = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=self.timeout
            )
            self.connected = True
            self.output_received.emit(
                f"Connected to {self.port} at {self.baudrate} baud"
            )
        except serial.SerialException as e:
            self.output_received.emit(f"Connection failed: {str(e)}")
            raise

    def disconnect(self):
        if self.serial:
            self.serial.close()
        self.connected = False
        self.connection_closed.emit()

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write((command + "\n").encode())
                response = self.serial.readline().decode().strip()
                self.output_received.emit(response)
            except serial.SerialException as e:
                self.output_received.emit(f"Error sending command: {str(e)}")
                self.connected = False
