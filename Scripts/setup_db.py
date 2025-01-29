import os
import subprocess
import sys
import time
import pymysql
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Function to install dependencies from requirements.txt
def install_requirements():
    print("Installing dependencies from requirements.txt...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

# Function to check if MySQL is running (for Windows)
def check_mysql_running():
    try:
        # Check if MySQL is running by attempting a simple query using Config values
        conn = pymysql.connect(
            host=config.Config.MYSQL_HOST,
            user=config.Config.MYSQL_USER,
            password=config.Config.MYSQL_PASSWORD
        )
        conn.close()
        print("MySQL is running.")
    except pymysql.MySQLError as e:
        print("MySQL is not running. Attempting to start MySQL...")
        start_mysql()

# Function to start MySQL (for Windows)
def start_mysql():
    # Starting MySQL service for Windows (adjust path if needed)
    print("Starting MySQL...")
    try:
        subprocess.run(["net", "start", "MySQL"], check=True)
        time.sleep(5)  # Give MySQL some time to start
        print("MySQL started successfully.")
    except subprocess.CalledProcessError:
        print("Failed to start MySQL. Please start it manually.")
        sys.exit(1)

# Function to create the database if it doesn't exist
def create_database():
    try:
        # Connect to MySQL using Config values
        conn = pymysql.connect(
            host=config.Config.MYSQL_HOST,
            user=config.Config.MYSQL_USER,
            password=config.Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.Config.MYSQL_DB};")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database '{config.Config.MYSQL_DB}' is ready.")
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def create_user_table_and_insert_dummy_data():
    try:
        # Connect to the specific database
        conn = pymysql.connect(
            host=config.Config.MYSQL_HOST,
            user=config.Config.MYSQL_USER,
            password=config.Config.MYSQL_PASSWORD,
            database=config.Config.MYSQL_DB
        )
        cursor = conn.cursor()

        # Drop the users table if it exists
        cursor.execute("DROP TABLE IF EXISTS users;")
        conn.commit()

        # Create the users table with the updated schema (including roles)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                city VARCHAR(100),
                age INT,
                phone_number VARCHAR(20),
                birth_date DATE,
                role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
                active BOOLEAN DEFAULT TRUE,
                password_hash VARCHAR(255) NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        # Hashing the password for dummy users
        hashed_admin_password = generate_password_hash('Aa123456')
        hashed_user_password = generate_password_hash('Aa123456')

        # Insert dummy users with different roles and hashed passwords
        cursor.execute("""
            INSERT INTO users (name, city, age, phone_number, birth_date, role, password_hash) 
            VALUES ('admin', 'New York', 30, '123-456-7890', '1990-01-01', 'admin', %s);
        """, (hashed_admin_password,))
        cursor.execute("""
            INSERT INTO users (name, city, age, phone_number, birth_date, role, password_hash) 
            VALUES ('Jane Smith', 'Los Angeles', 25, '987-654-3210', '1998-05-15', 'user', %s);
        """, (hashed_user_password,))
        conn.commit()

        print("User table recreated and dummy users inserted.")
        cursor.close()
        conn.close()
    except pymysql.MySQLError as e:
        print(f"Error recreating user table or inserting dummy data: {e}")
        sys.exit(1)

# Run the setup process
if __name__ == "__main__":
    # Install the requirements
    install_requirements()

    # Check if MySQL is running
    check_mysql_running()

    # Create the database
    create_database()

    # Recreate the user table and insert dummy data
    create_user_table_and_insert_dummy_data()

    print("Project setup completed successfully!")
