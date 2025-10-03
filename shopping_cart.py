from typing import List, Dict

class ShoppingCart:
    def __init__(self):
        self.items: List[Dict] = []

    def add_item(self, product: Dict, quantity: int = 1):
        """Add product to cart or increase quantity if already exists"""
        # Check if product already in cart
        for item in self.items:
            if item['product_id'] == product['id']:
                item['quantity'] += quantity
                item['subtotal'] = item['quantity'] * item['price']
                return

        # Add new item
        self.items.append({
            'product_id': product['id'],
            'barcode': product['barcode'],
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'subtotal': product['price'] * quantity
        })

    def remove_item(self, product_id: int):
        """Remove item from cart"""
        self.items = [item for item in self.items if item['product_id'] != product_id]

    def update_quantity(self, product_id: int, quantity: int):
        """Update item quantity"""
        for item in self.items:
            if item['product_id'] == product_id:
                if quantity > 0:
                    item['quantity'] = quantity
                    item['subtotal'] = item['quantity'] * item['price']
                else:
                    self.remove_item(product_id)
                return

    def get_total(self) -> float:
        """Calculate cart total"""
        return sum(item['subtotal'] for item in self.items)

    def get_items(self) -> List[Dict]:
        """Get all cart items"""
        return self.items.copy()

    def clear(self):
        """Clear all items from cart"""
        self.items = []

    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.items) == 0

    def get_item_count(self) -> int:
        """Get total number of items"""
        return sum(item['quantity'] for item in self.items)