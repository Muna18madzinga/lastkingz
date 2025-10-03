import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
import sqlite3

class SalesReportWindow:
    """Sales Reports Interface"""

    def __init__(self, parent, db: Database):
        self.window = tk.Toplevel(parent)
        self.window.title("Sales Reports")
        self.window.geometry("900x700")
        self.db = db

        self.setup_ui()
        self.load_today_report()

    def setup_ui(self):
        """Setup the UI"""
        # Title
        title_frame = tk.Frame(self.window, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Sales Reports", font=("Arial", 18, "bold"),
                bg="#2c3e50", fg="white").pack(pady=15)

        # Filter Frame
        filter_frame = tk.LabelFrame(self.window, text="Report Period", font=("Arial", 12, "bold"))
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(filter_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Today", command=self.load_today_report,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Yesterday", command=self.load_yesterday_report,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="This Week", command=self.load_week_report,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="This Month", command=self.load_month_report,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="All Time", command=self.load_all_time_report,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Summary Frame
        summary_frame = tk.LabelFrame(self.window, text="Summary", font=("Arial", 12, "bold"))
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        self.summary_text = tk.Text(summary_frame, height=8, font=("Arial", 11), bg="#ecf0f1")
        self.summary_text.pack(fill=tk.X, padx=10, pady=10)

        # Sales Table
        table_frame = tk.LabelFrame(self.window, text="Sales Transactions", font=("Arial", 12, "bold"))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Sale ID", "Date/Time", "Total", "Cash", "Change", "Items")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Sale ID", width=80)
        self.tree.column("Date/Time", width=180)
        self.tree.column("Total", width=100)
        self.tree.column("Cash", width=100)
        self.tree.column("Change", width=100)
        self.tree.column("Items", width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Double-click to view details
        self.tree.bind("<Double-1>", lambda e: self.view_sale_details())

    def load_report(self, start_date: str, end_date: str, title: str):
        """Load report for date range"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get summary
        summary = self.db.get_sales_report(start_date, end_date)

        # Get individual sales
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.sale_date, s.total_amount, s.cash_received, s.change_given,
                   COUNT(si.id) as item_count
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            WHERE date(s.sale_date) BETWEEN ? AND ?
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        ''', (start_date, end_date))
        sales = cursor.fetchall()
        conn.close()

        # Display summary
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, f"═══ {title} ═══\n\n", "title")
        self.summary_text.insert(tk.END, f"Total Sales:        {summary['total_sales']}\n", "bold")
        self.summary_text.insert(tk.END, f"Total Revenue:      ${summary['total_revenue']:.2f}\n", "bold")
        self.summary_text.insert(tk.END, f"Average Sale:       ${(summary['total_revenue'] / summary['total_sales'] if summary['total_sales'] > 0 else 0):.2f}\n")
        self.summary_text.insert(tk.END, f"Cash Collected:     ${summary['total_cash']:.2f}\n")
        self.summary_text.insert(tk.END, f"Change Given:       ${summary['total_change']:.2f}\n")

        self.summary_text.tag_config("title", font=("Arial", 12, "bold"), foreground="#2c3e50")
        self.summary_text.tag_config("bold", font=("Arial", 11, "bold"))

        # Display sales
        for sale in sales:
            self.tree.insert("", tk.END, values=(
                sale[0],
                sale[1],
                f"${sale[2]:.2f}",
                f"${sale[3]:.2f}",
                f"${sale[4]:.2f}",
                sale[5]
            ))

    def load_today_report(self):
        """Load today's report"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.load_report(today, today, "Today's Sales")

    def load_yesterday_report(self):
        """Load yesterday's report"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.load_report(yesterday, yesterday, "Yesterday's Sales")

    def load_week_report(self):
        """Load this week's report"""
        today = datetime.now()
        start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
        self.load_report(start, end, "This Week's Sales")

    def load_month_report(self):
        """Load this month's report"""
        today = datetime.now()
        start = today.replace(day=1).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
        self.load_report(start, end, "This Month's Sales")

    def load_all_time_report(self):
        """Load all-time report"""
        self.load_report("2000-01-01", "2099-12-31", "All Time Sales")

    def view_sale_details(self):
        """View details of selected sale"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        sale_id = item['values'][0]

        # Get sale items
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT product_name, quantity, unit_price, subtotal
            FROM sale_items
            WHERE sale_id = ?
        ''', (sale_id,))
        items = cursor.fetchall()
        conn.close()

        # Show details dialog
        details = f"Sale #{sale_id} - Details\n\n"
        details += f"{'Item':<30} {'Qty':<5} {'Price':<10} {'Subtotal':<10}\n"
        details += "=" * 60 + "\n"
        for item in items:
            details += f"{item[0]:<30} {item[1]:<5} ${item[2]:<9.2f} ${item[3]:<9.2f}\n"

        messagebox.showinfo(f"Sale #{sale_id} Details", details)