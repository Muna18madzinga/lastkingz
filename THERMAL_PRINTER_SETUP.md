# Thermal Printer Setup Guide for LastKingz POS

This guide will help you set up your thermal receipt printer with the LastKingz POS system.

## Supported Printers

The system supports most thermal receipt printers that use ESC/POS protocol, including:
- Epson TM series (TM-T20, TM-T88, TM-U220, etc.)
- Star Micronics TSP series
- Bixolon SRP series
- Generic 58mm and 80mm thermal printers
- POS-80, POS-58 models

## Step 1: Install Printer Drivers

### For USB Thermal Printers:

1. **Download the driver** from your printer manufacturer:
   - **Epson TM printers**: https://epson.com/Support/Point-of-Sale/
   - **Star Micronics**: https://www.starmicronics.com/support/
   - **Generic printers**: Usually come with a driver CD or download link

2. **Install the driver**:
   - Run the installer as Administrator
   - Follow the installation wizard
   - Connect your printer when prompted
   - Wait for Windows to recognize the device

3. **Set as default printer** (recommended):
   - Open **Settings** → **Devices** → **Printers & scanners**
   - Click on your thermal printer
   - Click **Manage** → **Set as default**

### For Network Thermal Printers:

1. **Get the printer's IP address**:
   - Print a network configuration page (usually by holding the feed button)
   - Note the IP address (e.g., 192.168.1.100)

2. **Add network printer**:
   - Open **Settings** → **Devices** → **Printers & scanners**
   - Click **Add a printer or scanner**
   - Click **The printer that I want isn't listed**
   - Select **Add a printer using a TCP/IP address or hostname**
   - Enter the IP address
   - Select the appropriate driver

### For Serial (COM Port) Printers:

1. **Install USB-to-Serial adapter driver** (if using adapter)
2. **Note the COM port** (e.g., COM3):
   - Right-click **Start** → **Device Manager**
   - Expand **Ports (COM & LPT)**
   - Note the COM port number

## Step 2: Test the Printer

### Method 1: Windows Test Page

1. Go to **Settings** → **Devices** → **Printers & scanners**
2. Click your thermal printer → **Manage**
3. Click **Print a test page**
4. Verify the printer prints correctly

### Method 2: POS System Test

Run this command in the POS directory:

```bash
py -3 -c "from receipt_printer import ReceiptPrinter; printer = ReceiptPrinter(); printer.print_test_receipt()"
```

If successful, you'll see a test receipt print!

## Step 3: Configure Cash Drawer

Most thermal printers have a cash drawer port (RJ11/RJ12 connector on the back).

### Connect the Cash Drawer:

1. **Locate the cash drawer port** on your printer (usually labeled "DK" or "Drawer")
2. **Connect the cash drawer cable** to this port
3. **The drawer should pop open** when a receipt prints

### Test Cash Drawer:

```bash
py -3 -c "from receipt_printer import ReceiptPrinter; printer = ReceiptPrinter(); printer.open_cash_drawer()"
```

## Step 4: Configure POS System

The POS system auto-detects your default printer. To use a specific printer:

1. Open `receipt_printer.py`
2. Find line 23: `self.printer_name = printer_name or win32print.GetDefaultPrinter()`
3. Change to: `self.printer_name = printer_name or "YOUR_PRINTER_NAME"`

## Common Issues & Solutions

### Issue 1: "No printer found" or receipts save to .txt files

**Solution:**
- Ensure pywin32 is installed: `py -3 -m pip install pywin32`
- Check printer is set as default in Windows
- Verify printer is online and has paper

### Issue 2: Receipt prints but text is garbled

**Solution:**
- Check printer driver is correctly installed
- Verify paper width (58mm or 80mm)
- Try updating `receipt_printer.py` width setting (line 66)

### Issue 3: Cash drawer doesn't open

**Solution:**
- Verify drawer is connected to printer's drawer port (not computer USB)
- Check drawer cable is fully inserted
- Some drawers require specific voltage - check printer manual
- Test with: `ReceiptPrinter().open_cash_drawer()`

### Issue 4: Printer cuts paper before printing complete

**Solution:**
- This is a driver issue
- Open printer properties → Preferences
- Adjust paper size and margins
- Disable "Fast print" mode

### Issue 5: Network printer not responding

**Solution:**
- Ping the printer: `ping 192.168.1.100`
- Check firewall isn't blocking port 9100
- Verify printer is on same network
- Try assigning a static IP to printer

## Printer Settings Recommendations

For best results, configure your printer with these settings:

### In Windows Printer Properties:
- **Paper Size**: Custom - Width: 80mm (or 58mm), Length: Continuous
- **Print Quality**: Draft or Fast
- **Paper Type**: Receipt Paper
- **Cutting**: After print

### In Printer Driver Advanced Settings:
- **Speed**: High speed
- **Density**: Medium
- **Character Set**: PC437 or PC850
- **Code Page**: CP437 (USA, Standard Europe)

## Supported Printer Models (Tested)

✅ **Working Models:**
- Epson TM-T20II
- Epson TM-T88V
- Star TSP143III
- Bixolon SRP-350III
- Generic POS-80 series
- Generic POS-58 series

⚠️ **Partial Support:**
- Older Star SP500 series (may need firmware update)
- Some Chinese generic brands (may need specific drivers)

## Advanced Configuration

### Using a Specific Printer Port:

Edit `receipt_printer.py` and modify the `__init__` method:

```python
def __init__(self, printer_name: str = "Epson TM-T20II", cash_drawer_port: bool = True):
    self.printer_name = printer_name
    self.cash_drawer_port = cash_drawer_port
```

### Network Printer Configuration:

For network printers, you may need to install the printer using its IP:

```python
# In receipt_printer.py, add:
import socket

def print_to_network_printer(self, text, ip_address, port=9100):
    """Print to network printer via raw TCP/IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip_address, port))
        sock.send(text.encode('utf-8'))
        sock.send(self.OPEN_DRAWER)  # Open cash drawer
        sock.send(self.CUT)  # Cut paper
        sock.close()
        return True
    except Exception as e:
        print(f"Network print error: {e}")
        return False
```

## Getting Help

If you're still having issues:

1. **Check printer is working**: Print a test page from Windows
2. **Verify driver installation**: Check Device Manager for errors
3. **Review the logs**: Check the Flask console for error messages
4. **Test with the test script**: Run the test receipt command above

## Automatic Printing Behavior

The POS system automatically:
- ✅ Prints a receipt after every completed sale
- ✅ Opens the cash drawer when receipt prints
- ✅ Falls back to saving .txt files if no printer detected
- ✅ Includes all sale items, totals, and change

## Manual Printer Selection

To manually select a printer when the app starts, you can list available printers:

```bash
py -3 -c "from receipt_printer import ReceiptPrinter; print(ReceiptPrinter.list_printers())"
```

This will show all installed printers.

## Next Steps

Once your printer is configured:
1. Complete a test sale in the POS
2. Verify the receipt prints correctly
3. Verify the cash drawer opens
4. Adjust receipt width in code if needed (58mm vs 80mm)

---

For technical support, check the printer manufacturer's documentation or contact their support team.
