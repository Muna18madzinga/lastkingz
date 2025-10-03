"""
LastKingz POS - Flask Web Application
Multi-workstation POS system with separate manager and cashier interfaces
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
from datetime import datetime, timedelta
import os
from database import Database
from user_auth import UserAuth
from shopping_cart import ShoppingCart
from inventory_manager import InventoryManager
from quick_sale import QuickSaleManager

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=8)

# Initialize components
db = Database()
auth = UserAuth()
inventory = InventoryManager(db)
quick_sale = QuickSaleManager()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Manager only decorator
def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != UserAuth.ROLE_MANAGER:
            flash('Manager access required', 'danger')
            return redirect(url_for('cashier_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == UserAuth.ROLE_MANAGER:
            return redirect(url_for('manager_dashboard'))
        else:
            return redirect(url_for('cashier_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = auth.authenticate(username, password)
        if user:
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']

            if user['role'] == UserAuth.ROLE_MANAGER:
                return redirect(url_for('manager_dashboard'))
            else:
                return redirect(url_for('cashier_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Manager Routes
@app.route('/manager/dashboard')
@manager_required
def manager_dashboard():
    # Get dashboard statistics
    conn = db.get_connection()
    cursor = conn.cursor()

    # Today's sales
    today = datetime.now().date()
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) = ?
    """, (today,))
    today_count, today_total = cursor.fetchone()

    # Today's sales by payment method
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
            COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
        FROM sales
        WHERE DATE(sale_date) = ?
    """, (today,))
    today_cash, today_ecocash = cursor.fetchone()

    # This week's sales
    week_start = today - timedelta(days=today.weekday())
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) >= ?
    """, (week_start,))
    week_count, week_total = cursor.fetchone()

    # This week's sales by payment method
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
            COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
        FROM sales
        WHERE DATE(sale_date) >= ?
    """, (week_start,))
    week_cash, week_ecocash = cursor.fetchone()

    # Low stock items
    cursor.execute("""
        SELECT name, stock, low_stock_threshold
        FROM products
        WHERE stock <= low_stock_threshold
        ORDER BY stock ASC
        LIMIT 10
    """)
    low_stock_items = cursor.fetchall()

    # Recent sales
    cursor.execute("""
        SELECT id, total_amount, sale_date
        FROM sales
        ORDER BY sale_date DESC
        LIMIT 5
    """)
    recent_sales = cursor.fetchall()

    stats = {
        'today_sales': today_count,
        'today_revenue': today_total,
        'today_cash': today_cash,
        'today_ecocash': today_ecocash,
        'week_sales': week_count,
        'week_revenue': week_total,
        'week_cash': week_cash,
        'week_ecocash': week_ecocash,
        'low_stock_count': len(low_stock_items),
        'low_stock_items': low_stock_items,
        'recent_sales': recent_sales
    }

    return render_template('manager/dashboard.html', stats=stats, user=session)

@app.route('/manager/pos')
@manager_required
def manager_pos():
    products = db.get_all_products()
    quick_items = quick_sale.get_all_items()
    return render_template('manager/pos.html', products=products, quick_items=quick_items, user=session)

@app.route('/manager/products')
@manager_required
def manager_products():
    products = db.get_all_products()
    return render_template('manager/products.html', products=products, user=session)

@app.route('/manager/reports')
@manager_required
def manager_reports():
    return render_template('manager/reports.html', user=session)

@app.route('/manager/quick-sales')
@manager_required
def manager_quick_sales():
    quick_items = quick_sale.get_all_items(active_only=False)
    return render_template('manager/quick_sales.html', quick_items=quick_items, user=session)

# Cashier Routes
@app.route('/cashier/dashboard')
@login_required
def cashier_dashboard():
    # Get dashboard statistics
    conn = db.get_connection()
    cursor = conn.cursor()

    # Today's sales (all)
    today = datetime.now().date()
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) = ?
    """, (today,))
    today_count, today_total = cursor.fetchone()

    # Today's sales by payment method
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
            COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
        FROM sales
        WHERE DATE(sale_date) = ?
    """, (today,))
    cash_total, ecocash_total = cursor.fetchone()

    # My sales today
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) = ? AND cashier_id = ?
    """, (today, session.get('user_id')))
    my_count, my_total = cursor.fetchone()

    # My sales by payment method
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
            COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
        FROM sales
        WHERE DATE(sale_date) = ? AND cashier_id = ?
    """, (today, session.get('user_id')))
    my_cash_total, my_ecocash_total = cursor.fetchone()

    # Average sale
    avg_sale = today_total / today_count if today_count > 0 else 0

    # Recent sales by this cashier
    cursor.execute("""
        SELECT s.id, s.total_amount, s.sale_date, COUNT(si.id) as item_count
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        WHERE DATE(s.sale_date) = ? AND s.cashier_id = ?
        GROUP BY s.id
        ORDER BY s.sale_date DESC
        LIMIT 10
    """, (today, session.get('user_id')))
    recent_sales = cursor.fetchall()

    conn.close()

    stats = {
        'today_sales': today_count,
        'today_revenue': today_total,
        'cash_total': cash_total,
        'ecocash_total': ecocash_total,
        'my_sales': my_count,
        'my_revenue': my_total,
        'my_cash_total': my_cash_total,
        'my_ecocash_total': my_ecocash_total,
        'avg_sale': avg_sale,
        'recent_sales': recent_sales
    }

    return render_template('cashier/dashboard.html', stats=stats, user=session)

@app.route('/cashier/pos')
@login_required
def cashier_pos():
    products = db.get_all_products()
    quick_items = quick_sale.get_all_items()
    return render_template('cashier/pos.html', products=products, quick_items=quick_items, user=session)

# API Routes
@app.route('/api/product/<search_term>')
@login_required
def get_product(search_term):
    # Try to find by barcode first
    product = db.get_product_by_barcode(search_term)

    # If not found, try to search by name
    if not product:
        products = db.get_all_products()
        matching = [p for p in products if search_term.lower() in p['name'].lower()]
        if matching:
            return jsonify({
                'success': True,
                'product': matching[0]
            })

    if product:
        return jsonify({
            'success': True,
            'product': product
        })
    return jsonify({'success': False, 'message': 'Product not found'})

@app.route('/api/search-products')
@login_required
def search_products():
    query = request.args.get('q', '').lower()
    if not query or len(query) < 2:
        return jsonify({'success': False, 'products': []})

    products = db.get_all_products()
    results = [p for p in products if query in p['name'].lower() or query in p['barcode'].lower()]

    # Limit to 10 results
    results = results[:10]

    return jsonify({
        'success': True,
        'products': results
    })

@app.route('/api/complete-sale', methods=['POST'])
@login_required
def complete_sale():
    try:
        data = request.json
        items = data.get('items', [])
        cash_received = float(data.get('cash_received', 0))
        payment_method = data.get('payment_method', 'cash')

        if not items:
            return jsonify({'success': False, 'message': 'Cart is empty'})

        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)

        if cash_received < total:
            return jsonify({'success': False, 'message': 'Insufficient payment'})

        change = cash_received - total

        # Process inventory updates and collect low stock alerts
        failed_items = []
        low_stock_alerts = []
        out_of_stock_items = []

        # First pass: Check stock availability
        for item in items:
            # Skip inventory check for quick sale items
            if item['barcode'].startswith('QUICK'):
                continue

            product = db.get_product_by_barcode(item['barcode'])
            if not product:
                failed_items.append(item.get('name', 'Unknown'))
                continue

            # Check if sufficient stock available
            if product['stock'] < item['quantity']:
                out_of_stock_items.append({
                    'name': product['name'],
                    'requested': item['quantity'],
                    'available': product['stock']
                })

        if failed_items:
            return jsonify({
                'success': False,
                'message': f"Product not found: {', '.join(failed_items)}"
            })

        if out_of_stock_items:
            messages = [f"{item['name']}: requested {item['requested']}, only {item['available']} available"
                       for item in out_of_stock_items]
            return jsonify({
                'success': False,
                'message': f"Insufficient stock: {'; '.join(messages)}"
            })

        # Second pass: Update inventory
        for item in items:
            # Skip inventory updates for quick sale items
            if item['barcode'].startswith('QUICK'):
                continue

            product = db.get_product_by_barcode(item['barcode'])
            if product:
                # Update stock
                new_stock = product['stock'] - item['quantity']
                db.update_product_stock(product['id'], new_stock)

                # Check for low stock
                if new_stock <= product.get('low_stock_threshold', 10):
                    low_stock_alerts.append({
                        'product_name': product['name'],
                        'current_stock': new_stock,
                        'threshold': product.get('low_stock_threshold', 10),
                        'message': f"LOW STOCK ALERT: {product['name']} - Only {new_stock} left!"
                    })

        # Prepare items for saving (add subtotal and product_id fields)
        sale_items = []
        for item in items:
            # For quick sale items, extract numeric id from 'quick_X' format
            if isinstance(item['id'], str) and item['id'].startswith('quick_'):
                product_id = int(item['id'].replace('quick_', ''))
            else:
                product_id = item['id']

            sale_items.append({
                **item,
                'product_id': product_id,  # Rename id to product_id for database
                'subtotal': item['price'] * item['quantity']
            })

        # Save sale to database
        sale_id = db.save_sale(sale_items, total, cash_received, change, session.get('user_id'), payment_method)

        # Print receipt
        from receipt_printer import ReceiptPrinter
        printer = ReceiptPrinter()
        sale_data = {
            'total': total,
            'cash_received': cash_received,
            'change': change,
            'date': datetime.now()
        }
        print_success = printer.print_receipt(sale_data, sale_items)

        return jsonify({
            'success': True,
            'sale_id': sale_id,
            'change': change,
            'total': total,
            'receipt_printed': print_success,
            'low_stock_alerts': low_stock_alerts
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/quick-sale/<int:item_id>')
@login_required
def get_quick_sale_item(item_id):
    item = quick_sale.get_item_by_id(item_id)
    if item:
        return jsonify({'success': True, 'item': item})
    return jsonify({'success': False, 'message': 'Item not found'})

@app.route('/api/quick-sale', methods=['POST'])
@manager_required
def add_quick_sale_item():
    try:
        data = request.json
        item_id = quick_sale.add_item(
            data['name'],
            float(data['price']),
            data.get('category', ''),
            data.get('icon', '📦'),
            int(data.get('display_order', 0))
        )
        if item_id:
            return jsonify({'success': True, 'item_id': item_id})
        return jsonify({'success': False, 'message': 'Failed to add item'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/quick-sale/<int:item_id>', methods=['PUT'])
@manager_required
def update_quick_sale_item(item_id):
    try:
        data = request.json
        success = quick_sale.update_item(
            item_id,
            data['name'],
            float(data['price']),
            data.get('category', ''),
            data.get('icon', '📦'),
            int(data.get('display_order', 0))
        )
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Failed to update item'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/quick-sale/<int:item_id>', methods=['DELETE'])
@manager_required
def delete_quick_sale_item(item_id):
    try:
        success = quick_sale.delete_item(item_id)
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Failed to delete item'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Product Management API Routes
@app.route('/api/product-by-id/<int:product_id>')
@manager_required
def get_product_by_id(product_id):
    products = [p for p in db.get_all_products() if p['id'] == product_id]
    if products:
        return jsonify({'success': True, 'product': products[0]})
    return jsonify({'success': False, 'message': 'Product not found'})

@app.route('/api/product', methods=['POST'])
@manager_required
def add_product():
    try:
        data = request.json
        success, message = db.add_product(
            data['barcode'],
            data['name'],
            data['price'],
            data['stock'],
            data['low_stock_threshold']
        )
        if success:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/product/<int:product_id>', methods=['PUT'])
@manager_required
def update_product(product_id):
    try:
        data = request.json
        db.update_product(
            product_id,
            data['name'],
            data['price'],
            data['stock'],
            data['low_stock_threshold']
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/product/<int:product_id>', methods=['DELETE'])
@manager_required
def delete_product(product_id):
    try:
        db.delete_product(product_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/product/<int:product_id>/add-stock', methods=['POST'])
@manager_required
def add_stock(product_id):
    try:
        data = request.json
        quantity = data['quantity']

        # Get current product
        products = [p for p in db.get_all_products() if p['id'] == product_id]
        if not products:
            return jsonify({'success': False, 'message': 'Product not found'})

        product = products[0]
        new_stock = product['stock'] + quantity

        # Update stock
        db.update_product_stock(product_id, new_stock)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/product/<int:product_id>/remove-stock', methods=['POST'])
@manager_required
def remove_stock(product_id):
    try:
        data = request.json
        quantity = data['quantity']

        # Get current product
        products = [p for p in db.get_all_products() if p['id'] == product_id]
        if not products:
            return jsonify({'success': False, 'message': 'Product not found'})

        product = products[0]
        new_stock = product['stock'] - quantity

        if new_stock < 0:
            return jsonify({'success': False, 'message': 'Insufficient stock'})

        # Update stock
        db.update_product_stock(product_id, new_stock)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Sales Reports API Routes
@app.route('/api/sales-report/<period>')
@manager_required
def sales_report(period):
    try:
        today = datetime.now().date()

        if period == 'today':
            start_date = today
            end_date = today
            title = "Today's Sales"
        elif period == 'yesterday':
            start_date = today - timedelta(days=1)
            end_date = today - timedelta(days=1)
            title = "Yesterday's Sales"
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
            title = "This Week's Sales"
        elif period == 'month':
            start_date = today.replace(day=1)
            end_date = today
            title = "This Month's Sales"
        elif period == 'all':
            start_date = datetime(2000, 1, 1).date()
            end_date = datetime(2099, 12, 31).date()
            title = "All Time Sales"
        else:
            return jsonify({'success': False, 'message': 'Invalid period'})

        # Get summary
        summary = db.get_sales_report(str(start_date), str(end_date))

        # Get individual sales
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.sale_date, s.total_amount, s.cash_received, s.change_given,
                   COUNT(si.id) as item_count
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            WHERE date(s.sale_date) BETWEEN ? AND ?
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        ''', (str(start_date), str(end_date)))
        sales_data = cursor.fetchall()
        conn.close()

        sales = []
        for sale in sales_data:
            sales.append({
                'id': sale[0],
                'sale_date': sale[1],
                'total_amount': sale[2],
                'cash_received': sale[3],
                'change_given': sale[4],
                'item_count': sale[5]
            })

        return jsonify({
            'success': True,
            'title': title,
            'summary': summary,
            'sales': sales
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/sale-details/<int:sale_id>')
@manager_required
def sale_details(sale_id):
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT product_name, quantity, unit_price, subtotal
            FROM sale_items
            WHERE sale_id = ?
        ''', (sale_id,))
        items_data = cursor.fetchall()
        conn.close()

        items = []
        for item in items_data:
            items.append({
                'product_name': item[0],
                'quantity': item[1],
                'unit_price': item[2],
                'subtotal': item[3]
            })

        return jsonify({
            'success': True,
            'items': items
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Inventory Report API
@app.route('/api/inventory-report')
@manager_required
def inventory_report():
    try:
        report = inventory.get_inventory_report()
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Cashier Daily Sales Report API
@app.route('/api/cashier-daily-sales')
@login_required
def cashier_daily_sales():
    try:
        today = datetime.now().date()
        conn = db.get_connection()
        cursor = conn.cursor()

        # Today's sales summary
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM sales
            WHERE DATE(sale_date) = ?
        """, (today,))
        total_count, total_revenue = cursor.fetchone()

        # Payment method breakdown
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
                COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
            FROM sales
            WHERE DATE(sale_date) = ?
        """, (today,))
        cash_total, ecocash_total = cursor.fetchone()

        # My sales today
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM sales
            WHERE DATE(sale_date) = ? AND cashier_id = ?
        """, (today, session.get('user_id')))
        my_count, my_revenue = cursor.fetchone()

        # My payment method breakdown
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END), 0) as cash_total,
                COALESCE(SUM(CASE WHEN payment_method = 'ecocash' THEN total_amount ELSE 0 END), 0) as ecocash_total
            FROM sales
            WHERE DATE(sale_date) = ? AND cashier_id = ?
        """, (today, session.get('user_id')))
        my_cash_total, my_ecocash_total = cursor.fetchone()

        # Average sale
        avg_sale = total_revenue / total_count if total_count > 0 else 0

        # All sales today with cashier info
        cursor.execute("""
            SELECT s.id, s.total_amount, s.sale_date, u.full_name, COUNT(si.id) as item_count, s.payment_method
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN users u ON s.cashier_id = u.id
            WHERE DATE(s.sale_date) = ?
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """, (today,))
        sales_data = cursor.fetchall()

        conn.close()

        all_sales = []
        for sale in sales_data:
            sale_time = datetime.fromisoformat(sale[2])
            all_sales.append({
                'id': sale[0],
                'total': sale[1],
                'time': sale_time.strftime('%I:%M %p'),
                'cashier': sale[3],
                'items': sale[4],
                'payment_method': sale[5] or 'cash'
            })

        report = {
            'total_sales': total_count,
            'total_revenue': total_revenue,
            'cash_total': cash_total,
            'ecocash_total': ecocash_total,
            'my_sales': my_count,
            'my_revenue': my_revenue,
            'my_cash_total': my_cash_total,
            'my_ecocash_total': my_ecocash_total,
            'avg_sale': avg_sale,
            'all_sales': all_sales
        }

        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    # Run on network-accessible address for multiple workstations
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
