from datetime import datetime
from typing import List, Dict
try:
    import win32print
except ImportError:
    win32print = None

class ReceiptPrinter:
    """
    Receipt printer using ESC/POS commands.
    Compatible with most thermal receipt printers.
    """

    def __init__(self, printer_name: str = None, cash_drawer_port: bool = True):
        """
        Initialize receipt printer.

        Args:
            printer_name: Name of printer, None for default
            cash_drawer_port: True if cash drawer is connected to printer
        """
        if win32print:
            self.printer_name = printer_name or win32print.GetDefaultPrinter()
        else:
            self.printer_name = printer_name or "Default"
        self.cash_drawer_port = cash_drawer_port

        # ESC/POS commands
        self.ESC = b'\x1B'
        self.GS = b'\x1D'
        self.INIT = b'\x1B\x40'  # Initialize printer
        self.BOLD_ON = b'\x1B\x45\x01'
        self.BOLD_OFF = b'\x1B\x45\x00'
        self.CENTER = b'\x1B\x61\x01'
        self.LEFT = b'\x1B\x61\x00'
        self.CUT = b'\x1D\x56\x00'  # Cut paper
        self.OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'  # Open cash drawer

    @staticmethod
    def list_printers():
        """List all available printers"""
        if not win32print:
            return ["No printers available - install pywin32"]
        printers = []
        try:
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
                printers.append(printer[2])
        except:
            pass
        return printers if printers else ["Default Printer"]

    def print_receipt(self, sale_data: Dict, items: List[Dict]):
        """
        Print receipt for a sale.

        Args:
            sale_data: Dict with 'total', 'cash_received', 'change', 'date'
            items: List of items with 'name', 'quantity', 'price', 'subtotal'
        """
        receipt_text = self._format_receipt(sale_data, items)
        self._send_to_printer(receipt_text)

    def _format_receipt(self, sale_data: Dict, items: List[Dict]) -> str:
        """Format receipt as text"""
        receipt = []
        width = 42  # Standard receipt width in characters

        # Header
        receipt.append("=" * width)
        receipt.append("LastKingz Liquor Store".center(width))
        receipt.append("=" * width)
        receipt.append("")

        # Date and time
        sale_date = sale_data.get('date', datetime.now())
        if isinstance(sale_date, str):
            date_str = sale_date
        else:
            date_str = sale_date.strftime("%Y-%m-%d %H:%M:%S")
        receipt.append(f"Date: {date_str}")
        receipt.append("-" * width)
        receipt.append("")

        # Items
        receipt.append("ITEM                    QTY   PRICE   TOTAL")
        receipt.append("-" * width)

        for item in items:
            name = item['name'][:20].ljust(20)
            qty = str(item['quantity']).rjust(5)
            price = f"${item['price']:.2f}".rjust(7)
            subtotal = f"${item['subtotal']:.2f}".rjust(8)
            receipt.append(f"{name} {qty} {price} {subtotal}")

        receipt.append("-" * width)
        receipt.append("")

        # Totals
        total = sale_data.get('total', 0)
        cash = sale_data.get('cash_received', 0)
        change = sale_data.get('change', 0)

        receipt.append(f"{'TOTAL:'.ljust(30)} ${total:.2f}".rjust(width))
        receipt.append(f"{'CASH:'.ljust(30)} ${cash:.2f}".rjust(width))
        receipt.append(f"{'CHANGE:'.ljust(30)} ${change:.2f}".rjust(width))
        receipt.append("")
        receipt.append("=" * width)
        receipt.append("")

        # Footer
        receipt.append("Thank you for your business!".center(width))
        receipt.append("Please drink responsibly.".center(width))
        receipt.append("")
        receipt.append("=" * width)
        receipt.append("")
        receipt.append("")

        return "\n".join(receipt)

    def _send_to_printer(self, text: str):
        """Send formatted text to printer"""
        # Fallback: Save to file if printer not available
        if not win32print:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"receipt_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Receipt saved to {filename} (printer module not available)")
                return True
            except Exception as e:
                print(f"Error saving receipt: {str(e)}")
                return False

        try:
            # Open printer
            hprinter = win32print.OpenPrinter(self.printer_name)

            try:
                # Start print job
                job_id = win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
                win32print.StartPagePrinter(hprinter)

                # Send text
                win32print.WritePrinter(hprinter, text.encode('utf-8'))

                # Open cash drawer if connected
                if self.cash_drawer_port:
                    win32print.WritePrinter(hprinter, self.OPEN_DRAWER)

                # Cut paper
                win32print.WritePrinter(hprinter, self.CUT)

                # End print job
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)

            finally:
                win32print.ClosePrinter(hprinter)

            return True

        except Exception as e:
            # Fallback to file
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"receipt_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Print error: {str(e)}. Receipt saved to {filename}")
                return True
            except:
                print(f"Print error: {str(e)}")
                return False

    def print_test_receipt(self):
        """Print a test receipt"""
        test_data = {
            'total': 45.97,
            'cash_received': 50.00,
            'change': 4.03,
            'date': datetime.now()
        }

        test_items = [
            {'name': 'Jack Daniels 750ml', 'quantity': 1, 'price': 24.99, 'subtotal': 24.99},
            {'name': 'Budweiser 12pk', 'quantity': 1, 'price': 14.99, 'subtotal': 14.99},
            {'name': 'Marlboro Red', 'quantity': 1, 'price': 5.99, 'subtotal': 5.99}
        ]

        return self.print_receipt(test_data, test_items)

    def open_cash_drawer(self):
        """Manually open cash drawer without printing"""
        if not win32print:
            print("Cash drawer command sent (simulation mode)")
            return True

        if self.cash_drawer_port:
            try:
                hprinter = win32print.OpenPrinter(self.printer_name)
                try:
                    job_id = win32print.StartDocPrinter(hprinter, 1, ("Open Drawer", None, "RAW"))
                    win32print.StartPagePrinter(hprinter)
                    win32print.WritePrinter(hprinter, self.OPEN_DRAWER)
                    win32print.EndPagePrinter(hprinter)
                    win32print.EndDocPrinter(hprinter)
                finally:
                    win32print.ClosePrinter(hprinter)
                return True
            except Exception as e:
                print(f"Error opening drawer: {str(e)}")
                return False
        return False