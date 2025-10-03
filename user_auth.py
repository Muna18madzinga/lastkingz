import sqlite3
import hashlib
from datetime import datetime

class UserAuth:
    """User authentication and role management"""

    ROLE_CASHIER = "cashier"
    ROLE_MANAGER = "manager"

    def __init__(self, db_name="lastkings_pos.db"):
        self.db_name = db_name
        self.init_users_table()
        self.create_default_users()

    def init_users_table(self):
        """Initialize users table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        conn.close()

    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_default_users(self):
        """Create default manager and cashier accounts"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Create default manager
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            """, ('manager', self.hash_password('manager123'), 'Store Manager', self.ROLE_MANAGER))

            # Create default cashier
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            """, ('cashier', self.hash_password('cashier123'), 'Cashier', self.ROLE_CASHIER))

            conn.commit()

        conn.close()

    def authenticate(self, username, password):
        """Authenticate user and return user data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, full_name, role, is_active
            FROM users
            WHERE username = ? AND password_hash = ?
        """, (username, self.hash_password(password)))

        user = cursor.fetchone()

        if user and user[4]:  # Check if user exists and is active
            # Log login
            cursor.execute("""
                INSERT INTO login_history (user_id)
                VALUES (?)
            """, (user[0],))
            conn.commit()

            user_data = {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'role': user[3],
                'is_active': user[4]
            }
            conn.close()
            return user_data

        conn.close()
        return None

    def add_user(self, username, password, full_name, role):
        """Add new user (manager only)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            """, (username, self.hash_password(password), full_name, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def get_all_users(self):
        """Get all users (manager only)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, full_name, role, is_active, created_at
            FROM users
            ORDER BY created_at DESC
        """)

        users = [{'id': r[0], 'username': r[1], 'full_name': r[2],
                 'role': r[3], 'is_active': r[4], 'created_at': r[5]}
                for r in cursor.fetchall()]

        conn.close()
        return users

    def change_password(self, user_id, new_password):
        """Change user password"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
        """, (self.hash_password(new_password), user_id))

        conn.commit()
        conn.close()
        return True
