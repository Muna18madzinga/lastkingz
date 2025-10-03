"""
Bulk product entry - paste your barcodes and details
Edit this file with your products, then run it
"""

from database import Database

# ADD YOUR PRODUCTS HERE
# Format: (barcode, name, price, stock, low_stock_threshold)
products = [
    ("6007616000633", "Product 1 - Update Name", 10.00, 50, 10),
    # Add more products below:
    # ("barcode_here", "Product Name", price, stock, threshold),
]

def add_bulk_products():
    db = Database()

    print("=" * 60)
    print("Adding Products to Database")
    print("=" * 60)

    for barcode, name, price, stock, threshold in products:
        success, message = db.add_product(barcode, name, price, stock, threshold)
        if success:
            print(f"[OK] Added: {name} (${price:.2f})")
        else:
            print(f"[SKIP] {barcode}: {message}")

    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)

    all_products = db.get_all_products()
    print(f"\nTotal products in database: {len(all_products)}")

if __name__ == "__main__":
    add_bulk_products()
    input("\nPress Enter to exit...")