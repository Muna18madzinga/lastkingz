# LastKings Liquor Store - POS System User Guide

## Quick Start

### Installation (Windows)

1. **Run Setup**
   ```
   Double-click: setup.bat
   ```
   This will:
   - Install required Python packages
   - Create database
   - Add sample products

2. **Start POS System**
   ```
   Double-click: run.bat
   ```
   Or manually run: `python pos_system.py`

---

## Main POS Interface

### Making a Sale

1. **Scan Products**
   - Use barcode scanner to scan product barcodes
   - OR manually type barcode and press Enter
   - Product automatically adds to cart

2. **Review Cart**
   - View all scanned items in the cart table
   - Check quantities and prices
   - Remove items if needed (select item → click "Remove Item")

3. **Process Payment**
   - Enter cash amount received from customer
   - System calculates change automatically
   - Click "Complete Sale"

4. **Complete Transaction**
   - Receipt prints automatically
   - Cash drawer opens
   - Give customer receipt and change
   - Cart clears for next customer

### Keyboard Shortcuts
- **Enter** - Scan/add barcode to cart
- Works seamlessly with USB barcode scanners

---

## Product Management

### Access: Menu → Products → Manage Products

### Add New Product
1. Click "Add Product"
2. Fill in details:
   - **Barcode** - Product barcode (12-13 digits)
   - **Product Name** - Full product name
   - **Price** - Selling price in dollars
   - **Stock Quantity** - Number of units in stock
   - **Low Stock Alert** - Alert when stock falls below this number
3. Click "Save"

### Edit Product
1. Double-click product in table OR select and click "Edit Product"
2. Update details
3. Click "Save"

### Delete Product
1. Select product
2. Click "Delete Product"
3. Confirm deletion

### Tips
- Products with low stock are highlighted in red
- Cannot change barcode after product is created
- Price changes apply to future sales only

---

## Sales Reports

### Access: Menu → Sales → View Sales Reports

### Available Reports
- **Today** - Today's sales
- **Yesterday** - Previous day
- **This Week** - Current week (Monday-Today)
- **This Month** - Current month
- **All Time** - Complete history

### Report Information
- Total number of sales
- Total revenue
- Average sale amount
- Cash collected
- Change given
- Individual transaction list

### View Transaction Details
- Double-click any sale to see items purchased

---

## Inventory Management

### Check Inventory Status
Menu → Products → View Inventory Report

Shows:
- Total products in system
- Number of low stock items
- Out of stock items
- Total inventory value
- List of items needing restock

### Automatic Features
- Stock decreases automatically after each sale
- Low stock alerts appear after transactions
- Out-of-stock items cannot be sold

---

## Hardware Setup

### Barcode Scanner
- **Type**: USB barcode scanner (keyboard wedge)
- **Setup**: Plug in USB → automatic driver installation
- **Test**: Open Notepad → scan barcode → should type numbers
- **No Configuration Required**

### Receipt Printer
- **Type**: ESC/POS thermal printer (58mm or 80mm)
- **Recommended Models**:
  - Epson TM-T20II
  - Star TSP143
  - Any ESC/POS compatible printer

- **Setup**:
  1. Install printer drivers
  2. Set as default printer in Windows
  3. Connect USB cable
  4. Test print from Windows

- **Fallback**: If printer unavailable, receipts save as text files

### Cash Drawer
- **Connection**:
  - Option 1: Printer's RJ11/RJ12 cash drawer port (recommended)
  - Option 2: Direct serial/COM port connection

- **Setup**:
  1. Connect drawer cable to printer
  2. Drawer opens automatically after each sale
  3. No additional configuration needed

---

## Troubleshooting

### Barcode Scanner Issues
**Problem**: Scanner not working
- ✓ Check USB connection
- ✓ Test in Notepad (should type numbers)
- ✓ Make sure cursor is in barcode field
- ✓ Check scanner is in numeric mode (not QR mode)

**Problem**: Wrong numbers scanned
- ✓ Clean scanner lens
- ✓ Check barcode is not damaged
- ✓ Ensure good lighting

### Printer Issues
**Problem**: Receipt not printing
- ✓ Check printer power and USB connection
- ✓ Check paper loaded correctly
- ✓ Verify printer set as default in Windows
- ✓ Check for paper jam
- ✓ Receipts will save as text files if printer fails

**Problem**: Poor print quality
- ✓ Replace thermal paper roll
- ✓ Clean print head
- ✓ Check paper quality

### Cash Drawer Issues
**Problem**: Drawer not opening
- ✓ Check RJ11/RJ12 cable connection to printer
- ✓ Verify cable plugged into correct port
- ✓ Test manual open (if available on drawer)
- ✓ Check cash_drawer_port setting in code

### Product Not Found
**Problem**: Scanned barcode shows "Product Not Found"
- ✓ Verify product exists in database (Products → Manage Products)
- ✓ Check barcode scanned correctly
- ✓ Add product if missing

### Application Crashes
- ✓ Check Python installed correctly
- ✓ Verify all packages installed (`pip list`)
- ✓ Check database file not corrupted
- ✓ Restart application

---

## Best Practices

### Daily Operations
1. **Morning**:
   - Start POS system
   - Check low stock alerts
   - Count cash drawer
   - Test printer

2. **During Day**:
   - Process sales normally
   - Monitor low stock alerts
   - Restock as needed

3. **End of Day**:
   - Run sales report (Today)
   - Count cash drawer
   - Reconcile cash vs. sales
   - Back up database

### Stock Management
- Set realistic low stock thresholds (typically 10-20% of normal stock)
- Check inventory report weekly
- Reorder before items reach zero
- Update stock quantities when receiving shipments

### Data Backup
- Database file: `lastkings_pos.db`
- Back up daily to external location
- Keep 7-30 days of backups
- Test restore process periodically

### Security
- Restrict POS system access to authorized staff only
- Keep backup receipts for audit purposes
- Monitor sales reports for discrepancies
- Lock computer when unattended

---

## Database Location

**Database File**: `lastkings_pos.db` (same folder as pos_system.py)

**Tables**:
- `products` - Product catalog
- `sales` - Sale transactions
- `sale_items` - Individual items per sale

**Backup**: Copy `lastkings_pos.db` to safe location daily

---

## Support & Maintenance

### Regular Maintenance
- **Weekly**: Check inventory report
- **Monthly**: Review sales reports
- **Monthly**: Clean hardware (scanner, printer)
- **Monthly**: Update low stock thresholds as needed
- **Quarterly**: Database backup verification

### Getting Help
- Check this user guide first
- Review README.txt for technical details
- Check printer/scanner manufacturer documentation
- Contact system administrator

---

## Keyboard Reference

| Key | Action |
|-----|--------|
| Enter | Add scanned barcode to cart |
| Tab | Navigate between fields |
| Esc | Cancel current dialog |

---

## System Requirements

- Windows 7 or higher
- Python 3.8+
- USB ports for scanner and printer
- Minimum 4GB RAM
- 100MB free disk space

---

*LastKings Liquor Store POS System v1.0*
*Copyright 2025*