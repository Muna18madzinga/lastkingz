# LastKingz POS System

A comprehensive Point of Sale system built with Flask, designed for retail businesses with support for multiple workstations, inventory management, and dual payment methods.

## Features

- 🛒 **POS Terminal** - Barcode scanning, product search, and quick sale items
- 👥 **Role-Based Access** - Separate interfaces for managers and cashiers
- 💰 **Dual Payment Methods** - Cash and EcoCash tracking
- 📊 **Sales Reports** - Real-time analytics and daily reports
- 📦 **Inventory Management** - Stock tracking with low stock alerts
- ⚡ **Quick Sale Items** - Customizable quick access products
- 🖨️ **Receipt Printing** - Automatic receipt generation
- 📱 **Responsive UI** - Works on desktop and tablets

## Quick Start

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/Muna18madzinga/lastkingz.git
cd lastkingz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application:
- Local: http://127.0.0.1:5000
- Network: http://YOUR_IP:5000

### Default Login Credentials

**Manager Account:**
- Username: `admin`
- Password: `admin123`

**Cashier Account:**
- Username: `cashier`
- Password: `cashier123`

⚠️ **Important**: Change these credentials after first login!

## Deployment on Render

### Prerequisites
- GitHub account
- Render account (free tier available)

### Steps

1. **Fork or clone this repository to your GitHub**

2. **Sign up at [Render.com](https://render.com)**
   - Use GitHub to sign up for easier integration

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `lastkingz` repository

4. **Configure Settings** (auto-detected from render.yaml):
   - **Name**: `lastkingz-pos`
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Access your app at: `https://your-app-name.onrender.com`

### Render Free Tier Notes
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds
- 750 hours/month free
- Automatic deploys on git push

## Project Structure

```
lastkingz/
├── app.py                  # Main Flask application
├── database.py             # Database operations
├── user_auth.py            # Authentication system
├── shopping_cart.py        # Shopping cart logic
├── inventory_manager.py    # Inventory management
├── quick_sale.py           # Quick sale items
├── receipt_printer.py      # Receipt generation
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── manager/           # Manager interface
│   └── cashier/           # Cashier interface
├── static/
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
├── requirements.txt        # Python dependencies
├── build.sh               # Render build script
└── render.yaml            # Render configuration
```

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn (production)
- **Authentication**: Session-based with role management

## API Endpoints

### Products
- `GET /api/product/<search_term>` - Search product by barcode or name
- `GET /api/search-products?q=<query>` - Search products
- `POST /api/product` - Add new product (manager only)
- `PUT /api/product/<id>` - Update product (manager only)
- `DELETE /api/product/<id>` - Delete product (manager only)

### Sales
- `POST /api/complete-sale` - Complete a sale transaction
- `GET /api/sales-report/<period>` - Get sales report
- `GET /api/cashier-daily-sales` - Get daily sales for cashier

### Quick Sale
- `GET /api/quick-sale/<id>` - Get quick sale item
- `POST /api/quick-sale` - Create quick sale item (manager only)
- `PUT /api/quick-sale/<id>` - Update quick sale item (manager only)
- `DELETE /api/quick-sale/<id>` - Delete quick sale item (manager only)

## Database Schema

### Tables
- **users** - User authentication and roles
- **products** - Product inventory
- **quick_sale_items** - Quick access items
- **sales** - Sales transactions
- **sale_items** - Individual sale line items

## Security Features

- Session-based authentication (8-hour expiry)
- Role-based access control (@manager_required, @login_required)
- Password hashing (recommended to implement bcrypt)
- CSRF protection (implement for production)

## Payment Methods

The system supports two payment methods:
- **Cash** - Traditional cash payments
- **EcoCash** - Mobile money payments

Each payment method is tracked separately in reports.

## Development

### Adding Products
Use the Products page in the manager interface or run:
```bash
python add_products_interactive.py
```

### Managing Quick Sale Items
Access the Quick Sales menu in the manager interface to add, edit, or remove quick sale items.

## Troubleshooting

**Database not found:**
```bash
python -c "from database import Database; Database()"
```

**Port already in use:**
```bash
# Change port in app.py or use environment variable
PORT=8000 python app.py
```

**Permission denied on build.sh:**
```bash
chmod +x build.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Email: support@lastkingz.com

## Acknowledgments

Built with ❤️ for LastKingz retail business

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
