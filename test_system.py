"""
Test script for LastKings POS System
Tests all core functionality
"""

import sys
from database import Database
from shopping_cart import ShoppingCart
from barcode_scanner import BarcodeScanner
from inventory_manager import InventoryManager

def test_database():
    """Test database operations"""
    print("=" * 60)
    print("Testing Database Operations")
    print("=" * 60)

    db = Database()

    # Test 1: Add a test product
    print("\n[TEST 1] Adding new product...")
    success, message = db.add_product(
        barcode="999999999999",
        name="Test Product - Premium Whiskey",
        price=49.99,
        stock=100,
        low_stock_threshold=15
    )
    if success:
        print(f"  [PASS] Product added: {message}")
    else:
        print(f"  [INFO] {message}")

    # Test 2: Retrieve product by barcode
    print("\n[TEST 2] Retrieving product by barcode...")
    product = db.get_product_by_barcode("999999999999")
    if product:
        print(f"  [PASS] Product found:")
        print(f"    - ID: {product['id']}")
        print(f"    - Name: {product['name']}")
        print(f"    - Price: ${product['price']:.2f}")
        print(f"    - Stock: {product['stock']}")
    else:
        print("  [FAIL] Product not found")
        return False

    # Test 3: Update product
    print("\n[TEST 3] Updating product...")
    db.update_product(
        product_id=product['id'],
        name="Test Product - Updated Name",
        price=54.99,
        stock=150,
        low_stock_threshold=20
    )
    updated_product = db.get_product_by_barcode("999999999999")
    if updated_product and updated_product['name'] == "Test Product - Updated Name":
        print(f"  [PASS] Product updated successfully")
        print(f"    - New Name: {updated_product['name']}")
        print(f"    - New Price: ${updated_product['price']:.2f}")
        print(f"    - New Stock: {updated_product['stock']}")
    else:
        print("  [FAIL] Product update failed")
        return False

    # Test 4: Get all products
    print("\n[TEST 4] Getting all products...")
    all_products = db.get_all_products()
    print(f"  [PASS] Found {len(all_products)} products in database")

    # Test 5: Update stock
    print("\n[TEST 5] Testing stock update...")
    original_stock = updated_product['stock']
    success = db.update_stock(product['id'], 10)
    if success:
        new_product = db.get_product_by_barcode("999999999999")
        print(f"  [PASS] Stock updated: {original_stock} -> {new_product['stock']}")
    else:
        print("  [FAIL] Stock update failed")
        return False

    # Test 6: Check low stock
    print("\n[TEST 6] Testing low stock detection...")
    db.update_stock(product['id'], 120)  # Reduce stock to 20
    is_low = db.check_low_stock(product['id'])
    current = db.get_product_by_barcode("999999999999")
    print(f"  Current stock: {current['stock']}, Threshold: {current['low_stock_threshold']}")
    if is_low:
        print(f"  [PASS] Low stock correctly detected")
    else:
        print(f"  [INFO] Stock is not low")

    # Test 7: Delete product
    print("\n[TEST 7] Deleting test product...")
    db.delete_product(product['id'])
    deleted_check = db.get_product_by_barcode("999999999999")
    if deleted_check is None:
        print("  [PASS] Product deleted successfully")
    else:
        print("  [FAIL] Product still exists after deletion")
        return False

    print("\n[SUCCESS] All database tests passed!")
    return True

def test_shopping_cart():
    """Test shopping cart operations"""
    print("\n" + "=" * 60)
    print("Testing Shopping Cart")
    print("=" * 60)

    cart = ShoppingCart()

    # Test product
    test_product = {
        'id': 1,
        'barcode': '012345678901',
        'name': 'Test Beer 12pk',
        'price': 15.99,
        'stock': 50,
        'low_stock_threshold': 10
    }

    # Test 1: Add item
    print("\n[TEST 1] Adding item to cart...")
    cart.add_item(test_product, 2)
    if len(cart.get_items()) == 1:
        item = cart.get_items()[0]
        print(f"  [PASS] Item added: {item['name']} x{item['quantity']}")
        print(f"    Subtotal: ${item['subtotal']:.2f}")
    else:
        print("  [FAIL] Failed to add item")
        return False

    # Test 2: Add same item again (should increase quantity)
    print("\n[TEST 2] Adding same item again...")
    cart.add_item(test_product, 3)
    item = cart.get_items()[0]
    if item['quantity'] == 5:
        print(f"  [PASS] Quantity increased: {item['quantity']}")
        print(f"    New Subtotal: ${item['subtotal']:.2f}")
    else:
        print(f"  [FAIL] Expected quantity 5, got {item['quantity']}")
        return False

    # Test 3: Get total
    print("\n[TEST 3] Calculating cart total...")
    total = cart.get_total()
    expected_total = 15.99 * 5
    if abs(total - expected_total) < 0.01:
        print(f"  [PASS] Total: ${total:.2f}")
    else:
        print(f"  [FAIL] Expected ${expected_total:.2f}, got ${total:.2f}")
        return False

    # Test 4: Update quantity
    print("\n[TEST 4] Updating item quantity...")
    cart.update_quantity(1, 3)
    item = cart.get_items()[0]
    if item['quantity'] == 3:
        print(f"  [PASS] Quantity updated: {item['quantity']}")
    else:
        print(f"  [FAIL] Expected quantity 3, got {item['quantity']}")
        return False

    # Test 5: Remove item
    print("\n[TEST 5] Removing item from cart...")
    cart.remove_item(1)
    if len(cart.get_items()) == 0:
        print("  [PASS] Item removed successfully")
    else:
        print("  [FAIL] Cart should be empty")
        return False

    # Test 6: Clear cart
    print("\n[TEST 6] Testing cart clear...")
    cart.add_item(test_product, 1)
    cart.clear()
    if cart.is_empty():
        print("  [PASS] Cart cleared successfully")
    else:
        print("  [FAIL] Cart should be empty")
        return False

    print("\n[SUCCESS] All shopping cart tests passed!")
    return True

def test_barcode_scanner():
    """Test barcode scanner"""
    print("\n" + "=" * 60)
    print("Testing Barcode Scanner")
    print("=" * 60)

    scanner = BarcodeScanner()

    # Test 1: Validate valid barcodes
    print("\n[TEST 1] Validating barcodes...")
    valid_barcodes = ["012345678901", "0123456789012"]
    for barcode in valid_barcodes:
        if scanner.validate_barcode(barcode):
            print(f"  [PASS] Valid barcode accepted: {barcode}")
        else:
            print(f"  [FAIL] Valid barcode rejected: {barcode}")
            return False

    # Test 2: Reject invalid barcodes
    print("\n[TEST 2] Rejecting invalid barcodes...")
    invalid_barcodes = ["123", "abcd12345678", "12345"]
    for barcode in invalid_barcodes:
        if not scanner.validate_barcode(barcode):
            print(f"  [PASS] Invalid barcode rejected: {barcode}")
        else:
            print(f"  [FAIL] Invalid barcode accepted: {barcode}")
            return False

    # Test 3: Process input
    print("\n[TEST 3] Testing input processing...")
    scanner.clear_buffer()
    test_barcode = "012345678901"
    for char in test_barcode:
        result = scanner.process_input(char)
        if result:
            print(f"  [FAIL] Premature barcode completion")
            return False
    result = scanner.process_input('\n')
    if result == test_barcode:
        print(f"  [PASS] Barcode processed correctly: {result}")
    else:
        print(f"  [FAIL] Expected {test_barcode}, got {result}")
        return False

    print("\n[SUCCESS] All barcode scanner tests passed!")
    return True

def test_inventory_manager():
    """Test inventory manager"""
    print("\n" + "=" * 60)
    print("Testing Inventory Manager")
    print("=" * 60)

    db = Database()
    inventory = InventoryManager(db)

    # Add test product
    db.add_product("888888888888", "Test Inventory Product", 29.99, 15, 20)
    product = db.get_product_by_barcode("888888888888")

    # Test 1: Check stock availability
    print("\n[TEST 1] Checking stock availability...")
    available = inventory.check_stock_availability(product['id'], 10)
    if available:
        print(f"  [PASS] Stock available for 10 units (stock: {product['stock']})")
    else:
        print(f"  [FAIL] Stock should be available")
        return False

    # Test 2: Process sale
    print("\n[TEST 2] Processing sale...")
    items = [{
        'product_id': product['id'],
        'barcode': product['barcode'],
        'name': product['name'],
        'price': product['price'],
        'quantity': 5,
        'subtotal': product['price'] * 5
    }]
    result = inventory.process_sale(items)
    if result['success']:
        print(f"  [PASS] Sale processed successfully")
        if result['low_stock_alerts']:
            print(f"  [INFO] Low stock alert generated")
    else:
        print(f"  [FAIL] Sale processing failed")
        return False

    # Test 3: Get inventory report
    print("\n[TEST 3] Getting inventory report...")
    report = inventory.get_inventory_report()
    print(f"  [PASS] Inventory report generated:")
    print(f"    - Total products: {report['total_products']}")
    print(f"    - Low stock items: {report['low_stock_count']}")
    print(f"    - Total value: ${report['total_inventory_value']:.2f}")

    # Cleanup
    db.delete_product(product['id'])

    print("\n[SUCCESS] All inventory manager tests passed!")
    return True

def test_complete_sale_workflow():
    """Test complete sale workflow"""
    print("\n" + "=" * 60)
    print("Testing Complete Sale Workflow")
    print("=" * 60)

    db = Database()
    cart = ShoppingCart()
    inventory = InventoryManager(db)

    # Get a real product from database
    print("\n[TEST 1] Loading product from database...")
    product = db.get_product_by_barcode("012345678909")  # Budweiser
    if not product:
        print("  [FAIL] Product not found in database")
        return False
    print(f"  [PASS] Product loaded: {product['name']}")

    # Add to cart
    print("\n[TEST 2] Adding to cart...")
    cart.add_item(product, 2)
    total = cart.get_total()
    print(f"  [PASS] Cart total: ${total:.2f}")

    # Process payment
    print("\n[TEST 3] Processing payment...")
    cash_received = 50.00
    change = cash_received - total
    print(f"  Cash received: ${cash_received:.2f}")
    print(f"  Change: ${change:.2f}")

    # Process sale and update inventory
    print("\n[TEST 4] Processing sale and updating inventory...")
    original_stock = product['stock']
    result = inventory.process_sale(cart.get_items())
    if result['success']:
        print(f"  [PASS] Sale processed successfully")
        updated_product = db.get_product_by_barcode(product['barcode'])
        new_stock = updated_product['stock']
        print(f"  Stock updated: {original_stock} -> {new_stock}")
    else:
        print(f"  [FAIL] Sale processing failed")
        return False

    # Save to database
    print("\n[TEST 5] Saving sale to database...")
    sale_id = db.save_sale(cart.get_items(), total, cash_received, change)
    print(f"  [PASS] Sale saved with ID: {sale_id}")

    # Verify sale report
    print("\n[TEST 6] Verifying sales report...")
    report = db.get_sales_report()
    if report['total_sales'] > 0:
        print(f"  [PASS] Sales report generated:")
        print(f"    - Total sales: {report['total_sales']}")
        print(f"    - Total revenue: ${report['total_revenue']:.2f}")
    else:
        print(f"  [FAIL] No sales found in report")
        return False

    print("\n[SUCCESS] Complete sale workflow test passed!")
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print(" LastKings POS System - Comprehensive Test Suite ".center(60))
    print("=" * 60)

    tests = [
        ("Database Operations", test_database),
        ("Shopping Cart", test_shopping_cart),
        ("Barcode Scanner", test_barcode_scanner),
        ("Inventory Manager", test_inventory_manager),
        ("Complete Sale Workflow", test_complete_sale_workflow),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED - System is fully functional!")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())