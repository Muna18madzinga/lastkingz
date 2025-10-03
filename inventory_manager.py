from database import Database
from typing import List, Dict

class InventoryManager:
    """Manages inventory updates and stock alerts"""

    def __init__(self, db: Database):
        self.db = db
        self.low_stock_alerts = []

    def process_sale(self, items: List[Dict]) -> Dict:
        """
        Process sale and update inventory.
        Returns dict with 'success' status and any alerts.
        """
        alerts = []
        failed_items = []

        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']

            # Update stock
            success = self.db.update_stock(product_id, quantity)

            if not success:
                failed_items.append(item['name'])
                continue

            # Check for low stock
            if self.db.check_low_stock(product_id):
                product = self.db.get_product_by_barcode(item['barcode'])
                if product:
                    alerts.append({
                        'product_name': product['name'],
                        'current_stock': product['stock'],
                        'threshold': product['low_stock_threshold'],
                        'message': f"LOW STOCK ALERT: {product['name']} - Only {product['stock']} left!"
                    })

        return {
            'success': len(failed_items) == 0,
            'failed_items': failed_items,
            'low_stock_alerts': alerts
        }

    def get_all_low_stock_items(self) -> List[Dict]:
        """Get all products currently below stock threshold"""
        return self.db.get_low_stock_products()

    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT stock FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0] >= quantity
        return False

    def get_inventory_report(self) -> Dict:
        """Generate inventory status report"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Total products
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0]

        # Low stock items
        low_stock = self.get_all_low_stock_items()

        # Out of stock
        cursor.execute('SELECT COUNT(*) FROM products WHERE stock = 0')
        out_of_stock = cursor.fetchone()[0]

        # Total inventory value
        cursor.execute('SELECT SUM(stock * price) FROM products')
        total_value = cursor.fetchone()[0] or 0

        # Get all products
        all_products = self.db.get_all_products()

        conn.close()

        return {
            'total_products': total_products,
            'low_stock_count': len(low_stock),
            'out_of_stock_count': out_of_stock,
            'total_inventory_value': total_value,
            'low_stock_items': low_stock,
            'all_products': all_products
        }