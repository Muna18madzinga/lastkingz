"""
Migrate quick sale items to the products table
"""
from database import Database
from quick_sale import QuickSaleManager

db = Database()
qs = QuickSaleManager()

# Get all quick sale items
quick_items = qs.get_all_items()

print(f"Found {len(quick_items)} quick sale items to migrate")

# Add each quick sale item to products table
for item in quick_items:
    # Create a unique barcode for quick sale items
    barcode = f"QUICK{item['id']:04d}"

    # Check if already exists
    existing = db.get_product_by_barcode(barcode)
    if existing:
        print(f"  [SKIP] {item['name']} - already exists with barcode {barcode}")
        continue

    # Add to products table with high stock (9999) since these don't track inventory
    success, message = db.add_product(
        barcode=barcode,
        name=item['name'],
        price=item['price'],
        stock=9999,  # High stock so they never run out
        low_stock_threshold=0  # No low stock alerts for quick sale items
    )

    if success:
        print(f"  [OK] Added {item['name']} with barcode {barcode}")
    else:
        print(f"  [ERROR] Failed to add {item['name']}: {message}")

print("\nMigration complete!")
print("Quick sale items are now in the products table and can be managed via Products page.")
