"""
seed_data.py
────────────
Populates all tables with realistic dummy data for quick
testing and demonstration of the Tour & Travel Management
System.  Run once after the database has been initialized.
"""

import pymysql
from db_config import get_connection, initialize_database


def seed():
    """Insert sample data into every table (idempotent-safe)."""
    initialize_database()
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            # ── Users ──────────────────────────────────────────
            cur.execute("SELECT COUNT(*) AS cnt FROM Users")
            if cur.fetchone()["cnt"] == 0:
                users = [
                    ("Aarav Sharma",   "aarav.sharma@email.com",   "9876543210"),
                    ("Priya Patel",    "priya.patel@email.com",    "9876543211"),
                    ("Rohan Mehta",    "rohan.mehta@email.com",    "9876543212"),
                    ("Sneha Iyer",     "sneha.iyer@email.com",     "9876543213"),
                    ("Vikram Singh",   "vikram.singh@email.com",   "9876543214"),
                ]
                cur.executemany(
                    "INSERT INTO Users (name, email, phone) VALUES (%s,%s,%s)",
                    users,
                )
                print(f"  ✅ Inserted {len(users)} users.")

            # ── Tour Packages ─────────────────────────────────
            cur.execute("SELECT COUNT(*) AS cnt FROM Tour_Packages")
            if cur.fetchone()["cnt"] == 0:
                packages = [
                    ("Golden Triangle",      "Delhi-Agra-Jaipur", 6,  25000.00),
                    ("Kerala Backwaters",     "Kerala",            5,  22000.00),
                    ("Himalayan Adventure",   "Manali-Leh",        8,  35000.00),
                    ("Goa Beach Retreat",     "Goa",               4,  18000.00),
                    ("Rajasthan Heritage",    "Udaipur-Jodhpur",   7,  30000.00),
                ]
                cur.executemany(
                    "INSERT INTO Tour_Packages "
                    "(package_name, destination, duration_days, price) "
                    "VALUES (%s,%s,%s,%s)",
                    packages,
                )
                print(f"  ✅ Inserted {len(packages)} packages.")

            # ── Tour Guides ───────────────────────────────────
            cur.execute("SELECT COUNT(*) AS cnt FROM Tour_Guides")
            if cur.fetchone()["cnt"] == 0:
                guides = [
                    ("Amit Kumar",    "Hindi, English",          "Available"),
                    ("Lakshmi Nair",  "Malayalam, English",      "Available"),
                    ("Tenzin Dorje",  "Hindi, English, Tibetan", "Available"),
                    ("Fatima Sheikh", "Hindi, Urdu, English",    "Available"),
                    ("Rajesh Verma",  "Hindi, English, French",  "Available"),
                ]
                cur.executemany(
                    "INSERT INTO Tour_Guides "
                    "(name, language_expertise, availability_status) "
                    "VALUES (%s,%s,%s)",
                    guides,
                )
                print(f"  ✅ Inserted {len(guides)} guides.")

            # ── Hotels ────────────────────────────────────────
            cur.execute("SELECT COUNT(*) AS cnt FROM Hotels")
            if cur.fetchone()["cnt"] == 0:
                hotels = [
                    ("Taj Lake Palace",    "Udaipur",  5.0, 12000.00),
                    ("The Leela",          "Goa",      4.5,  9500.00),
                    ("ITC Grand Chola",    "Chennai",  4.8, 10000.00),
                    ("Oberoi Wildflower",  "Shimla",   4.7, 11000.00),
                    ("Radisson Blu",       "Delhi",    4.2,  7500.00),
                ]
                cur.executemany(
                    "INSERT INTO Hotels "
                    "(hotel_name, location, rating, price_per_night) "
                    "VALUES (%s,%s,%s,%s)",
                    hotels,
                )
                print(f"  ✅ Inserted {len(hotels)} hotels.")

            # ── Transportation ────────────────────────────────
            cur.execute("SELECT COUNT(*) AS cnt FROM Transportation")
            if cur.fetchone()["cnt"] == 0:
                transport = [
                    ("AC Bus",        40, "Ramesh Yadav"),
                    ("SUV (Innova)",   6, "Sunil Chauhan"),
                    ("Sedan (Dzire)",  4, "Manoj Tiwari"),
                    ("Tempo Traveller",12, "Karan Joshi"),
                    ("Mini Van",       8, "Deepak Rawat"),
                ]
                cur.executemany(
                    "INSERT INTO Transportation "
                    "(vehicle_type, capacity, driver_name) "
                    "VALUES (%s,%s,%s)",
                    transport,
                )
                print(f"  ✅ Inserted {len(transport)} transport options.")

        conn.commit()
        print("\n🎉 Seed data loaded successfully!\n")

    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Seeding failed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
