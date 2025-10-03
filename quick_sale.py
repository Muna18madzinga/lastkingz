import sqlite3

class QuickSaleManager:
    """Manage quick sale items (non-barcode items)"""

    def __init__(self, db_name="lastkings_pos.db"):
        self.db_name = db_name
        self.init_quick_sale_table()
        self.create_default_items()

    def init_quick_sale_table(self):
        """Initialize quick sale items table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quick_sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT,
                icon TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def create_default_items(self):
        """Create default quick sale items"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if items exist
        cursor.execute("SELECT COUNT(*) FROM quick_sale_items")
        if cursor.fetchone()[0] == 0:
            default_items = [
                ('Ice Bag', 2.00, 'Supplies', '❄️', 1),
                ('Plastic Cups', 0.50, 'Supplies', '🥤', 2),
                ('Cigarettes', 8.00, 'Tobacco', '🚬', 3),
                ('Lighter', 1.50, 'Tobacco', '🔥', 4),
                ('Rolling Papers', 1.00, 'Tobacco', '📄', 5),
                ('Plastic Bag', 0.25, 'Supplies', '🛍️', 6),
                ('Energy Drink', 2.50, 'Drinks', '⚡', 7),
                ('Water Bottle', 1.00, 'Drinks', '💧', 8),
            ]

            cursor.executemany("""
                INSERT INTO quick_sale_items (name, price, category, icon, display_order)
                VALUES (?, ?, ?, ?, ?)
            """, default_items)

            conn.commit()

        conn.close()

    def get_all_items(self, active_only=True):
        """Get all quick sale items"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if active_only:
            cursor.execute("""
                SELECT id, name, price, category, icon, display_order, is_active
                FROM quick_sale_items
                WHERE is_active = 1
                ORDER BY display_order, name
            """)
        else:
            cursor.execute("""
                SELECT id, name, price, category, icon, display_order, is_active
                FROM quick_sale_items
                ORDER BY display_order, name
            """)

        items = [{'id': r[0], 'name': r[1], 'price': r[2], 'category': r[3],
                 'icon': r[4], 'display_order': r[5], 'is_active': r[6]}
                for r in cursor.fetchall()]

        conn.close()
        return items

    def add_item(self, name, price, category='', icon='📦', display_order=0):
        """Add new quick sale item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO quick_sale_items (name, price, category, icon, display_order)
                VALUES (?, ?, ?, ?, ?)
            """, (name, price, category, icon, display_order))
            conn.commit()
            item_id = cursor.lastrowid
            conn.close()
            return item_id
        except Exception as e:
            conn.close()
            return None

    def update_item(self, item_id, name, price, category='', icon='📦', display_order=0):
        """Update quick sale item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE quick_sale_items
            SET name = ?, price = ?, category = ?, icon = ?, display_order = ?
            WHERE id = ?
        """, (name, price, category, icon, display_order, item_id))

        conn.commit()
        conn.close()
        return True

    def delete_item(self, item_id):
        """Delete (deactivate) quick sale item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE quick_sale_items
            SET is_active = 0
            WHERE id = ?
        """, (item_id,))

        conn.commit()
        conn.close()
        return True

    def get_item_by_id(self, item_id):
        """Get single item by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, price, category, icon, display_order, is_active
            FROM quick_sale_items
            WHERE id = ?
        """, (item_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {'id': row[0], 'name': row[1], 'price': row[2], 'category': row[3],
                   'icon': row[4], 'display_order': row[5], 'is_active': row[6]}
        return None
