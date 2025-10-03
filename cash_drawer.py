import serial
import serial.tools.list_ports

class CashDrawer:
    """
    Cash drawer controller.
    Most cash drawers connect via:
    1. Serial/COM port (RJ11/RJ12 connector)
    2. USB to Serial adapter
    3. Through receipt printer's cash drawer port
    """

    # Standard ESC/POS command to open cash drawer
    OPEN_DRAWER_CMD = b'\x1B\x70\x00\x19\xFA'  # ESC p 0 25 250

    def __init__(self, port: str = None, method: str = 'serial'):
        """
        Initialize cash drawer.

        Args:
            port: COM port (e.g., 'COM1', 'COM3') or None for auto-detect
            method: 'serial' for direct connection, 'printer' if connected through printer
        """
        self.port = port
        self.method = method
        self.serial_connection = None

    @staticmethod
    def list_available_ports():
        """List all available COM ports"""
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]

    def connect(self, port: str = None):
        """Connect to cash drawer via serial port"""
        if port:
            self.port = port

        if not self.port:
            # Try to auto-detect
            ports = self.list_available_ports()
            if ports:
                self.port = ports[0][0]
            else:
                raise Exception("No COM ports found. Please specify port manually.")

        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            return True
        except serial.SerialException as e:
            raise Exception(f"Failed to connect to cash drawer on {self.port}: {str(e)}")

    def open_drawer(self) -> bool:
        """
        Open the cash drawer.
        Returns True if command sent successfully.
        """
        if self.method == 'serial':
            return self._open_via_serial()
        elif self.method == 'printer':
            return self._open_via_printer()
        else:
            return self._open_via_network()

    def _open_via_serial(self) -> bool:
        """Open drawer via direct serial connection"""
        try:
            if not self.serial_connection or not self.serial_connection.is_open:
                self.connect()

            self.serial_connection.write(self.OPEN_DRAWER_CMD)
            self.serial_connection.flush()
            return True
        except Exception as e:
            print(f"Error opening cash drawer: {str(e)}")
            return False

    def _open_via_printer(self) -> bool:
        """
        Open drawer via printer connection.
        This is handled by the receipt printer module.
        """
        # This will be called from receipt_printer.py
        return True

    def _open_via_network(self) -> bool:
        """Open drawer via network printer"""
        # For network printers with cash drawer ports
        return True

    def close_connection(self):
        """Close serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

    def __del__(self):
        """Cleanup on deletion"""
        self.close_connection()