"""
Test receipt printing functionality
"""

from receipt_printer import ReceiptPrinter
from datetime import datetime

def test_receipt():
    printer = ReceiptPrinter()

    print("=" * 60)
    print("Testing Receipt Printing")
    print("=" * 60)

    # Test sale data
    sale_data = {
        'total': 45.97,
        'cash_received': 50.00,
        'change': 4.03,
        'date': datetime.now()
    }

    # Test items
    items = [
        {'name': 'Jack Daniels 750ml', 'quantity': 1, 'price': 24.99, 'subtotal': 24.99},
        {'name': 'Budweiser 12pk', 'quantity': 1, 'price': 14.99, 'subtotal': 14.99},
        {'name': 'Marlboro Red', 'quantity': 1, 'price': 5.99, 'subtotal': 5.99}
    ]

    print("\nPrinting test receipt...")
    success = printer.print_receipt(sale_data, items)

    if success:
        print("\n[SUCCESS] Receipt printed/saved successfully!")
        print("\nIf no printer is connected, check for receipt_*.txt file")
        print("in the current directory.")
    else:
        print("\n[FAIL] Receipt printing failed")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_receipt()
    input("\nPress Enter to exit...")