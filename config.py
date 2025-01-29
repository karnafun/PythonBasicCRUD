import os

class Config:
    # Database configuration
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')  # Default to 'root' if no environment variable is set
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'MySqlPassword123')  # Default password if not set
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  # Default to 'localhost'
    MYSQL_DB = os.getenv('MYSQL_DB', 'ThisIsHowItsDone')  # Default database name

    # Full connection URI for the database
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

    # Any other configurations you may need
    SQLALCHEMY_TRACK_MODIFICATIONS = False
