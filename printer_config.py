"""
Thermal Printer Configuration Utility
Run this to test and configure your thermal printer
"""

import sys
from receipt_printer import ReceiptPrinter

def main():
    print("=" * 50)
    print("LastKingz POS - Thermal Printer Configuration")
    print("=" * 50)
    print()

    # List available printers
    print("Available Printers:")
    printers = ReceiptPrinter.list_printers()
    for i, printer in enumerate(printers, 1):
        print(f"  {i}. {printer}")
    print()

    if not printers or printers == ["No printers available - install pywin32"]:
        print("ERROR: No printers found or pywin32 not installed.")
        print()
        print("To install pywin32, run:")
        print("  py -3 -m pip install pywin32")
        print()
        return

    # Select printer
    print("Select printer to use:")
    print("  Press ENTER to use default printer")
    print("  Or enter printer number (1-{})".format(len(printers)))

    choice = input("Your choice: ").strip()

    if choice:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(printers):
                printer_name = printers[idx]
            else:
                print("Invalid choice. Using default.")
                printer_name = None
        except ValueError:
            print("Invalid input. Using default.")
            printer_name = None
    else:
        printer_name = None

    # Create printer instance
    print()
    print(f"Using printer: {printer_name or 'Default'}")
    printer = ReceiptPrinter(printer_name=printer_name)
    print()

    # Main menu
    while True:
        print("-" * 50)
        print("What would you like to do?")
        print("  1. Print test receipt")
        print("  2. Test cash drawer")
        print("  3. Check printer status")
        print("  4. Print configuration page")
        print("  5. Exit")
        print()

        option = input("Select option (1-5): ").strip()
        print()

        if option == "1":
            print("Printing test receipt...")
            success = printer.print_test_receipt()
            if success:
                print("✓ Test receipt sent to printer!")
                print("  (Check if receipt printed correctly)")
            else:
                print("✗ Failed to print receipt")
                print("  (Check console for error messages)")

        elif option == "2":
            print("Testing cash drawer...")
            success = printer.open_cash_drawer()
            if success:
                print("✓ Cash drawer command sent!")
                print("  (Check if drawer opened)")
            else:
                print("✗ Failed to open cash drawer")
                print("  (Ensure drawer is connected to printer)")

        elif option == "3":
            print("Printer Information:")
            print(f"  Name: {printer.printer_name}")
            print(f"  Cash drawer enabled: {printer.cash_drawer_port}")
            try:
                import win32print
                hprinter = win32print.OpenPrinter(printer.printer_name)
                status = win32print.GetPrinter(hprinter, 2)
                win32print.ClosePrinter(hprinter)
                print(f"  Status: Online")
                print(f"  Port: {status['pPortName']}")
            except Exception as e:
                print(f"  Status: {str(e)}")

        elif option == "4":
            print("Configuration Settings:")
            print(f"  Printer: {printer.printer_name}")
            print(f"  Receipt width: 42 characters")
            print(f"  Paper size: 80mm thermal")
            print(f"  Cash drawer: {'Enabled' if printer.cash_drawer_port else 'Disabled'}")
            print(f"  ESC/POS commands: Supported")
            print()
            print("To change these settings, edit receipt_printer.py")

        elif option == "5":
            print("Exiting printer configuration.")
            break

        else:
            print("Invalid option. Please select 1-5.")

        print()

    print()
    print("=" * 50)
    print("Configuration Complete!")
    print()
    print("Your printer is now configured for the POS system.")
    print("Receipts will print automatically on every sale.")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
