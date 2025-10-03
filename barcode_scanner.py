class BarcodeScanner:
    """
    Interface for barcode scanner integration.
    Most USB barcode scanners work as keyboard input devices.
    They scan and automatically "type" the barcode followed by Enter.
    """

    def __init__(self):
        self.scan_buffer = ""

    def process_input(self, key_input: str) -> str:
        """
        Process keyboard input from barcode scanner.
        Returns barcode when Enter is detected, otherwise empty string.
        """
        if key_input == '\r' or key_input == '\n':
            # Enter key detected - return complete barcode
            barcode = self.scan_buffer
            self.scan_buffer = ""
            return barcode
        else:
            # Accumulate characters
            self.scan_buffer += key_input
            return ""

    def clear_buffer(self):
        """Clear the scan buffer"""
        self.scan_buffer = ""

    @staticmethod
    def validate_barcode(barcode: str) -> bool:
        """Basic barcode validation"""
        # Most liquor barcodes are UPC-A (12 digits) or EAN-13 (13 digits)
        return barcode.isdigit() and len(barcode) in [12, 13]