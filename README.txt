LastKings Liquor Store - POS System
===================================

SETUP INSTRUCTIONS
------------------

1. Install Python 3.8 or higher

2. Install required packages:
   pip install -r requirements.txt

3. Add sample products to database:
   python sample_products.py

4. Run the POS system:
   python pos_system.py


HARDWARE REQUIREMENTS
---------------------

1. BARCODE SCANNER
   - USB barcode scanner (works as keyboard input device)
   - Most USB scanners are plug-and-play
   - No special configuration needed

2. RECEIPT PRINTER
   - ESC/POS compatible thermal printer
   - Connect via USB or Serial port
   - Set as default printer in Windows
   - Recommended: Epson TM-T20, Star TSP143, or similar

3. CASH DRAWER
   - Can be connected to:
     * Receipt printer's RJ11/RJ12 cash drawer port (recommended)
     * Direct serial/COM port connection
   - Automatically opens after each sale


SYSTEM FEATURES
---------------

✓ Barcode scanning integration
✓ Real-time inventory tracking
✓ Automatic receipt printing
✓ Cash drawer control
✓ Low stock alerts
✓ Sales transaction logging
✓ Easy-to-use GUI interface


USER GUIDE
----------

1. SCANNING ITEMS:
   - Scan product barcode with scanner
   - Or manually type barcode and press Enter
   - Item appears in shopping cart

2. COMPLETING SALE:
   - Review items in cart
   - Enter cash received amount
   - System calculates change automatically
   - Click "Complete Sale"
   - Receipt prints automatically
   - Cash drawer opens

3. MANAGING CART:
   - Select item and click "Remove Item" to delete
   - Click "Clear Cart" to start over

4. LOW STOCK ALERTS:
   - Alerts appear in the Alerts panel after each sale
   - Check inventory regularly


DATABASE
--------
- Stored in: lastkings_pos.db (SQLite)
- Automatically created on first run
- Contains: products, sales, sale_items tables


TROUBLESHOOTING
---------------

* Barcode scanner not working?
  - Check USB connection
  - Test scanner in notepad - it should type the barcode
  - Ensure cursor is in the barcode entry field

* Printer not working?
  - Check printer is set as default in Windows
  - Verify printer is connected and powered on
  - Run printer test: python -c "from receipt_printer import ReceiptPrinter; ReceiptPrinter().print_test_receipt()"

* Cash drawer not opening?
  - Ensure drawer is connected to printer's cash drawer port
  - Check cable connection (RJ11/RJ12)
  - Verify cash_drawer_port=True in receipt_printer.py

* Product not found?
  - Run sample_products.py to add products
  - Or manually add products to database


SUPPORT
-------
For issues or questions, contact your system administrator.


LastKings Liquor Store POS System v1.0
Developed 2025