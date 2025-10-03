"""
Sample script to populate database with liquor store products.
Run this once to add sample products for testing.
"""

from database import Database

def add_sample_products():
    db = Database()

    products = [
        # Whiskey
        ("012345678901", "Jack Daniels 750ml", 24.99, 50, 10),
        ("012345678902", "Jim Beam 1L", 19.99, 45, 10),
        ("012345678903", "Jameson Irish Whiskey 750ml", 29.99, 30, 8),
        ("012345678904", "Crown Royal 750ml", 32.99, 25, 8),

        # Vodka
        ("012345678905", "Absolut Vodka 750ml", 21.99, 40, 10),
        ("012345678906", "Grey Goose 750ml", 39.99, 20, 5),
        ("012345678907", "Smirnoff 1L", 18.99, 60, 15),
        ("012345678908", "Tito's Handmade Vodka 750ml", 24.99, 35, 10),

        # Beer
        ("012345678909", "Budweiser 12pk", 14.99, 100, 20),
        ("012345678910", "Corona Extra 12pk", 16.99, 80, 20),
        ("012345678911", "Heineken 12pk", 17.99, 70, 15),
        ("012345678912", "Modelo Especial 12pk", 16.49, 75, 15),

        # Wine
        ("012345678913", "Barefoot Moscato 750ml", 8.99, 50, 10),
        ("012345678914", "Kendall Jackson Chardonnay", 12.99, 40, 10),
        ("012345678915", "Yellow Tail Cabernet 750ml", 7.99, 60, 15),

        # Rum
        ("012345678916", "Bacardi Superior 750ml", 15.99, 45, 10),
        ("012345678917", "Captain Morgan Spiced 750ml", 17.99, 40, 10),

        # Tequila
        ("012345678918", "Jose Cuervo Gold 750ml", 19.99, 35, 8),
        ("012345678919", "Patron Silver 750ml", 49.99, 15, 5),

        # Gin
        ("012345678920", "Tanqueray London Dry 750ml", 24.99, 30, 8),
        ("012345678921", "Bombay Sapphire 750ml", 26.99, 25, 8),
    ]

    print("Adding sample products to database...")
    for barcode, name, price, stock, threshold in products:
        success, message = db.add_product(barcode, name, price, stock, threshold)
        if success:
            print(f"[OK] Added: {name}")
        else:
            print(f"[FAIL] Failed: {name} - {message}")

    print("\nSample products added successfully!")
    print("You can now run pos_system.py to start the POS system.")

if __name__ == "__main__":
    add_sample_products()