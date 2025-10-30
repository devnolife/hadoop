"""
Create Sample Data for Hadoop Toolkit Demo
Generate dummy data untuk testing MySQL dan HDFS operations
Author: devnolife
"""

from src.mysql_handler import MySQLHandler
import random
from datetime import datetime, timedelta


def generate_sample_products(count=100):
    """Generate sample products data"""
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Toys', 'Sports', 'Home', 'Beauty']
    brands = ['Samsung', 'Apple', 'Nike', 'Adidas', 'Sony', 'LG', 'HP', 'Dell']
    
    products = []
    for i in range(1, count + 1):
        product = {
            'name': f'{random.choice(brands)} {random.choice(["Pro", "Max", "Plus", "Ultra"])} {i}',
            'category': random.choice(categories),
            'price': round(random.uniform(10000, 5000000), 2),
            'stock': random.randint(0, 500),
            'rating': round(random.uniform(3.0, 5.0), 1)
        }
        products.append(product)
    
    return products


def generate_sample_customers(count=50):
    """Generate sample customers data"""
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa', 'Tom', 'Anna']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Makassar', 'Palembang']
    
    customers = []
    for i in range(1, count + 1):
        customer = {
            'name': f'{random.choice(first_names)} {random.choice(last_names)}',
            'email': f'customer{i}@example.com',
            'phone': f'08{random.randint(1000000000, 9999999999)}',
            'city': random.choice(cities),
            'registered_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        }
        customers.append(customer)
    
    return customers


def generate_sample_orders(count=200, max_customer_id=50, max_product_id=100):
    """Generate sample orders data"""
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    orders = []
    for i in range(1, count + 1):
        order = {
            'customer_id': random.randint(1, max_customer_id),
            'product_id': random.randint(1, max_product_id),
            'quantity': random.randint(1, 10),
            'total_price': round(random.uniform(50000, 10000000), 2),
            'status': random.choice(statuses),
            'order_date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d %H:%M:%S')
        }
        orders.append(order)
    
    return orders


def create_sample_database():
    """Create sample database with tables and data"""
    print("=" * 60)
    print("🎨 Sample Data Generator for Hadoop Toolkit")
    print("=" * 60)
    
    # MySQL Connection
    print("\n📊 MySQL Connection Settings:")
    host = input("Host (localhost): ").strip() or "localhost"
    port = input("Port (3306): ").strip() or "3306"
    user = input("User (root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database name (test_db): ").strip() or "test_db"
    
    try:
        # Connect to MySQL (without database)
        print("\n🔌 Connecting to MySQL...")
        mysql = MySQLHandler(
            host=host,
            port=int(port),
            user=user,
            password=password
        )
        
        if not mysql.connect():
            print("❌ Failed to connect to MySQL")
            return
        
        # Create database if not exists
        print(f"\n🗄️  Creating database '{database}'...")
        mysql.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        mysql.cursor.execute(f"USE {database}")
        mysql.connection.commit()
        print(f"✅ Database '{database}' ready")
        
        # Create products table
        print("\n📦 Creating 'products' table...")
        mysql.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(200) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(12,2),
                stock INT,
                rating DECIMAL(2,1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        print("✅ Table 'products' created")
        
        # Insert products
        print("📥 Inserting sample products...")
        products = generate_sample_products(100)
        for product in products:
            mysql.cursor.execute("""
                INSERT INTO products (name, category, price, stock, rating)
                VALUES (%s, %s, %s, %s, %s)
            """, (product['name'], product['category'], product['price'], 
                  product['stock'], product['rating']))
        mysql.connection.commit()
        print(f"✅ Inserted {len(products)} products")
        
        # Create customers table
        print("\n👥 Creating 'customers' table...")
        mysql.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20),
                city VARCHAR(50),
                registered_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        print("✅ Table 'customers' created")
        
        # Insert customers
        print("📥 Inserting sample customers...")
        customers = generate_sample_customers(50)
        for customer in customers:
            mysql.cursor.execute("""
                INSERT INTO customers (name, email, phone, city, registered_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (customer['name'], customer['email'], customer['phone'], 
                  customer['city'], customer['registered_date']))
        mysql.connection.commit()
        print(f"✅ Inserted {len(customers)} customers")
        
        # Create orders table
        print("\n🛒 Creating 'orders' table...")
        mysql.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT,
                product_id INT,
                quantity INT,
                total_price DECIMAL(12,2),
                status VARCHAR(20),
                order_date DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        mysql.connection.commit()
        print("✅ Table 'orders' created")
        
        # Insert orders
        print("📥 Inserting sample orders...")
        orders = generate_sample_orders(200, 50, 100)
        for order in orders:
            mysql.cursor.execute("""
                INSERT INTO orders (customer_id, product_id, quantity, total_price, status, order_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (order['customer_id'], order['product_id'], order['quantity'], 
                  order['total_price'], order['status'], order['order_date']))
        mysql.connection.commit()
        print(f"✅ Inserted {len(orders)} orders")
        
        # Create sales_summary view
        print("\n📊 Creating 'sales_summary' view...")
        mysql.cursor.execute("""
            CREATE OR REPLACE VIEW sales_summary AS
            SELECT 
                p.category,
                COUNT(o.id) as total_orders,
                SUM(o.quantity) as total_quantity,
                SUM(o.total_price) as total_revenue,
                AVG(o.total_price) as avg_order_value
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.status = 'delivered'
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """)
        mysql.connection.commit()
        print("✅ View 'sales_summary' created")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Sample Data Summary")
        print("=" * 60)
        
        # Count records
        mysql.cursor.execute("SELECT COUNT(*) as count FROM products")
        products_count = mysql.cursor.fetchone()['count']
        
        mysql.cursor.execute("SELECT COUNT(*) as count FROM customers")
        customers_count = mysql.cursor.fetchone()['count']
        
        mysql.cursor.execute("SELECT COUNT(*) as count FROM orders")
        orders_count = mysql.cursor.fetchone()['count']
        
        print(f"✅ Products: {products_count} records")
        print(f"✅ Customers: {customers_count} records")
        print(f"✅ Orders: {orders_count} records")
        print(f"✅ Views: 1 (sales_summary)")
        
        print("\n📋 Sample Queries to Try:")
        print("-" * 60)
        print("-- Top selling categories")
        print("SELECT * FROM sales_summary;")
        print("\n-- Recent orders")
        print("SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;")
        print("\n-- Customer with most orders")
        print("SELECT c.name, COUNT(o.id) as order_count")
        print("FROM customers c JOIN orders o ON c.id = o.customer_id")
        print("GROUP BY c.id ORDER BY order_count DESC LIMIT 5;")
        
        print("\n" + "=" * 60)
        print("🎉 Sample data created successfully!")
        print("=" * 60)
        print(f"\n🌐 Next Steps:")
        print(f"1. Open web interface: http://localhost:5000")
        print(f"2. Connect to database: {database}")
        print(f"3. Browse tables and export data")
        print(f"4. Try HDFS operations!")
        
        mysql.disconnect()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        create_sample_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
