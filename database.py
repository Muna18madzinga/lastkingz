import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "lastkings_pos.db"):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                low_stock_threshold INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_amount REAL NOT NULL,
                cash_received REAL NOT NULL,
                change_given REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cashier_id INTEGER,
                payment_method TEXT DEFAULT 'cash',
                FOREIGN KEY (cashier_id) REFERENCES users(id)
            )
        ''')

        # Add cashier_id column if it doesn't exist (migration)
        try:
            cursor.execute('ALTER TABLE sales ADD COLUMN cashier_id INTEGER')
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

        # Add payment_method column if it doesn't exist (migration)
        try:
            cursor.execute('ALTER TABLE sales ADD COLUMN payment_method TEXT DEFAULT "cash"')
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

        # Sale items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                barcode TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_product(self, barcode: str, name: str, price: float, stock: int, low_stock_threshold: int = 10):
        """Add a new product to inventory"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (barcode, name, price, stock, low_stock_threshold)
                VALUES (?, ?, ?, ?, ?)
            ''', (barcode, name, price, stock, low_stock_threshold))
            conn.commit()
            return True, "Product added successfully"
        except sqlite3.IntegrityError:
            return False, "Product with this barcode already exists"
        finally:
            conn.close()

    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Get product details by barcode"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'barcode': row[1],
                'name': row[2],
                'price': row[3],
                'stock': row[4],
                'low_stock_threshold': row[5]
            }
        return None

    def update_stock(self, product_id: int, quantity_sold: int) -> bool:
        """Reduce stock after a sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products
            SET stock = stock - ?
            WHERE id = ? AND stock >= ?
        ''', (quantity_sold, product_id, quantity_sold))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def check_low_stock(self, product_id: int) -> bool:
        """Check if product stock is below threshold"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT stock, low_stock_threshold
            FROM products
            WHERE id = ?
        ''', (product_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0] <= row[1]
        return False

    def get_low_stock_products(self) -> List[Dict]:
        """Get all products with low stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, barcode, name, stock, low_stock_threshold
            FROM products
            WHERE stock <= low_stock_threshold
        ''')
        rows = cursor.fetchall()
        conn.close()

        return [{
            'id': row[0],
            'barcode': row[1],
            'name': row[2],
            'stock': row[3],
            'low_stock_threshold': row[4]
        } for row in rows]

    def save_sale(self, items: List[Dict], total_amount: float, cash_received: float, change_given: float, cashier_id: int = None, payment_method: str = 'cash') -> int:
        """Save sale transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Insert sale
        cursor.execute('''
            INSERT INTO sales (total_amount, cash_received, change_given, cashier_id, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (total_amount, cash_received, change_given, cashier_id, payment_method))
        sale_id = cursor.lastrowid

        # Insert sale items
        for item in items:
            cursor.execute('''
                INSERT INTO sale_items (sale_id, product_id, barcode, product_name, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sale_id, item['product_id'], item['barcode'], item['name'],
                  item['quantity'], item['price'], item['subtotal']))

        conn.commit()
        conn.close()
        return sale_id

    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY name')
        rows = cursor.fetchall()
        conn.close()

        return [{
            'id': row[0],
            'barcode': row[1],
            'name': row[2],
            'price': row[3],
            'stock': row[4],
            'low_stock_threshold': row[5]
        } for row in rows]

    def update_product_stock(self, product_id: int, new_stock: int):
        """Update product stock to a specific value"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products
            SET stock = ?
            WHERE id = ?
        ''', (new_stock, product_id))
        conn.commit()
        conn.close()

    def update_product(self, product_id: int, name: str, price: float, stock: int, low_stock_threshold: int):
        """Update product details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products
            SET name = ?, price = ?, stock = ?, low_stock_threshold = ?
            WHERE id = ?
        ''', (name, price, stock, low_stock_threshold, product_id))
        conn.commit()
        conn.close()

    def delete_product(self, product_id: int):
        """Delete a product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

    def get_sales_report(self, start_date: str = None, end_date: str = None) -> Dict:
        """Get sales report for date range"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute('''
                SELECT COUNT(*), SUM(total_amount), SUM(cash_received), SUM(change_given)
                FROM sales
                WHERE date(sale_date) BETWEEN ? AND ?
            ''', (start_date, end_date))
        else:
            cursor.execute('''
                SELECT COUNT(*), SUM(total_amount), SUM(cash_received), SUM(change_given)
                FROM sales
            ''')

        row = cursor.fetchone()
        conn.close()

        return {
            'total_sales': row[0] or 0,
            'total_revenue': row[1] or 0.0,
            'total_cash': row[2] or 0.0,
            'total_change': row[3] or 0.0
        }