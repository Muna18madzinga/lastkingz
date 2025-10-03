import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from datetime import datetime
from database import Database
from barcode_scanner import BarcodeScanner
from shopping_cart import ShoppingCart
from receipt_printer import ReceiptPrinter
from inventory_manager import InventoryManager
from product_manager_ui import ProductManagerWindow
from sales_report_ui import SalesReportWindow
from user_auth import UserAuth
from quick_sale import QuickSaleManager

class POSSystem:
    """Main POS System GUI for LastKings Liquor Store"""

    def __init__(self, root):
        self.root = root
        self.root.title("LastKings Liquor Store - POS System")

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set to 95% of screen size to ensure fit
        window_width = int(screen_width * 0.95)
        window_height = int(screen_height * 0.92)

        self.root.geometry(f"{window_width}x{window_height}+0+0")
        self.root.configure(bg="#f8fafc")

        # Modern flat minimalist color scheme (Indigo/Teal palette)
        self.colors = {
            'primary': '#4f46e5',      # Indigo
            'primary_hover': '#4338ca',# Darker indigo
            'secondary': '#14b8a6',    # Teal
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#3b82f6',         # Blue
            'dark': '#1e293b',         # Slate dark
            'text': '#1e293b',         # Slate dark
            'text_light': '#64748b',   # Slate gray
            'bg': '#f8fafc',           # Very light gray background
            'white': '#ffffff',
            'light': '#f1f5f9',        # Light slate
            'border': '#e2e8f0',       # Border gray
            'shadow': 'rgba(15, 23, 42, 0.08)',  # Soft shadow
            'card': '#ffffff',         # Card white
            'hover': '#f1f5f9'         # Hover state
        }

        # Initialize components
        self.db = Database()
        self.auth = UserAuth()
        self.scanner = BarcodeScanner()
        self.cart = ShoppingCart()
        self.printer = None  # Will be initialized after UI setup
        self.inventory = InventoryManager(self.db)
        self.quick_sale = QuickSaleManager()
        self.selected_printer = tk.StringVar()

        # User session
        self.current_user = None

        # Variables
        self.barcode_var = tk.StringVar()
        self.total_var = tk.StringVar(value="$0.00")
        self.cash_var = tk.StringVar()
        self.change_var = tk.StringVar(value="$0.00")
        self.current_view = "dashboard"  # dashboard or pos

        # Setup modern ttk style
        self.setup_styles()

        # Show login first
        self.show_login()

    def show_login(self):
        """Show login screen - Modern UI inspired by PyQt6 design"""
        # Create login window
        login_window = tk.Toplevel(self.root)
        login_window.title("Sign In — Modern UI")
        login_window.geometry("420x540")

        # Gradient background simulation
        login_window.configure(bg='#eef2f7')
        login_window.transient(self.root)
        login_window.grab_set()

        # Center the window
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - (420 // 2)
        y = (login_window.winfo_screenheight() // 2) - (540 // 2)
        login_window.geometry(f"420x540+{x}+{y}")

        # Prevent closing
        login_window.protocol("WM_DELETE_WINDOW", lambda: None)

        # Main container
        main_container = tk.Frame(login_window, bg='#eef2f7')
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Card container - white with shadow effect
        card = tk.Frame(main_container, bg='white', relief=tk.FLAT, bd=0,
                       highlightthickness=1, highlightbackground='#d0d5dd')
        card.pack(expand=True, fill=tk.BOTH)

        # Inner padding
        inner = tk.Frame(card, bg='white')
        inner.pack(padx=24, pady=24, fill=tk.BOTH, expand=True)

        # Header
        tk.Label(inner, text="Welcome back",
                font=("Segoe UI", 20, "bold"),
                bg='white',
                fg='#222222').pack(anchor=tk.W, pady=(0, 2))

        tk.Label(inner, text="Sign in to continue",
                font=("Segoe UI", 10),
                bg='white',
                fg='#6b7280').pack(anchor=tk.W, pady=(0, 20))

        # Username/Email field
        username_var = tk.StringVar()
        username_entry = tk.Entry(inner, textvariable=username_var,
                                  font=("Segoe UI", 11),
                                  relief=tk.FLAT,
                                  bg='#fbfbfd',
                                  fg='#222222',
                                  bd=0,
                                  highlightthickness=1,
                                  highlightbackground='#e6e9ee',
                                  highlightcolor='#6c8cff')
        username_entry.pack(fill=tk.X, pady=(0, 4), ipady=10, padx=1)
        username_entry.insert(0, "Email or username")
        username_entry.config(fg='#9ca3af')
        username_entry.focus()

        # Username error
        err_user = tk.Label(inner, text="", font=("Segoe UI", 9),
                           bg='white', fg='#d9534f')
        err_user.pack(anchor=tk.W, pady=(0, 8))

        # Password field
        password_var = tk.StringVar()
        password_frame = tk.Frame(inner, bg='white')
        password_frame.pack(fill=tk.X, pady=(0, 4))

        password_entry = tk.Entry(password_frame, textvariable=password_var,
                                 font=("Segoe UI", 11),
                                 show="●",
                                 relief=tk.FLAT,
                                 bg='#fbfbfd',
                                 fg='#222222',
                                 bd=0,
                                 highlightthickness=1,
                                 highlightbackground='#e6e9ee',
                                 highlightcolor='#6c8cff')
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=1)
        password_entry.insert(0, "Password")
        password_entry.config(fg='#9ca3af', show="")

        # Toggle password visibility
        show_pwd_var = tk.BooleanVar(value=False)
        toggle_btn = tk.Button(password_frame, text="👁",
                              font=("Segoe UI", 12),
                              bg='#fbfbfd',
                              fg='#6b7280',
                              relief=tk.FLAT,
                              bd=0,
                              cursor="hand2",
                              width=3)
        toggle_btn.pack(side=tk.RIGHT, padx=(2, 1))

        def toggle_password():
            if show_pwd_var.get():
                password_entry.config(show="●")
                show_pwd_var.set(False)
            else:
                password_entry.config(show="")
                show_pwd_var.set(True)

        toggle_btn.config(command=toggle_password)

        # Password error
        err_pwd = tk.Label(inner, text="", font=("Segoe UI", 9),
                          bg='white', fg='#d9534f')
        err_pwd.pack(anchor=tk.W, pady=(0, 8))

        # Focus handlers for placeholders
        def on_username_focus_in(event):
            if username_entry.get() == "Email or username":
                username_entry.delete(0, tk.END)
                username_entry.config(fg='#222222')

        def on_username_focus_out(event):
            if username_entry.get() == "":
                username_entry.insert(0, "Email or username")
                username_entry.config(fg='#9ca3af')
            validate_form()

        def on_password_focus_in(event):
            if password_entry.get() == "Password":
                password_entry.delete(0, tk.END)
                password_entry.config(fg='#222222', show="●")

        def on_password_focus_out(event):
            if password_entry.get() == "":
                password_entry.insert(0, "Password")
                password_entry.config(fg='#9ca3af', show="")
            validate_form()

        username_entry.bind('<FocusIn>', on_username_focus_in)
        username_entry.bind('<FocusOut>', on_username_focus_out)
        password_entry.bind('<FocusIn>', on_password_focus_in)
        password_entry.bind('<FocusOut>', on_password_focus_out)

        # Options row
        opts_frame = tk.Frame(inner, bg='white')
        opts_frame.pack(fill=tk.X, pady=(0, 16))

        remember_var = tk.BooleanVar()
        tk.Checkbutton(opts_frame, text="Remember me", variable=remember_var,
                      bg='white', fg='#334155',
                      font=("Segoe UI", 9),
                      activebackground='white',
                      selectcolor='white').pack(side=tk.LEFT)

        forgot_link = tk.Label(opts_frame, text="Forgot password?",
                              font=("Segoe UI", 9, "underline"),
                              bg='white', fg='#4266ff',
                              cursor="hand2")
        forgot_link.pack(side=tk.RIGHT)

        # Status label
        status_label = tk.Label(inner, text="", font=("Segoe UI", 10, "bold"),
                               bg='white', fg='#0b8457')

        # Sign In button
        signin_btn = tk.Button(inner, text="Sign In",
                              font=("Segoe UI", 11, "bold"),
                              bg='#5b8cff',
                              fg='white',
                              relief=tk.FLAT,
                              bd=0,
                              cursor="hand2",
                              activebackground='#4266ff',
                              state=tk.DISABLED)
        signin_btn.pack(fill=tk.X, ipady=12, pady=(0, 12))

        # Form validation
        def validate_form(*args):
            user = username_entry.get().strip()
            pwd = password_entry.get().strip()

            user_ok = user and user != "Email or username" and len(user) >= 3
            pwd_ok = pwd and pwd != "Password" and len(pwd) >= 8

            if user and user != "Email or username":
                if len(user) < 3:
                    err_user.config(text="Username must be at least 3 characters.")
                else:
                    err_user.config(text="")

            if pwd and pwd != "Password":
                if len(pwd) < 8:
                    err_pwd.config(text="Password must be at least 8 characters.")
                else:
                    err_pwd.config(text="")

            if user_ok and pwd_ok:
                signin_btn.config(state=tk.NORMAL, bg='#5b8cff')
            else:
                signin_btn.config(state=tk.DISABLED, bg='#dfe7ff')

        username_var.trace('w', validate_form)
        password_var.trace('w', validate_form)

        def attempt_login(event=None):
            username = username_var.get().strip()
            password = password_var.get().strip()

            if username == "Email or username" or username == "":
                return
            if password == "Password" or password == "":
                return

            # Disable button and show status
            signin_btn.config(state=tk.DISABLED, bg='#dfe7ff')
            status_label.config(text="Authenticating…", fg='#6b7280')
            status_label.pack(pady=(0, 8))
            login_window.update()

            # Simulate authentication delay
            login_window.after(600, lambda: finish_login(username, password))

        def finish_login(username, password):
            user = self.auth.authenticate(username, password)
            if user:
                status_label.config(text="Signed in successfully ✅", fg='#0b8457')
                login_window.update()
                login_window.after(400, lambda: [
                    setattr(self, 'current_user', user),
                    login_window.destroy(),
                    self.init_main_ui()
                ])
            else:
                status_label.config(text="Authentication failed — wrong credentials.", fg='#d9534f')
                signin_btn.config(state=tk.NORMAL, bg='#5b8cff')

        signin_btn.config(command=attempt_login)

        # Hover effects
        def on_btn_enter(e):
            if signin_btn['state'] == tk.NORMAL:
                signin_btn['bg'] = '#4266ff'
        def on_btn_leave(e):
            if signin_btn['state'] == tk.NORMAL:
                signin_btn['bg'] = '#5b8cff'
        signin_btn.bind("<Enter>", on_btn_enter)
        signin_btn.bind("<Leave>", on_btn_leave)

        # Footer
        footer = tk.Label(inner, text="Default: manager/manager123 or cashier/cashier123",
                         font=("Segoe UI", 8),
                         bg='white', fg='#9ca3af')
        footer.pack(pady=(12, 0))

        # Bind enter key
        password_entry.bind('<Return>', attempt_login)
        username_entry.bind('<Return>', lambda e: password_entry.focus())


    def init_main_ui(self):
        """Initialize main UI after login"""
        # Setup UI
        self.setup_menu()
        self.setup_main_container()
        self.show_dashboard()

        # Initialize printer with selected or default printer
        self.initialize_printer()

        # Bind barcode scanner
        self.root.bind('<Return>', self.on_barcode_scan)

    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Treeview
        style.configure("Treeview",
                       background=self.colors['white'],
                       foreground=self.colors['text'],
                       rowheight=35,
                       fieldbackground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        style.map('Treeview', background=[('selected', self.colors['secondary'])])
        style.map('Treeview.Heading', background=[('active', self.colors['hover'])])

    def is_manager(self):
        """Check if current user is manager"""
        return self.current_user and self.current_user['role'] == UserAuth.ROLE_MANAGER

    def is_cashier(self):
        """Check if current user is cashier"""
        return self.current_user and self.current_user['role'] == UserAuth.ROLE_CASHIER

    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # User menu
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=f"👤 {self.current_user['full_name']} ({self.current_user['role'].title()})", menu=user_menu)
        user_menu.add_command(label="Logout", command=self.logout)
        user_menu.add_separator()
        user_menu.add_command(label="Exit", command=self.root.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dashboard", command=self.show_dashboard)
        view_menu.add_command(label="POS Terminal", command=self.show_pos)

        # Products menu (Manager only can manage, cashier can view)
        products_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=products_menu)

        if self.is_manager():
            products_menu.add_command(label="Manage Products", command=self.open_product_manager)
        else:
            products_menu.add_command(label="Manage Products", command=self.request_manager_approval,
                                     state=tk.DISABLED)

        products_menu.add_command(label="View Inventory Report", command=self.view_inventory_report)

        # Sales menu (Both can view, only manager can access detailed reports)
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sales", menu=sales_menu)

        if self.is_manager():
            sales_menu.add_command(label="View Sales Reports", command=self.open_sales_reports)
        else:
            sales_menu.add_command(label="View Sales Reports", command=self.open_sales_reports)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Select Printer", command=self.select_printer)
        tools_menu.add_command(label="Check Printer Status", command=self.check_printer_status)
        tools_menu.add_command(label="Print Test Receipt", command=self.print_test_receipt)
        tools_menu.add_separator()
        tools_menu.add_command(label="Open Cash Drawer", command=self.open_cash_drawer_manual)

        if self.is_manager():
            tools_menu.add_separator()
            tools_menu.add_command(label="Manage Quick Sale Items", command=self.manage_quick_sale_items)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_main_container(self):
        """Setup main container with modern slim navbar"""
        # Modern Slim Navbar
        navbar = tk.Frame(self.root, bg=self.colors['white'], height=60)
        navbar.pack(fill=tk.X)
        navbar.pack_propagate(False)

        # Add subtle shadow effect with a thin line
        tk.Frame(self.root, bg=self.colors['border'], height=1).pack(fill=tk.X)

        nav_inner = tk.Frame(navbar, bg=self.colors['white'])
        nav_inner.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Left side - Store branding
        brand_frame = tk.Frame(nav_inner, bg=self.colors['white'])
        brand_frame.pack(side=tk.LEFT)

        tk.Label(brand_frame, text="👑",
                font=("Segoe UI", 24),
                bg=self.colors['white']).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(brand_frame, text="LastKings",
                font=("Inter", 16, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)

        # Right side - Navigation links
        nav_links = tk.Frame(nav_inner, bg=self.colors['white'])
        nav_links.pack(side=tk.RIGHT)

        # Dashboard button
        self.nav_dashboard_btn = tk.Button(nav_links, text="📊  Dashboard",
                                          command=self.show_dashboard,
                                          bg=self.colors['light'],
                                          fg=self.colors['text'],
                                          font=("Inter", 10, "bold"),
                                          relief=tk.FLAT,
                                          bd=0,
                                          cursor="hand2",
                                          padx=16, pady=8)
        self.nav_dashboard_btn.pack(side=tk.LEFT, padx=4)

        # POS button
        self.nav_pos_btn = tk.Button(nav_links, text="🛒  POS Terminal",
                                     command=self.show_pos,
                                     bg=self.colors['white'],
                                     fg=self.colors['text'],
                                     font=("Inter", 10, "bold"),
                                     relief=tk.FLAT,
                                     bd=0,
                                     cursor="hand2",
                                     padx=16, pady=8)
        self.nav_pos_btn.pack(side=tk.LEFT, padx=4)

        # User info
        user_label = tk.Label(nav_links,
                             text=f"👤 {self.current_user['full_name']} ({self.current_user['role'].title()})",
                             font=("Inter", 9),
                             bg=self.colors['white'],
                             fg=self.colors['text_light'])
        user_label.pack(side=tk.LEFT, padx=16)

        # Main content container with background
        self.content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Modern minimal status bar
        status_frame = tk.Frame(self.root, bg=self.colors['white'], height=32)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)

        tk.Frame(self.root, bg=self.colors['border'], height=1).pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = tk.Label(status_frame,
                                   text="● Ready",
                                   bg=self.colors['white'],
                                   fg=self.colors['text_light'],
                                   font=("Inter", 9),
                                   anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=16)

        # Printer status indicator
        self.printer_status = tk.Label(status_frame,
                                      bg=self.colors['white'],
                                      fg=self.colors['text_light'],
                                      font=("Inter", 9),
                                      anchor=tk.E)
        self.printer_status.pack(side=tk.RIGHT, padx=16)

    def show_dashboard(self):
        """Show dashboard view"""
        self.current_view = "dashboard"
        self.nav_dashboard_btn.config(bg=self.colors['light'], fg=self.colors['primary'])
        self.nav_pos_btn.config(bg=self.colors['white'], fg=self.colors['text'])

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create dashboard
        self.setup_dashboard()
        self.status_bar.config(text="● Dashboard View")

    def show_pos(self):
        """Show POS terminal view"""
        self.current_view = "pos"
        self.nav_dashboard_btn.config(bg=self.colors['white'], fg=self.colors['text'])
        self.nav_pos_btn.config(bg=self.colors['light'], fg=self.colors['primary'])

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create POS UI
        self.setup_pos_ui()
        self.status_bar.config(text="● POS Terminal - Ready to scan")

    def setup_dashboard(self):
        """Setup stunning dashboard with statistics"""
        # Main Container with padding
        main_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Get statistics
        stats = self.get_dashboard_stats()

        # Top row - Statistics cards
        stats_frame = tk.Frame(main_frame, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        # Sales Today Card
        self.create_stat_card(stats_frame, "💰 Today's Sales",
                             f"${stats['today_sales']:.2f}",
                             f"{stats['today_transactions']} transactions",
                             self.colors['success'], 0, 0)

        # Sales This Week Card
        self.create_stat_card(stats_frame, "📈 This Week",
                             f"${stats['week_sales']:.2f}",
                             f"{stats['week_transactions']} transactions",
                             self.colors['info'], 0, 1)

        # Low Stock Card
        self.create_stat_card(stats_frame, "⚠️ Low Stock Items",
                             str(stats['low_stock_count']),
                             "items need restock",
                             self.colors['warning'], 0, 2)

        # Total Products Card
        self.create_stat_card(stats_frame, "📦 Total Products",
                             str(stats['total_products']),
                             f"${stats['inventory_value']:.2f} value",
                             self.colors['primary'], 0, 3)

        # Middle section - Two columns
        middle_frame = tk.Frame(main_frame, bg=self.colors['light'])
        middle_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Recent Sales
        left_col = tk.Frame(middle_frame, bg=self.colors['white'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_col, text="📋 Recent Sales",
                font=("Segoe UI", 16, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(padx=20, pady=(20, 15), anchor=tk.W)

        # Recent sales list
        sales_list_frame = tk.Frame(left_col, bg=self.colors['white'])
        sales_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Time", "Amount", "Items")
        sales_tree = ttk.Treeview(sales_list_frame, columns=columns, show="headings", height=10)

        for col in columns:
            sales_tree.heading(col, text=col)
            if col == "ID":
                sales_tree.column(col, width=60, anchor=tk.CENTER)
            elif col == "Time":
                sales_tree.column(col, width=150)
            elif col == "Amount":
                sales_tree.column(col, width=100, anchor=tk.E)
            else:
                sales_tree.column(col, width=80, anchor=tk.CENTER)

        # Populate recent sales
        for sale in stats['recent_sales']:
            sales_tree.insert("", tk.END, values=(
                f"#{sale['id']}",
                sale['date'],
                f"${sale['total']:.2f}",
                sale['items_count']
            ))

        sales_tree.pack(fill=tk.BOTH, expand=True)

        # Right column - Low Stock & Quick Actions
        right_col = tk.Frame(middle_frame, bg=self.colors['light'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Quick Actions Card
        actions_card = tk.Frame(right_col, bg=self.colors['white'])
        actions_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(actions_card, text="⚡ Quick Actions",
                font=("Segoe UI", 16, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(padx=20, pady=(20, 15), anchor=tk.W)

        actions_frame = tk.Frame(actions_card, bg=self.colors['white'])
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.create_modern_button(actions_frame, "🛒 Start New Sale", self.show_pos,
                                 self.colors['primary'], fill=tk.X, pady=(0, 10))

        # Manager-only or require approval
        if self.is_manager():
            self.create_modern_button(actions_frame, "📦 Manage Products", self.open_product_manager,
                                     self.colors['info'], fill=tk.X, pady=(0, 10))
        else:
            self.create_modern_button(actions_frame, "📦 Manage Products (Needs Approval)", self.request_manager_approval,
                                     self.colors['text_light'], fill=tk.X, pady=(0, 10))

        self.create_modern_button(actions_frame, "📊 View Reports", self.open_sales_reports,
                                 self.colors['secondary'], fill=tk.X, pady=(0, 10))
        self.create_modern_button(actions_frame, "🖨️ Select Printer", self.select_printer,
                                 self.colors['success'], fill=tk.X)

        # Low Stock Items Card
        low_stock_card = tk.Frame(right_col, bg=self.colors['white'])
        low_stock_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(low_stock_card, text="📉 Low Stock Alert",
                font=("Segoe UI", 16, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(padx=20, pady=(20, 15), anchor=tk.W)

        low_stock_frame = tk.Frame(low_stock_card, bg=self.colors['white'])
        low_stock_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        if stats['low_stock_items']:
            for item in stats['low_stock_items'][:5]:  # Show top 5
                item_frame = tk.Frame(low_stock_frame, bg=self.colors['light'])
                item_frame.pack(fill=tk.X, pady=5)

                tk.Label(item_frame, text=item['name'][:25],
                        font=("Segoe UI", 10, "bold"),
                        bg=self.colors['light'],
                        fg=self.colors['text']).pack(side=tk.LEFT, padx=10, pady=8)

                tk.Label(item_frame, text=f"{item['stock']} left",
                        font=("Segoe UI", 10),
                        bg=self.colors['danger'],
                        fg=self.colors['white'],
                        padx=10, pady=5).pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(low_stock_frame, text="✓ All items well stocked!",
                    font=("Segoe UI", 11),
                    bg=self.colors['white'],
                    fg=self.colors['success']).pack(pady=20)

    def create_stat_card(self, parent, title, value, subtitle, color, row, col):
        """Create a modern statistics card"""
        card = tk.Frame(parent, bg=color, relief=tk.FLAT, bd=0)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title,
                font=("Segoe UI", 12),
                bg=color,
                fg=self.colors['white']).pack(pady=(20, 5), padx=20, anchor=tk.W)

        tk.Label(card, text=value,
                font=("Segoe UI", 32, "bold"),
                bg=color,
                fg=self.colors['white']).pack(padx=20, anchor=tk.W)

        tk.Label(card, text=subtitle,
                font=("Segoe UI", 10),
                bg=color,
                fg=self.colors['white']).pack(pady=(0, 20), padx=20, anchor=tk.W)

    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        from datetime import datetime, timedelta

        today = datetime.now().date()
        week_ago = today - timedelta(days=7)

        # Get sales data
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Today's sales
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM sales
            WHERE DATE(sale_date) = ?
        """, (today,))
        today_trans, today_sales = cursor.fetchone()

        # Week's sales
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM sales
            WHERE DATE(sale_date) >= ?
        """, (week_ago,))
        week_trans, week_sales = cursor.fetchone()

        # Recent sales
        cursor.execute("""
            SELECT id, sale_date, total_amount,
                   (SELECT COUNT(*) FROM sale_items WHERE sale_id = sales.id) as items_count
            FROM sales
            ORDER BY sale_date DESC
            LIMIT 10
        """)
        recent_sales = [{'id': r[0], 'date': r[1], 'total': r[2], 'items_count': r[3]}
                       for r in cursor.fetchall()]

        # Inventory stats
        report = self.inventory.get_inventory_report()

        return {
            'today_sales': today_sales or 0,
            'today_transactions': today_trans or 0,
            'week_sales': week_sales or 0,
            'week_transactions': week_trans or 0,
            'total_products': report['total_products'],
            'low_stock_count': report['low_stock_count'],
            'inventory_value': report['total_inventory_value'],
            'low_stock_items': report['low_stock_items'],
            'recent_sales': recent_sales
        }

    def setup_pos_ui(self):
        """Setup modern POS terminal interface with dashboard-style layout"""
        # Main Container with modern background
        main_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Column - Cart + Quick Sale
        left_column = tk.Frame(main_frame, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        # Cart Section (Modern Card with shadow) - Top
        cart_card = tk.Frame(left_column, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                           highlightthickness=1, highlightbackground=self.colors['border'])
        cart_card.pack(fill=tk.X, pady=(0, 16))

        # Cart Header with icon
        cart_header = tk.Frame(cart_card, bg=self.colors['card'])
        cart_header.pack(fill=tk.X, padx=20, pady=(16, 8))

        tk.Label(cart_header, text="🛒",
                font=("Segoe UI", 18),
                bg=self.colors['card']).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(cart_header, text="Shopping Cart",
                font=("Inter", 14, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(side=tk.LEFT, anchor=tk.W)

        # Cart Tree with modern styling (minimal height)
        cart_frame = tk.Frame(cart_card, bg=self.colors['white'])
        cart_frame.pack(fill=tk.X, padx=15, pady=3)

        columns = ("Item", "Qty", "Price", "Subtotal")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=5)

        for col in columns:
            self.cart_tree.heading(col, text=col)
            if col == "Item":
                self.cart_tree.column(col, width=200)
            else:
                self.cart_tree.column(col, width=80, anchor=tk.CENTER)

        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.config(yscrollcommand=scrollbar.set)

        # Cart Buttons (Modern outlined style)
        button_frame = tk.Frame(cart_card, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, padx=20, pady=(8, 16))

        # Remove button (outlined danger)
        remove_btn = tk.Button(button_frame, text="🗑️  Remove",
                              command=self.remove_item,
                              bg=self.colors['card'],
                              fg=self.colors['danger'],
                              font=("Inter", 10, "bold"),
                              relief=tk.FLAT,
                              bd=0,
                              cursor="hand2",
                              highlightthickness=1,
                              highlightbackground=self.colors['danger'])
        remove_btn.pack(side=tk.LEFT, padx=(0, 8), ipady=8, ipadx=16)

        def on_remove_enter(e):
            remove_btn['bg'] = self.colors['danger']
            remove_btn['fg'] = self.colors['white']
        def on_remove_leave(e):
            remove_btn['bg'] = self.colors['card']
            remove_btn['fg'] = self.colors['danger']
        remove_btn.bind("<Enter>", on_remove_enter)
        remove_btn.bind("<Leave>", on_remove_leave)

        # Clear button (outlined warning)
        clear_btn = tk.Button(button_frame, text="🧹  Clear All",
                             command=self.clear_cart,
                             bg=self.colors['card'],
                             fg=self.colors['warning'],
                             font=("Inter", 10, "bold"),
                             relief=tk.FLAT,
                             bd=0,
                             cursor="hand2",
                             highlightthickness=1,
                             highlightbackground=self.colors['warning'])
        clear_btn.pack(side=tk.LEFT, ipady=8, ipadx=16)

        def on_clear_enter(e):
            clear_btn['bg'] = self.colors['warning']
            clear_btn['fg'] = self.colors['white']
        def on_clear_leave(e):
            clear_btn['bg'] = self.colors['card']
            clear_btn['fg'] = self.colors['warning']
        clear_btn.bind("<Enter>", on_clear_enter)
        clear_btn.bind("<Leave>", on_clear_leave)

        # Quick Sale Section (Modern Card with shadow)
        quick_sale_card = tk.Frame(left_column, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                                  highlightthickness=1, highlightbackground=self.colors['border'])
        quick_sale_card.pack(fill=tk.BOTH, expand=True)

        # Quick Sale Header
        qs_header = tk.Frame(quick_sale_card, bg=self.colors['card'])
        qs_header.pack(fill=tk.X, padx=20, pady=(16, 8))

        tk.Label(qs_header, text="⚡",
                font=("Segoe UI", 18),
                bg=self.colors['card']).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(qs_header, text="Quick Sale",
                font=("Inter", 14, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(side=tk.LEFT, anchor=tk.W)

        # Quick sale tiles grid
        quick_buttons_frame = tk.Frame(quick_sale_card, bg=self.colors['card'])
        quick_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        # Get quick sale items
        quick_items = self.quick_sale.get_all_items()

        # Create grid of modern tiles (4 columns)
        if quick_items:
            row = 0
            col = 0
            for item in quick_items[:8]:  # Show max 8 items
                # Modern tile card
                tile_card = tk.Frame(quick_buttons_frame, bg=self.colors['light'],
                                   relief=tk.FLAT, highlightthickness=1,
                                   highlightbackground=self.colors['border'])
                tile_card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

                # Create button with proper closure
                def make_button_command(item_data):
                    return lambda: self.quick_add_item(item_data)

                # Modern tile button
                btn = tk.Button(tile_card,
                              text=f"{item['icon']}\n{item['name']}\n${item['price']:.2f}",
                              command=make_button_command(item),
                              bg=self.colors['light'],
                              fg=self.colors['text'],
                              font=("Inter", 9, "bold"),
                              relief=tk.FLAT,
                              bd=0,
                              cursor="hand2",
                              activebackground=self.colors['primary'],
                              activeforeground=self.colors['white'],
                              wraplength=70,
                              height=3,
                              width=10)
                btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

                # Hover effect with modern colors
                def make_hover_handlers(button, default_bg):
                    def on_enter(e):
                        button['bg'] = self.colors['primary']
                        button['fg'] = self.colors['white']

                    def on_leave(e):
                        button['bg'] = default_bg
                        button['fg'] = self.colors['text']

                    return on_enter, on_leave

                enter_handler, leave_handler = make_hover_handlers(btn, self.colors['light'])
                btn.bind("<Enter>", enter_handler)
                btn.bind("<Leave>", leave_handler)

                col += 1
                if col > 3:  # 4 columns
                    col = 0
                    row += 1
        else:
            tk.Label(quick_buttons_frame, text="No quick sale items configured",
                    font=("Inter", 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']).pack(pady=10)

        # Configure grid weights
        for i in range(4):
            quick_buttons_frame.grid_columnconfigure(i, weight=1)

        # Right Column - Scanner, Total, Payment & Keypad
        right_column = tk.Frame(main_frame, bg=self.colors['bg'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(12, 0))

        # Scanner Section (Modern Card)
        scanner_card = tk.Frame(right_column, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground=self.colors['border'])
        scanner_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(scanner_card, text="📱 Scan Item",
                font=("Inter", 12, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(padx=16, pady=(12, 8), anchor=tk.W)

        barcode_entry = tk.Entry(scanner_card, textvariable=self.barcode_var,
                                font=("Inter", 12),
                                width=28,
                                relief=tk.FLAT,
                                bg=self.colors['light'],
                                fg=self.colors['text'],
                                insertbackground=self.colors['primary'],
                                bd=0,
                                highlightthickness=1,
                                highlightbackground=self.colors['border'],
                                highlightcolor=self.colors['primary'])
        barcode_entry.pack(padx=16, pady=(0, 12), ipady=8)
        barcode_entry.focus()

        # Modern Add to Cart button with icon
        add_btn = tk.Button(scanner_card, text="🛒  Add to Cart",
                           command=self.add_to_cart,
                           bg=self.colors['primary'],
                           fg=self.colors['white'],
                           font=("Inter", 11, "bold"),
                           relief=tk.FLAT,
                           bd=0,
                           cursor="hand2",
                           activebackground=self.colors['primary_hover'])
        add_btn.pack(fill=tk.X, padx=16, pady=(0, 16), ipady=12)

        def on_add_enter(e):
            add_btn['bg'] = self.colors['primary_hover']
        def on_add_leave(e):
            add_btn['bg'] = self.colors['primary']
        add_btn.bind("<Enter>", on_add_enter)
        add_btn.bind("<Leave>", on_add_leave)

        # Total Display (Prominent Modern Card)
        total_card = tk.Frame(right_column, bg=self.colors['primary'], relief=tk.FLAT, bd=0,
                            highlightthickness=1, highlightbackground=self.colors['primary'])
        total_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(total_card, text="Total Amount",
                font=("Inter", 10),
                bg=self.colors['primary'],
                fg=self.colors['white']).pack(pady=(16, 4))

        total_label = tk.Label(total_card, textvariable=self.total_var,
                              font=("Inter", 32, "bold"),
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        total_label.pack(pady=(0, 16))

        def update_total_display(*args):
            pass  # Total var already bound
        self.total_var.trace('w', update_total_display)

        # Payment Section (Modern Card)
        payment_card = tk.Frame(right_column, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground=self.colors['border'])
        payment_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(payment_card, text="💳 Payment",
                font=("Inter", 12, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(padx=16, pady=(12, 8), anchor=tk.W)

        tk.Label(payment_card, text="Cash Received",
                font=("Inter", 9),
                bg=self.colors['card'],
                fg=self.colors['text_light']).pack(padx=16, pady=(0, 4), anchor=tk.W)

        cash_entry = tk.Entry(payment_card, textvariable=self.cash_var,
                             font=("Inter", 12),
                             width=28,
                             relief=tk.FLAT,
                             bg=self.colors['light'],
                             fg=self.colors['text'],
                             insertbackground=self.colors['primary'],
                             bd=0,
                             highlightthickness=1,
                             highlightbackground=self.colors['border'],
                             highlightcolor=self.colors['primary'])
        cash_entry.pack(padx=16, pady=(0, 12), ipady=8)

        # Change display
        change_container = tk.Frame(payment_card, bg=self.colors['light'])
        change_container.pack(fill=tk.X, padx=16, pady=(0, 12))

        tk.Label(change_container, text="Change:",
                font=("Inter", 9),
                bg=self.colors['light'],
                fg=self.colors['text_light']).pack(side=tk.LEFT, padx=8, pady=6)

        tk.Label(change_container, textvariable=self.change_var,
                font=("Inter", 16, "bold"),
                bg=self.colors['light'],
                fg=self.colors['success']).pack(side=tk.RIGHT, padx=8, pady=6)

        self.cash_var.trace('w', self.calculate_change)

        # Complete Sale Button (Large, prominent with icon)
        complete_btn = tk.Button(payment_card, text="✓  Complete Sale",
                                command=self.complete_sale,
                                bg=self.colors['success'],
                                fg=self.colors['white'],
                                font=("Inter", 12, "bold"),
                                relief=tk.FLAT,
                                bd=0,
                                cursor="hand2",
                                activebackground='#059669')
        complete_btn.pack(fill=tk.X, padx=16, pady=(0, 16), ipady=14)

        def on_complete_enter(e):
            complete_btn['bg'] = '#059669'
        def on_complete_leave(e):
            complete_btn['bg'] = self.colors['success']
        complete_btn.bind("<Enter>", on_complete_enter)
        complete_btn.bind("<Leave>", on_complete_leave)

        # Touchscreen Numeric Keypad (Modern Card with rounded buttons)
        keypad_card = tk.Frame(right_column, bg=self.colors['card'], relief=tk.FLAT, bd=0,
                              highlightthickness=1, highlightbackground=self.colors['border'])
        keypad_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(keypad_card, text="🔢 Keypad",
                font=("Inter", 12, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(padx=16, pady=(12, 8), anchor=tk.W)

        # Keypad buttons grid
        keypad_buttons = tk.Frame(keypad_card, bg=self.colors['card'])
        keypad_buttons.pack(padx=16, pady=(0, 16))

        # Create numeric buttons with modern styling
        buttons_layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['C', '0', '⌫']
        ]

        def keypad_click(value):
            if value == 'C':
                self.barcode_var.set("")
            elif value == '⌫':
                current = self.barcode_var.get()
                self.barcode_var.set(current[:-1])
            else:
                current = self.barcode_var.get()
                self.barcode_var.set(current + value)

        for row_idx, row in enumerate(buttons_layout):
            for col_idx, num in enumerate(row):
                # Color scheme for different button types
                if num == 'C':
                    bg_color = self.colors['warning']
                    hover_color = '#ea580c'
                elif num == '⌫':
                    bg_color = self.colors['danger']
                    hover_color = '#dc2626'
                else:
                    bg_color = self.colors['light']
                    hover_color = self.colors['primary']
                    num_fg = self.colors['text']

                # Rounded square button (modern design)
                btn_container = tk.Frame(keypad_buttons, bg=self.colors['card'])
                btn_container.grid(row=row_idx, column=col_idx, padx=4, pady=4)

                btn = tk.Button(btn_container,
                              text=num,
                              command=lambda v=num: keypad_click(v),
                              bg=bg_color,
                              fg=self.colors['white'] if num in ['C', '⌫'] else self.colors['text'],
                              font=("Inter", 16, "bold"),
                              relief=tk.FLAT,
                              bd=0,
                              cursor="hand2",
                              width=5,
                              height=2)
                btn.pack()

                # Modern hover effect with animation
                def make_hover(button, default_bg, hover_bg, is_special=False):
                    def on_enter(e):
                        button['bg'] = hover_bg
                        if not is_special:
                            button['fg'] = self.colors['white']

                    def on_leave(e):
                        button['bg'] = default_bg
                        if not is_special:
                            button['fg'] = self.colors['text']

                    return on_enter, on_leave

                enter_h, leave_h = make_hover(btn, bg_color, hover_color, num in ['C', '⌫'])
                btn.bind("<Enter>", enter_h)
                btn.bind("<Leave>", leave_h)

        # Configure grid weights for even spacing
        for i in range(3):
            keypad_buttons.grid_columnconfigure(i, weight=1)

        # Alerts Section (Modern Card - compact)
        alerts_frame = tk.Frame(right_column, bg=self.colors['white'], relief=tk.FLAT, bd=0)
        alerts_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(alerts_frame, text="⚠️ Alerts",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(padx=12, pady=(6, 3), anchor=tk.W)

        self.alerts_text = scrolledtext.ScrolledText(alerts_frame,
                                                     height=4,
                                                     font=("Segoe UI", 8),
                                                     state=tk.DISABLED,
                                                     relief=tk.FLAT,
                                                     bg=self.colors['light'],
                                                     fg=self.colors['text'],
                                                     bd=0,
                                                     wrap=tk.WORD)
        self.alerts_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))

    def create_modern_button(self, parent, text, command, bg_color, side=None, padx=0, pady=0, fill=None, height=2):
        """Create a modern flat button with hover effect"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color,
                       fg=self.colors['white'],
                       font=("Segoe UI", 11, "bold"),
                       relief=tk.FLAT,
                       bd=0,
                       cursor="hand2",
                       activebackground=self.darken_color(bg_color),
                       activeforeground=self.colors['white'],
                       height=height)

        if side:
            btn.pack(side=side, padx=padx, pady=pady, fill=fill if fill else None)
        else:
            btn.pack(padx=padx, pady=pady, fill=fill if fill else None)

        # Hover effect
        def on_enter(e):
            btn['bg'] = self.darken_color(bg_color)

        def on_leave(e):
            btn['bg'] = bg_color

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def darken_color(self, hex_color, factor=0.85):
        """Darken a hex color by a factor"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return '#%02x%02x%02x' % darkened

    def on_barcode_scan(self, event):
        """Handle barcode scan (Enter key press)"""
        self.add_to_cart()

    def quick_add_item(self, item):
        """Add quick sale item to cart"""
        # Create a product-like dictionary for cart
        quick_product = {
            'product_id': f"quick_{item['id']}",
            'name': item['name'],
            'price': item['price'],
            'stock': 999,  # Quick sale items don't track stock
            'barcode': f"QUICK{item['id']}"
        }

        # Add to cart
        self.cart.add_item(quick_product)
        self.update_cart_display()
        self.status_bar.config(text=f"Added: {item['name']} - ${item['price']:.2f}")

    def add_to_cart(self):
        """Add scanned product to cart"""
        barcode = self.barcode_var.get().strip()

        if not barcode:
            return

        # Validate barcode
        if not self.scanner.validate_barcode(barcode):
            messagebox.showerror("Invalid Barcode", "Please scan a valid barcode")
            self.barcode_var.set("")
            return

        # Get product from database
        product = self.db.get_product_by_barcode(barcode)

        if not product:
            messagebox.showerror("Product Not Found", f"No product found with barcode: {barcode}")
            self.barcode_var.set("")
            return

        # Check stock
        if product['stock'] <= 0:
            messagebox.showerror("Out of Stock", f"{product['name']} is out of stock!")
            self.barcode_var.set("")
            return

        # Add to cart
        self.cart.add_item(product)
        self.update_cart_display()
        self.barcode_var.set("")
        self.status_bar.config(text=f"Added: {product['name']}")

    def update_cart_display(self):
        """Update cart tree view"""
        # Clear tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Add items
        for item in self.cart.get_items():
            self.cart_tree.insert("", tk.END, values=(
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['subtotal']:.2f}"
            ), tags=(item['product_id'],))

        # Update total
        total = self.cart.get_total()
        self.total_var.set(f"${total:.2f}")

    def remove_item(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove")
            return

        item = self.cart_tree.item(selection[0])
        product_id = item['tags'][0]
        self.cart.remove_item(product_id)
        self.update_cart_display()
        self.status_bar.config(text="Item removed")

    def clear_cart(self):
        """Clear all items from cart"""
        if self.cart.is_empty():
            return

        if messagebox.askyesno("Clear Cart", "Are you sure you want to clear the cart?"):
            self.cart.clear()
            self.update_cart_display()
            self.cash_var.set("")
            self.change_var.set("$0.00")
            self.status_bar.config(text="Cart cleared")

    def calculate_change(self, *args):
        """Calculate change when cash amount is entered"""
        try:
            cash = float(self.cash_var.get() or 0)
            total = self.cart.get_total()
            change = cash - total
            self.change_var.set(f"${change:.2f}")
        except ValueError:
            self.change_var.set("$0.00")

    def complete_sale(self):
        """Complete the sale transaction"""
        if self.cart.is_empty():
            messagebox.showwarning("Empty Cart", "Please add items to cart")
            return

        try:
            cash_received = float(self.cash_var.get() or 0)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid cash amount")
            return

        total = self.cart.get_total()

        if cash_received < total:
            messagebox.showerror("Insufficient Payment", f"Cash received (${cash_received:.2f}) is less than total (${total:.2f})")
            return

        change = cash_received - total

        # Process inventory updates
        result = self.inventory.process_sale(self.cart.get_items())

        if not result['success']:
            messagebox.showerror("Sale Failed", f"Failed to update stock for: {', '.join(result['failed_items'])}")
            return

        # Save sale to database
        sale_data = {
            'total': total,
            'cash_received': cash_received,
            'change': change,
            'date': datetime.now()
        }

        sale_id = self.db.save_sale(self.cart.get_items(), total, cash_received, change)

        # Print receipt
        print_success = self.printer.print_receipt(sale_data, self.cart.get_items())

        # Display alerts
        if result['low_stock_alerts']:
            self.display_alerts(result['low_stock_alerts'])

        # Clear cart
        self.cart.clear()
        self.update_cart_display()
        self.cash_var.set("")
        self.change_var.set("$0.00")

        # Show completion message
        receipt_msg = "\nReceipt printed successfully!" if print_success else "\nReceipt saved to file (printer unavailable)"
        messagebox.showinfo("Sale Complete",
                          f"Sale #{sale_id} completed successfully!\n\n"
                          f"Change: ${change:.2f}"
                          f"{receipt_msg}\n\n"
                          f"Cash drawer opened.")
        self.status_bar.config(text=f"Sale #{sale_id} completed - Receipt printed")

    def display_alerts(self, alerts):
        """Display low stock alerts"""
        self.alerts_text.config(state=tk.NORMAL)
        self.alerts_text.delete(1.0, tk.END)

        for alert in alerts:
            self.alerts_text.insert(tk.END, f"{alert['message']}\n", "alert")
            self.alerts_text.insert(tk.END, "-" * 50 + "\n")

        self.alerts_text.tag_config("alert", foreground="red", font=("Arial", 9, "bold"))
        self.alerts_text.config(state=tk.DISABLED)

    def open_product_manager(self):
        """Open product management window"""
        ProductManagerWindow(self.root, self.db)

    def open_sales_reports(self):
        """Open sales reports window"""
        SalesReportWindow(self.root, self.db)

    def view_inventory_report(self):
        """Show inventory report"""
        report = self.inventory.get_inventory_report()

        msg = f"═══ INVENTORY REPORT ═══\n\n"
        msg += f"Total Products:        {report['total_products']}\n"
        msg += f"Low Stock Items:       {report['low_stock_count']}\n"
        msg += f"Out of Stock:          {report['out_of_stock_count']}\n"
        msg += f"Total Inventory Value: ${report['total_inventory_value']:.2f}\n\n"

        if report['low_stock_items']:
            msg += "LOW STOCK ITEMS:\n"
            msg += "-" * 50 + "\n"
            for item in report['low_stock_items']:
                msg += f"{item['name']}: {item['stock']} units (Alert: {item['low_stock_threshold']})\n"

        messagebox.showinfo("Inventory Report", msg)

    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Clear current user
            self.current_user = None

            # Destroy all widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Show login again
            self.show_login()

    def request_manager_approval(self):
        """Request manager approval for restricted actions"""
        # Create approval dialog
        approval_window = tk.Toplevel(self.root)
        approval_window.title("Manager Approval Required")
        approval_window.geometry("400x300")
        approval_window.configure(bg=self.colors['light'])
        approval_window.transient(self.root)
        approval_window.grab_set()

        # Center the window
        approval_window.update_idletasks()
        x = (approval_window.winfo_screenwidth() // 2) - (200)
        y = (approval_window.winfo_screenheight() // 2) - (150)
        approval_window.geometry(f"400x300+{x}+{y}")

        card = tk.Frame(approval_window, bg=self.colors['white'])
        card.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(card, text="🔒 Manager Approval Required",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(pady=(20, 10))

        tk.Label(card, text="This action requires manager credentials",
                font=("Segoe UI", 10),
                bg=self.colors['white'],
                fg=self.colors['text_light']).pack(pady=(0, 20))

        # Manager password
        tk.Label(card, text="Manager Password:",
                font=("Segoe UI", 9),
                bg=self.colors['white'],
                fg=self.colors['text_light']).pack(anchor=tk.W, padx=20)

        password_var = tk.StringVar()
        password_entry = tk.Entry(card, textvariable=password_var,
                                 font=("Segoe UI", 11),
                                 show="●",
                                 relief=tk.FLAT,
                                 bg=self.colors['light'],
                                 bd=0)
        password_entry.pack(fill=tk.X, padx=20, pady=(5, 20), ipady=8)
        password_entry.focus()

        error_label = tk.Label(card, text="",
                              font=("Segoe UI", 8),
                              bg=self.colors['white'],
                              fg=self.colors['danger'])
        error_label.pack()

        def verify_manager():
            # Try to authenticate as manager
            user = self.auth.authenticate('manager', password_var.get())
            if user and user['role'] == UserAuth.ROLE_MANAGER:
                approval_window.destroy()
                self.open_product_manager()
            else:
                error_label.config(text="Invalid manager credentials")
                password_var.set("")

        approve_btn = tk.Button(card, text="Approve",
                               command=verify_manager,
                               bg=self.colors['success'],
                               fg=self.colors['white'],
                               font=("Segoe UI", 10, "bold"),
                               relief=tk.FLAT,
                               cursor="hand2")
        approve_btn.pack(fill=tk.X, padx=20, pady=(10, 10), ipady=10)

        cancel_btn = tk.Button(card, text="Cancel",
                              command=approval_window.destroy,
                              bg=self.colors['danger'],
                              fg=self.colors['white'],
                              font=("Segoe UI", 10, "bold"),
                              relief=tk.FLAT,
                              cursor="hand2")
        cancel_btn.pack(fill=tk.X, padx=20, pady=(0, 20), ipady=10)

        password_entry.bind('<Return>', lambda e: verify_manager())

    def show_about(self):
        """Show about dialog"""
        about_text = f"""LastKings Liquor Store POS System
Version 1.0

A complete point-of-sale system featuring:
• Barcode scanning
• Inventory management
• Cash drawer integration
• Receipt printing
• Sales reporting
• Low stock alerts
• User authentication & role management

Logged in as: {self.current_user['full_name']} ({self.current_user['role'].title()})

Developed 2025"""
        messagebox.showinfo("About", about_text)

    def initialize_printer(self):
        """Initialize printer with selected or default printer"""
        try:
            import win32print
            # Check if X Printer is available
            printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]

            # Look for X Printer variants
            xprinter_name = None
            for p in printers:
                if 'xprinter' in p.lower() or 'x printer' in p.lower() or 'xp' in p.lower():
                    xprinter_name = p
                    break

            if xprinter_name:
                self.selected_printer.set(xprinter_name)
                self.printer = ReceiptPrinter(printer_name=xprinter_name)
            else:
                default_printer = win32print.GetDefaultPrinter()
                self.selected_printer.set(default_printer)
                self.printer = ReceiptPrinter(printer_name=default_printer)
        except:
            self.selected_printer.set("Not Connected")
            self.printer = ReceiptPrinter()

        self.update_printer_status()

    def update_printer_status(self):
        """Update printer status indicator"""
        try:
            # Check if win32print is available
            try:
                import win32print
                printer_available = True
                printer_name = self.selected_printer.get()
            except:
                printer_available = False
                printer_name = None

            if printer_available and printer_name and printer_name != "Not Connected":
                self.printer_status.config(
                    text=f"🖨️ {printer_name[:22]}",
                    bg=self.colors['success'],
                    fg=self.colors['white']
                )
            else:
                self.printer_status.config(
                    text="🖨️ No Printer (Saving to File)",
                    bg=self.colors['warning'],
                    fg=self.colors['dark']
                )
        except Exception as e:
            self.printer_status.config(
                text="🖨️ Printer Error",
                bg=self.colors['danger'],
                fg=self.colors['white']
            )

    def select_printer(self):
        """Open dialog to select printer"""
        try:
            import win32print
            printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]

            if not printers:
                messagebox.showwarning("No Printers", "No printers found. Please install printer drivers.")
                return

            # Create selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Printer")
            dialog.geometry("400x300")
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text="Select Receipt Printer:", font=("Arial", 12, "bold")).pack(pady=10)

            listbox = tk.Listbox(dialog, font=("Arial", 10), height=10)
            listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            for printer in printers:
                listbox.insert(tk.END, printer)

            # Pre-select current printer
            current = self.selected_printer.get()
            if current in printers:
                listbox.selection_set(printers.index(current))

            def on_select():
                selection = listbox.curselection()
                if selection:
                    selected = listbox.get(selection[0])
                    self.selected_printer.set(selected)
                    self.printer = ReceiptPrinter(printer_name=selected)
                    self.update_printer_status()
                    messagebox.showinfo("Printer Selected", f"Printer set to:\n{selected}")
                    dialog.destroy()

            tk.Button(dialog, text="Select Printer", command=on_select,
                     bg="#3498db", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to list printers:\n{str(e)}")

    def check_printer_status(self):
        """Check and display printer status"""
        self.update_printer_status()

        try:
            import win32print
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            current_printer = self.selected_printer.get()

            msg = "PRINTER STATUS\n\n"
            msg += f"Current Printer: {current_printer}\n\n"
            msg += f"Available Printers ({len(printers)}):\n"
            for printer_info in printers:
                msg += f"  • {printer_info[2]}\n"

            messagebox.showinfo("Printer Status", msg)
        except Exception as e:
            messagebox.showwarning("Printer Status",
                                  f"No printer detected.\n\n"
                                  f"Receipts will be saved as text files.\n\n"
                                  f"To use a physical printer:\n"
                                  f"1. Install printer drivers\n"
                                  f"2. Set printer as default in Windows\n"
                                  f"3. Install: pip install pywin32")

    def print_test_receipt(self):
        """Print a test receipt"""
        result = messagebox.askyesno("Test Receipt",
                                     "Print a test receipt?\n\n"
                                     "This will test your printer connection.")
        if result:
            success = self.printer.print_test_receipt()
            if success:
                messagebox.showinfo("Success",
                                  "Test receipt sent to printer!\n\n"
                                  "Check your printer or the receipt_*.txt file.")
            else:
                messagebox.showerror("Error", "Failed to print test receipt")

    def open_cash_drawer_manual(self):
        """Manually open cash drawer"""
        result = messagebox.askyesno("Open Cash Drawer",
                                     "Open the cash drawer?\n\n"
                                     "This requires a cash drawer connected to the printer.")
        if result:
            success = self.printer.open_cash_drawer()
            if success:
                messagebox.showinfo("Success", "Cash drawer command sent!")
            else:
                messagebox.showwarning("Warning", "Cash drawer command failed")

    def manage_quick_sale_items(self):
        """Manage quick sale items (Manager only)"""
        # Create management window
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Quick Sale Items")
        manage_window.geometry("700x600")
        manage_window.configure(bg=self.colors['light'])
        manage_window.transient(self.root)

        # Header
        header = tk.Frame(manage_window, bg=self.colors['primary'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="⚡ Quick Sale Items Management",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['primary'],
                fg=self.colors['white']).pack(pady=20, padx=20, anchor=tk.W)

        # Main content
        content = tk.Frame(manage_window, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Items list
        list_frame = tk.Frame(content, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Icon", "Name", "Price", "Category")
        items_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            items_tree.heading(col, text=col)
            if col == "ID":
                items_tree.column(col, width=50, anchor=tk.CENTER)
            elif col == "Icon":
                items_tree.column(col, width=50, anchor=tk.CENTER)
            elif col == "Price":
                items_tree.column(col, width=80, anchor=tk.E)
            else:
                items_tree.column(col, width=150)

        items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=items_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        items_tree.config(yscrollcommand=scrollbar.set)

        def refresh_list():
            """Refresh items list"""
            items_tree.delete(*items_tree.get_children())
            items = self.quick_sale.get_all_items(active_only=False)
            for item in items:
                status = "✓" if item['is_active'] else "✗"
                items_tree.insert("", tk.END, values=(
                    item['id'],
                    item['icon'],
                    f"{item['name']} {status}",
                    f"${item['price']:.2f}",
                    item['category']
                ))

        def add_new_item():
            """Add new quick sale item"""
            dialog = tk.Toplevel(manage_window)
            dialog.title("Add Quick Sale Item")
            dialog.geometry("400x400")
            dialog.configure(bg=self.colors['white'])
            dialog.transient(manage_window)
            dialog.grab_set()

            tk.Label(dialog, text="Add New Quick Sale Item",
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors['white']).pack(pady=20)

            # Name
            tk.Label(dialog, text="Name:", bg=self.colors['white']).pack(anchor=tk.W, padx=20)
            name_var = tk.StringVar()
            tk.Entry(dialog, textvariable=name_var, font=("Segoe UI", 11)).pack(fill=tk.X, padx=20, pady=5)

            # Price
            tk.Label(dialog, text="Price:", bg=self.colors['white']).pack(anchor=tk.W, padx=20)
            price_var = tk.StringVar()
            tk.Entry(dialog, textvariable=price_var, font=("Segoe UI", 11)).pack(fill=tk.X, padx=20, pady=5)

            # Category
            tk.Label(dialog, text="Category:", bg=self.colors['white']).pack(anchor=tk.W, padx=20)
            category_var = tk.StringVar()
            tk.Entry(dialog, textvariable=category_var, font=("Segoe UI", 11)).pack(fill=tk.X, padx=20, pady=5)

            # Icon
            tk.Label(dialog, text="Icon (emoji):", bg=self.colors['white']).pack(anchor=tk.W, padx=20)
            icon_var = tk.StringVar(value="📦")
            tk.Entry(dialog, textvariable=icon_var, font=("Segoe UI", 11)).pack(fill=tk.X, padx=20, pady=5)

            def save_item():
                try:
                    name = name_var.get().strip()
                    price = float(price_var.get())
                    category = category_var.get().strip()
                    icon = icon_var.get().strip()

                    if not name:
                        messagebox.showerror("Error", "Name is required")
                        return

                    self.quick_sale.add_item(name, price, category, icon)
                    refresh_list()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Quick sale item added!")
                except ValueError:
                    messagebox.showerror("Error", "Invalid price")

            tk.Button(dialog, text="Save", command=save_item,
                     bg=self.colors['success'], fg=self.colors['white'],
                     font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                     cursor="hand2").pack(fill=tk.X, padx=20, pady=20)

        # Buttons
        button_frame = tk.Frame(content, bg=self.colors['white'])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(button_frame, text="➕ Add New Item",
                 command=add_new_item,
                 bg=self.colors['success'],
                 fg=self.colors['white'],
                 font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT,
                 cursor="hand2",
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="🔄 Refresh",
                 command=refresh_list,
                 bg=self.colors['info'],
                 fg=self.colors['white'],
                 font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT,
                 cursor="hand2",
                 padx=20, pady=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Close",
                 command=manage_window.destroy,
                 bg=self.colors['danger'],
                 fg=self.colors['white'],
                 font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT,
                 cursor="hand2",
                 padx=20, pady=10).pack(side=tk.RIGHT, padx=5)

        # Initial load
        refresh_list()


def main():
    root = tk.Tk()
    app = POSSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()