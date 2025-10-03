"""
Interactive product entry system
Scan barcodes and enter product details
"""

from database import Database

def add_products_interactive():
    """Add products interactively by scanning barcodes"""
    db = Database()

    print("=" * 60)
    print("LastKings Liquor Store - Product Entry System")
    print("=" * 60)
    print("\nEnter product details. Type 'done' to finish.\n")

    while True:
        print("-" * 60)

        # Get barcode
        barcode = input("\nScan or enter barcode (or 'done' to finish): ").strip()

        if barcode.lower() == 'done':
            break

        if not barcode:
            continue

        # Check if product already exists
        existing = db.get_product_by_barcode(barcode)
        if existing:
            print(f"\n[INFO] Product already exists: {existing['name']}")
            update = input("Update this product? (y/n): ").strip().lower()
            if update != 'y':
                continue

            # Update existing product
            print(f"\nCurrent details:")
            print(f"  Name: {existing['name']}")
            print(f"  Price: ${existing['price']:.2f}")
            print(f"  Stock: {existing['stock']}")
            print(f"  Low Stock Alert: {existing['low_stock_threshold']}")
            print()

            name = input(f"Product name [{existing['name']}]: ").strip() or existing['name']
            price_input = input(f"Price (dollars) [{existing['price']:.2f}]: ").strip()
            price = float(price_input) if price_input else existing['price']
            stock_input = input(f"Stock quantity [{existing['stock']}]: ").strip()
            stock = int(stock_input) if stock_input else existing['stock']
            threshold_input = input(f"Low stock alert [{existing['low_stock_threshold']}]: ").strip()
            threshold = int(threshold_input) if threshold_input else existing['low_stock_threshold']

            db.update_product(existing['id'], name, price, stock, threshold)
            print(f"\n[SUCCESS] Product updated: {name}")

        else:
            # Add new product
            print(f"\nBarcode: {barcode}")
            name = input("Product name: ").strip()

            if not name:
                print("[ERROR] Product name is required")
                continue

            try:
                price = float(input("Price (dollars): ").strip())
                stock = int(input("Stock quantity: ").strip())
                threshold_input = input("Low stock alert [10]: ").strip()
                threshold = int(threshold_input) if threshold_input else 10

                success, message = db.add_product(barcode, name, price, stock, threshold)

                if success:
                    print(f"\n[SUCCESS] Product added: {name}")
                    print(f"  Price: ${price:.2f}")
                    print(f"  Stock: {stock} units")
                else:
                    print(f"\n[ERROR] {message}")

            except ValueError:
                print("[ERROR] Invalid input. Please enter valid numbers.")

    # Show summary
    print("\n" + "=" * 60)
    print("Product Entry Complete")
    print("=" * 60)

    all_products = db.get_all_products()
    print(f"\nTotal products in database: {len(all_products)}")

    if all_products:
        print("\nCurrent inventory:")
        for p in all_products:
            print(f"  - {p['name']} (${p['price']:.2f}) - Stock: {p['stock']}")

    print("\nYou can now start the POS system: py pos_system.py")

if __name__ == "__main__":
    add_products_interactive()