import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database

class ProductManagerWindow:
    """Product Management Interface"""

    def __init__(self, parent, db: Database):
        self.window = tk.Toplevel(parent)
        self.window.title("Product Management")
        self.window.geometry("900x600")
        self.db = db

        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        """Setup the UI"""
        # Title
        title_frame = tk.Frame(self.window, bg="#34495e", height=60)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Product Management", font=("Arial", 18, "bold"),
                bg="#34495e", fg="white").pack(pady=15)

        # Toolbar
        toolbar = tk.Frame(self.window)
        toolbar.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(toolbar, text="Add Product", command=self.add_product,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Edit Product", command=self.edit_product,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Delete Product", command=self.delete_product,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Refresh", command=self.load_products,
                 bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        # Products Table
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Barcode", "Name", "Price", "Stock", "Low Stock Alert")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        # Column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Low Stock Alert", text="Low Stock Alert")

        # Column widths
        self.tree.column("ID", width=50)
        self.tree.column("Barcode", width=120)
        self.tree.column("Name", width=250)
        self.tree.column("Price", width=80)
        self.tree.column("Stock", width=80)
        self.tree.column("Low Stock Alert", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Double-click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_product())

    def load_products(self):
        """Load products from database"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load products
        products = self.db.get_all_products()
        for product in products:
            # Highlight low stock items
            tag = "low_stock" if product['stock'] <= product['low_stock_threshold'] else ""
            self.tree.insert("", tk.END, values=(
                product['id'],
                product['barcode'],
                product['name'],
                f"${product['price']:.2f}",
                product['stock'],
                product['low_stock_threshold']
            ), tags=(tag,))

        # Configure tags
        self.tree.tag_configure("low_stock", background="#ffcccc")

    def add_product(self):
        """Add new product"""
        dialog = ProductDialog(self.window, self.db, mode="add")
        self.window.wait_window(dialog.window)
        self.load_products()

    def edit_product(self):
        """Edit selected product"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to edit")
            return

        item = self.tree.item(selection[0])
        product_id = item['values'][0]

        # Get product from database
        products = [p for p in self.db.get_all_products() if p['id'] == product_id]
        if products:
            dialog = ProductDialog(self.window, self.db, mode="edit", product=products[0])
            self.window.wait_window(dialog.window)
            self.load_products()

    def delete_product(self):
        """Delete selected product"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to delete")
            return

        item = self.tree.item(selection[0])
        product_name = item['values'][2]
        product_id = item['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            self.db.delete_product(product_id)
            self.load_products()
            messagebox.showinfo("Success", "Product deleted successfully")


class ProductDialog:
    """Dialog for adding/editing products"""

    def __init__(self, parent, db: Database, mode="add", product=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Add Product" if mode == "add" else "Edit Product")
        self.window.geometry("400x350")
        self.window.transient(parent)
        self.window.grab_set()

        self.db = db
        self.mode = mode
        self.product = product

        self.barcode_var = tk.StringVar(value=product['barcode'] if product else "")
        self.name_var = tk.StringVar(value=product['name'] if product else "")
        self.price_var = tk.StringVar(value=str(product['price']) if product else "")
        self.stock_var = tk.StringVar(value=str(product['stock']) if product else "")
        self.threshold_var = tk.StringVar(value=str(product['low_stock_threshold']) if product else "10")

        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI"""
        # Form
        form_frame = tk.Frame(self.window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Barcode
        tk.Label(form_frame, text="Barcode:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        barcode_entry = tk.Entry(form_frame, textvariable=self.barcode_var, font=("Arial", 10), width=30)
        barcode_entry.grid(row=0, column=1, pady=5)
        if self.mode == "edit":
            barcode_entry.config(state='disabled')  # Can't change barcode

        # Name
        tk.Label(form_frame, text="Product Name:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.name_var, font=("Arial", 10), width=30).grid(row=1, column=1, pady=5)

        # Price
        tk.Label(form_frame, text="Price ($):", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.price_var, font=("Arial", 10), width=30).grid(row=2, column=1, pady=5)

        # Stock
        tk.Label(form_frame, text="Stock Quantity:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.stock_var, font=("Arial", 10), width=30).grid(row=3, column=1, pady=5)

        # Low Stock Threshold
        tk.Label(form_frame, text="Low Stock Alert:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.threshold_var, font=("Arial", 10), width=30).grid(row=4, column=1, pady=5)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(button_frame, text="Save", command=self.save,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy,
                 bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=10).pack(side=tk.LEFT, padx=5)

    def save(self):
        """Save product"""
        # Validate
        barcode = self.barcode_var.get().strip()
        name = self.name_var.get().strip()
        price_str = self.price_var.get().strip()
        stock_str = self.stock_var.get().strip()
        threshold_str = self.threshold_var.get().strip()

        if not all([barcode, name, price_str, stock_str, threshold_str]):
            messagebox.showerror("Validation Error", "All fields are required")
            return

        try:
            price = float(price_str)
            stock = int(stock_str)
            threshold = int(threshold_str)

            if price <= 0:
                raise ValueError("Price must be positive")
            if stock < 0:
                raise ValueError("Stock cannot be negative")
            if threshold < 0:
                raise ValueError("Threshold cannot be negative")

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return

        # Save
        if self.mode == "add":
            success, message = self.db.add_product(barcode, name, price, stock, threshold)
            if success:
                messagebox.showinfo("Success", "Product added successfully")
                self.window.destroy()
            else:
                messagebox.showerror("Error", message)
        else:
            self.db.update_product(self.product['id'], name, price, stock, threshold)
            messagebox.showinfo("Success", "Product updated successfully")
            self.window.destroy()