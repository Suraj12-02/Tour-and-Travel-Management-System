"""
operations.py
─────────────
All CRUD and reporting operations for the Tour & Travel
Management System.  Every SQL query is parameterized to
prevent SQL injection and multi-table writes use explicit
transactions for ACID compliance.
"""

import pymysql
from datetime import date
from db_config import get_connection


# ══════════════════════════════════════════════════════════════
#  PACKAGE OPERATIONS
# ══════════════════════════════════════════════════════════════

def add_package(name: str, destination: str, duration: int, price: float):
    """Insert a new tour package."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """INSERT INTO Tour_Packages
                     (package_name, destination, duration_days, price)
                     VALUES (%s, %s, %s, %s)"""
            cur.execute(sql, (name, destination, duration, price))
        conn.commit()
        print(f"\n✅ Package '{name}' added successfully.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error adding package: {e}")
    finally:
        conn.close()


def view_packages():
    """Retrieve and display all tour packages."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Tour_Packages ORDER BY package_id")
            rows = cur.fetchall()
        if not rows:
            print("\n📭 No packages found.")
            return []
        print("\n" + "=" * 90)
        print(f"{'ID':<6}{'Package Name':<25}{'Destination':<20}"
              f"{'Days':<8}{'Price (₹)':<12}")
        print("=" * 90)
        for r in rows:
            print(f"{r['package_id']:<6}{r['package_name']:<25}"
                  f"{r['destination']:<20}{r['duration_days']:<8}"
                  f"{r['price']:<12.2f}")
        print("=" * 90)
        return rows
    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching packages: {e}")
        return []
    finally:
        conn.close()


def update_package(pkg_id: int, name: str, destination: str,
                   duration: int, price: float):
    """Update an existing tour package by ID."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """UPDATE Tour_Packages
                     SET package_name=%s, destination=%s,
                         duration_days=%s, price=%s
                     WHERE package_id=%s"""
            cur.execute(sql, (name, destination, duration, price, pkg_id))
        conn.commit()
        if cur.rowcount:
            print(f"\n✅ Package ID {pkg_id} updated.")
        else:
            print(f"\n⚠️  Package ID {pkg_id} not found.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error updating package: {e}")
    finally:
        conn.close()


def delete_package(pkg_id: int):
    """Delete a tour package (cascades to related bookings)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Tour_Packages WHERE package_id=%s",
                        (pkg_id,))
        conn.commit()
        if cur.rowcount:
            print(f"\n✅ Package ID {pkg_id} deleted.")
        else:
            print(f"\n⚠️  Package ID {pkg_id} not found.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error deleting package: {e}")
    finally:
        conn.close()


# ══════════════════════════════════════════════════════════════
#  TOUR GUIDE OPERATIONS
# ══════════════════════════════════════════════════════════════

def add_guide(name: str, languages: str):
    """Insert a new tour guide (defaults to 'Available')."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """INSERT INTO Tour_Guides
                     (name, language_expertise, availability_status)
                     VALUES (%s, %s, 'Available')"""
            cur.execute(sql, (name, languages))
        conn.commit()
        print(f"\n✅ Guide '{name}' added successfully.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error adding guide: {e}")
    finally:
        conn.close()


def view_guides():
    """Retrieve and display all tour guides."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Tour_Guides ORDER BY guide_id")
            rows = cur.fetchall()
        if not rows:
            print("\n📭 No guides found.")
            return []
        print("\n" + "=" * 80)
        print(f"{'ID':<6}{'Name':<22}{'Languages':<30}{'Status':<15}")
        print("=" * 80)
        for r in rows:
            print(f"{r['guide_id']:<6}{r['name']:<22}"
                  f"{r['language_expertise']:<30}"
                  f"{r['availability_status']:<15}")
        print("=" * 80)
        return rows
    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching guides: {e}")
        return []
    finally:
        conn.close()


def update_guide_availability(guide_id: int, status: str):
    """Set a guide's availability_status ('Available' or 'Assigned')."""
    if status not in ("Available", "Assigned"):
        print("\n⚠️  Status must be 'Available' or 'Assigned'.")
        return
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE Tour_Guides SET availability_status=%s WHERE guide_id=%s",
                (status, guide_id),
            )
        conn.commit()
        if cur.rowcount:
            print(f"\n✅ Guide ID {guide_id} → {status}.")
        else:
            print(f"\n⚠️  Guide ID {guide_id} not found.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error updating guide: {e}")
    finally:
        conn.close()


def _get_available_guide(cursor):
    """Return the first available guide's ID, or None."""
    cursor.execute(
        "SELECT guide_id FROM Tour_Guides "
        "WHERE availability_status='Available' LIMIT 1"
    )
    row = cursor.fetchone()
    return row["guide_id"] if row else None


# ══════════════════════════════════════════════════════════════
#  HOTEL OPERATIONS (view for booking selection)
# ══════════════════════════════════════════════════════════════

def view_hotels():
    """Retrieve and display all hotels."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Hotels ORDER BY hotel_id")
            rows = cur.fetchall()
        if not rows:
            print("\n📭 No hotels found.")
            return []
        print("\n" + "=" * 90)
        print(f"{'ID':<6}{'Hotel Name':<25}{'Location':<20}"
              f"{'Rating':<8}{'₹/Night':<12}")
        print("=" * 90)
        for r in rows:
            print(f"{r['hotel_id']:<6}{r['hotel_name']:<25}"
                  f"{r['location']:<20}{r['rating']:<8}"
                  f"{r['price_per_night']:<12.2f}")
        print("=" * 90)
        return rows
    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching hotels: {e}")
        return []
    finally:
        conn.close()


# ══════════════════════════════════════════════════════════════
#  TRANSPORTATION OPERATIONS (view for booking selection)
# ══════════════════════════════════════════════════════════════

def view_transport():
    """Retrieve and display all transportation options."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Transportation ORDER BY transport_id")
            rows = cur.fetchall()
        if not rows:
            print("\n📭 No transport options found.")
            return []
        print("\n" + "=" * 80)
        print(f"{'ID':<6}{'Vehicle':<18}{'Capacity':<10}{'Driver':<20}")
        print("=" * 80)
        for r in rows:
            print(f"{r['transport_id']:<6}{r['vehicle_type']:<18}"
                  f"{r['capacity']:<10}{r['driver_name']:<20}")
        print("=" * 80)
        return rows
    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching transport: {e}")
        return []
    finally:
        conn.close()


# ══════════════════════════════════════════════════════════════
#  USER OPERATIONS (for booking creation)
# ══════════════════════════════════════════════════════════════

def view_users():
    """Retrieve and display all registered users."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Users ORDER BY user_id")
            rows = cur.fetchall()
        if not rows:
            print("\n📭 No users found.")
            return []
        print("\n" + "=" * 70)
        print(f"{'ID':<6}{'Name':<22}{'Email':<28}{'Phone':<15}")
        print("=" * 70)
        for r in rows:
            print(f"{r['user_id']:<6}{r['name']:<22}"
                  f"{r['email']:<28}{r['phone']:<15}")
        print("=" * 70)
        return rows
    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching users: {e}")
        return []
    finally:
        conn.close()


def add_user(name: str, email: str, phone: str):
    """Register a new customer."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO Users (name, email, phone) VALUES (%s, %s, %s)"
            cur.execute(sql, (name, email, phone))
        conn.commit()
        print(f"\n✅ User '{name}' registered (ID: {cur.lastrowid}).")
        return cur.lastrowid
    except pymysql.IntegrityError:
        conn.rollback()
        print(f"\n⚠️  Email '{email}' is already registered.")
        return None
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Error adding user: {e}")
        return None
    finally:
        conn.close()


# ══════════════════════════════════════════════════════════════
#  BOOKING OPERATIONS
# ══════════════════════════════════════════════════════════════

def create_booking(user_id: int, package_id: int,
                   hotel_id: int, transport_id: int):
    """
    Create a new booking inside an explicit transaction:
      1. Validate all referenced IDs exist.
      2. Auto-assign the first available tour guide.
      3. Calculate total_cost = package price + (hotel price × duration).
      4. Insert booking and flip guide status to 'Assigned'.
    Rolls back the entire transaction on any failure.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # ── Validate user ──
            cur.execute("SELECT user_id FROM Users WHERE user_id=%s",
                        (user_id,))
            if not cur.fetchone():
                print(f"\n⚠️  User ID {user_id} does not exist.")
                return

            # ── Validate package & get details ──
            cur.execute(
                "SELECT price, duration_days FROM Tour_Packages "
                "WHERE package_id=%s", (package_id,)
            )
            pkg = cur.fetchone()
            if not pkg:
                print(f"\n⚠️  Package ID {package_id} does not exist.")
                return

            # ── Validate hotel & get price ──
            cur.execute(
                "SELECT price_per_night FROM Hotels WHERE hotel_id=%s",
                (hotel_id,)
            )
            hotel = cur.fetchone()
            if not hotel:
                print(f"\n⚠️  Hotel ID {hotel_id} does not exist.")
                return

            # ── Validate transport ──
            cur.execute(
                "SELECT transport_id FROM Transportation "
                "WHERE transport_id=%s", (transport_id,)
            )
            if not cur.fetchone():
                print(f"\n⚠️  Transport ID {transport_id} does not exist.")
                return

            # ── Auto-assign available guide ──
            guide_id = _get_available_guide(cur)
            if guide_id is None:
                print("\n⚠️  No guides are currently available. "
                      "Please add or free a guide first.")
                return

            # ── Calculate total cost ──
            total_cost = (
                float(pkg["price"])
                + float(hotel["price_per_night"]) * int(pkg["duration_days"])
            )

            # ── Insert booking ──
            cur.execute(
                """INSERT INTO Bookings
                   (user_id, package_id, guide_id, hotel_id,
                    transport_id, booking_date, total_cost, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, 'Active')""",
                (user_id, package_id, guide_id, hotel_id,
                 transport_id, date.today(), total_cost),
            )

            # ── Mark guide as 'Assigned' ──
            cur.execute(
                "UPDATE Tour_Guides SET availability_status='Assigned' "
                "WHERE guide_id=%s", (guide_id,)
            )

        # ── Commit the whole transaction atomically ──
        conn.commit()
        print(f"\n✅ Booking created successfully!")
        print(f"   Booking ID   : {cur.lastrowid}")
        print(f"   Guide Assigned: ID {guide_id}")
        print(f"   Total Cost   : ₹{total_cost:,.2f}")

    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Booking failed (rolled back): {e}")
    finally:
        conn.close()


def view_active_bookings():
    """
    Display all active bookings using a multi-table INNER JOIN
    showing customer, package, guide, hotel, and transport info.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT
                    b.booking_id,
                    u.name          AS customer,
                    u.email,
                    tp.package_name AS package,
                    tp.destination,
                    tp.duration_days,
                    tg.name         AS guide,
                    tg.language_expertise,
                    h.hotel_name,
                    h.rating        AS hotel_rating,
                    t.vehicle_type,
                    t.driver_name,
                    b.booking_date,
                    b.total_cost,
                    b.status
                FROM Bookings b
                INNER JOIN Users u            ON b.user_id      = u.user_id
                INNER JOIN Tour_Packages tp   ON b.package_id   = tp.package_id
                INNER JOIN Tour_Guides tg     ON b.guide_id     = tg.guide_id
                INNER JOIN Hotels h           ON b.hotel_id     = h.hotel_id
                INNER JOIN Transportation t   ON b.transport_id = t.transport_id
                WHERE b.status = 'Active'
                ORDER BY b.booking_id
            """
            cur.execute(sql)
            rows = cur.fetchall()

        if not rows:
            print("\n📭 No active bookings found.")
            return

        for r in rows:
            print("\n" + "─" * 55)
            print(f"  Booking ID    : {r['booking_id']}")
            print(f"  Customer      : {r['customer']} ({r['email']})")
            print(f"  Package       : {r['package']} → {r['destination']}"
                  f" ({r['duration_days']} days)")
            print(f"  Guide         : {r['guide']}"
                  f" [{r['language_expertise']}]")
            print(f"  Hotel         : {r['hotel_name']}"
                  f" (★ {r['hotel_rating']})")
            print(f"  Transport     : {r['vehicle_type']}"
                  f" — Driver: {r['driver_name']}")
            print(f"  Booking Date  : {r['booking_date']}")
            print(f"  Total Cost    : ₹{r['total_cost']:,.2f}")
            print(f"  Status        : {r['status']}")
        print("─" * 55)

    except pymysql.MySQLError as e:
        print(f"\n❌ Error fetching bookings: {e}")
    finally:
        conn.close()


def cancel_booking(booking_id: int):
    """
    Cancel an active booking:
      1. Set booking status to 'Cancelled'.
      2. Release the assigned guide back to 'Available'.
    Uses an explicit transaction for atomicity.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # ── Fetch the booking ──
            cur.execute(
                "SELECT guide_id, status FROM Bookings WHERE booking_id=%s",
                (booking_id,),
            )
            booking = cur.fetchone()
            if not booking:
                print(f"\n⚠️  Booking ID {booking_id} not found.")
                return
            if booking["status"] == "Cancelled":
                print(f"\n⚠️  Booking ID {booking_id} is already cancelled.")
                return

            # ── Cancel the booking ──
            cur.execute(
                "UPDATE Bookings SET status='Cancelled' WHERE booking_id=%s",
                (booking_id,),
            )

            # ── Free the guide ──
            cur.execute(
                "UPDATE Tour_Guides SET availability_status='Available' "
                "WHERE guide_id=%s", (booking["guide_id"],)
            )

        conn.commit()
        print(f"\n✅ Booking ID {booking_id} cancelled. "
              f"Guide ID {booking['guide_id']} is now Available.")
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"\n❌ Cancellation failed (rolled back): {e}")
    finally:
        conn.close()
