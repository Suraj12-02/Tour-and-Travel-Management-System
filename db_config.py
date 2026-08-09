"""
db_config.py
────────────
Handles MySQL connection management and automatic schema
bootstrapping for the Tour & Travel Management System.
"""

import pymysql
import sys

# ── Connection Parameters ─────────────────────────────────────
DB_HOST = os.getenv("DB_HOST") 
DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD") 
DB_NAME = os.getenv("DB_NAME") 
DB_PORT = int(os.getenv("DB_PORT", 3306))


def get_connection(database: str = DB_NAME):
    """Return a pymysql connection object to the specified database."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"\n[ERROR] Could not connect to MySQL: {e}")
        sys.exit(1)


def _get_server_connection():
    """Return a connection to the MySQL server (no database selected)."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"\n[ERROR] Could not connect to MySQL server: {e}")
        sys.exit(1)


def initialize_database():
    """Create the database and all tables if they do not already exist."""
    # Step 1 – Create the database
    server_conn = _get_server_connection()
    try:
        with server_conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        print(f"[OK] Database '{DB_NAME}' is ready.")
    finally:
        server_conn.close()

    # Step 2 – Create all tables inside tour_travel_db
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # ── Users ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id       INT AUTO_INCREMENT PRIMARY KEY,
                    name          VARCHAR(100)  NOT NULL,
                    email         VARCHAR(150)  NOT NULL UNIQUE,
                    phone         VARCHAR(15)   NOT NULL
                ) ENGINE=InnoDB
            """)

            # ── Tour_Packages ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Tour_Packages (
                    package_id    INT AUTO_INCREMENT PRIMARY KEY,
                    package_name  VARCHAR(150)  NOT NULL,
                    destination   VARCHAR(150)  NOT NULL,
                    duration_days INT           NOT NULL,
                    price         DECIMAL(10,2) NOT NULL
                ) ENGINE=InnoDB
            """)

            # ── Tour_Guides ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Tour_Guides (
                    guide_id            INT AUTO_INCREMENT PRIMARY KEY,
                    name                VARCHAR(100) NOT NULL,
                    language_expertise  VARCHAR(200) NOT NULL,
                    availability_status ENUM('Available','Assigned')
                                        NOT NULL DEFAULT 'Available'
                ) ENGINE=InnoDB
            """)

            # ── Hotels ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Hotels (
                    hotel_id        INT AUTO_INCREMENT PRIMARY KEY,
                    hotel_name      VARCHAR(150)  NOT NULL,
                    location        VARCHAR(150)  NOT NULL,
                    rating          DECIMAL(2,1)  NOT NULL,
                    price_per_night DECIMAL(10,2) NOT NULL
                ) ENGINE=InnoDB
            """)

            # ── Transportation ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Transportation (
                    transport_id  INT AUTO_INCREMENT PRIMARY KEY,
                    vehicle_type  VARCHAR(50)  NOT NULL,
                    capacity      INT          NOT NULL,
                    driver_name   VARCHAR(100) NOT NULL
                ) ENGINE=InnoDB
            """)

            # ── Bookings ──
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Bookings (
                    booking_id    INT AUTO_INCREMENT PRIMARY KEY,
                    user_id       INT            NOT NULL,
                    package_id    INT            NOT NULL,
                    guide_id      INT            NOT NULL,
                    hotel_id      INT            NOT NULL,
                    transport_id  INT            NOT NULL,
                    booking_date  DATE           NOT NULL,
                    total_cost    DECIMAL(12,2)  NOT NULL,
                    status        ENUM('Active','Cancelled')
                                  NOT NULL DEFAULT 'Active',
                    FOREIGN KEY (user_id)
                        REFERENCES Users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (package_id)
                        REFERENCES Tour_Packages(package_id) ON DELETE CASCADE,
                    FOREIGN KEY (guide_id)
                        REFERENCES Tour_Guides(guide_id) ON DELETE CASCADE,
                    FOREIGN KEY (hotel_id)
                        REFERENCES Hotels(hotel_id) ON DELETE CASCADE,
                    FOREIGN KEY (transport_id)
                        REFERENCES Transportation(transport_id) ON DELETE CASCADE
                ) ENGINE=InnoDB
            """)

        conn.commit()
        print("[OK] All tables verified / created successfully.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"[ERROR] Table creation failed: {e}")
        sys.exit(1)
    finally:
        conn.close()


# Run bootstrap when this module is executed directly
if __name__ == "__main__":
    initialize_database()
