"""
main.py
───────
Interactive CLI menu for the Tour & Travel Management System.
Bootstraps the database on first run and exposes all
administrative operations via a numbered menu.
"""

from db_config import initialize_database
from operations import (
    add_package, view_packages, update_package, delete_package,
    add_guide, view_guides, update_guide_availability,
    view_hotels, view_transport, view_users, add_user,
    create_booking, view_active_bookings, cancel_booking,
)


BANNER = r"""
╔═══════════════════════════════════════════════════════════╗
║       🌍  TOUR & TRAVEL MANAGEMENT SYSTEM  🌍            ║
╚═══════════════════════════════════════════════════════════╝
"""

MAIN_MENU = """
┌─────────────────────────────────────┐
│           MAIN MENU                 │
├─────────────────────────────────────┤
│  1. Manage Packages                 │
│  2. Manage Tour Guides              │
│  3. Create New Booking              │
│  4. View All Active Bookings        │
│  5. Cancel a Booking                │
│  6. View Hotels                     │
│  7. View Transport Options          │
│  8. Manage Users                    │
│  9. Exit                            │
└─────────────────────────────────────┘
"""

PKG_MENU = """
  ┌── Package Menu ──────────────────┐
  │  1. Add Package                  │
  │  2. View All Packages            │
  │  3. Update Package               │
  │  4. Delete Package               │
  │  5. Back to Main Menu            │
  └──────────────────────────────────┘
"""

GUIDE_MENU = """
  ┌── Guide Menu ────────────────────┐
  │  1. Add Guide                    │
  │  2. View All Guides              │
  │  3. Update Guide Availability    │
  │  4. Back to Main Menu            │
  └──────────────────────────────────┘
"""

USER_MENU = """
  ┌── User Menu ─────────────────────┐
  │  1. Register New User            │
  │  2. View All Users               │
  │  3. Back to Main Menu            │
  └──────────────────────────────────┘
"""


# ── Helper ────────────────────────────────────────────────────
def _input_int(prompt: str) -> int:
    """Prompt until a valid integer is entered."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  ⚠️  Please enter a valid integer.")


def _input_float(prompt: str) -> float:
    """Prompt until a valid float is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


# ══════════════════════════════════════════════════════════════
#  SUB-MENUS
# ══════════════════════════════════════════════════════════════

def package_menu():
    """Package management sub-menu loop."""
    while True:
        print(PKG_MENU)
        choice = input("  Select option: ").strip()

        if choice == "1":
            name = input("  Package name : ").strip()
            dest = input("  Destination  : ").strip()
            days = _input_int("  Duration (days): ")
            price = _input_float("  Price (₹)    : ")
            add_package(name, dest, days, price)

        elif choice == "2":
            view_packages()

        elif choice == "3":
            view_packages()
            pid = _input_int("  Package ID to update: ")
            name = input("  New name       : ").strip()
            dest = input("  New destination: ").strip()
            days = _input_int("  New duration   : ")
            price = _input_float("  New price (₹)  : ")
            update_package(pid, name, dest, days, price)

        elif choice == "4":
            view_packages()
            pid = _input_int("  Package ID to delete: ")
            confirm = input(
                f"  ⚠️  Delete package {pid}? (y/n): "
            ).strip().lower()
            if confirm == "y":
                delete_package(pid)

        elif choice == "5":
            break
        else:
            print("  ⚠️  Invalid option.")


def guide_menu():
    """Guide management sub-menu loop."""
    while True:
        print(GUIDE_MENU)
        choice = input("  Select option: ").strip()

        if choice == "1":
            name = input("  Guide name       : ").strip()
            langs = input("  Languages (csv)  : ").strip()
            add_guide(name, langs)

        elif choice == "2":
            view_guides()

        elif choice == "3":
            view_guides()
            gid = _input_int("  Guide ID : ")
            print("  1. Available")
            print("  2. Assigned")
            s = input("  New status (1/2): ").strip()
            status = "Available" if s == "1" else "Assigned"
            update_guide_availability(gid, status)

        elif choice == "4":
            break
        else:
            print("  ⚠️  Invalid option.")


def user_menu():
    """User management sub-menu loop."""
    while True:
        print(USER_MENU)
        choice = input("  Select option: ").strip()

        if choice == "1":
            name = input("  Full name : ").strip()
            email = input("  Email     : ").strip()
            phone = input("  Phone     : ").strip()
            add_user(name, email, phone)

        elif choice == "2":
            view_users()

        elif choice == "3":
            break
        else:
            print("  ⚠️  Invalid option.")


def booking_wizard():
    """Step-by-step booking creation with live selection lists."""
    print("\n── 📝 New Booking Wizard ──")

    # Step 1 – Select user
    users = view_users()
    if not users:
        print("  Register a user first (Main Menu → 8).")
        return
    uid = _input_int("  Select User ID   : ")

    # Step 2 – Select package
    pkgs = view_packages()
    if not pkgs:
        print("  Add a package first (Main Menu → 1).")
        return
    pid = _input_int("  Select Package ID: ")

    # Step 3 – Select hotel
    hotels = view_hotels()
    if not hotels:
        print("  Add hotels via seed data first.")
        return
    hid = _input_int("  Select Hotel ID  : ")

    # Step 4 – Select transport
    trans = view_transport()
    if not trans:
        print("  Add transport options via seed data first.")
        return
    tid = _input_int("  Select Transport ID: ")

    # Step 5 – Create
    create_booking(uid, pid, hid, tid)


# ══════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════

def main():
    print(BANNER)
    print("Initializing database …")
    initialize_database()

    while True:
        print(MAIN_MENU)
        choice = input("Select option: ").strip()

        if choice == "1":
            package_menu()
        elif choice == "2":
            guide_menu()
        elif choice == "3":
            booking_wizard()
        elif choice == "4":
            view_active_bookings()
        elif choice == "5":
            bid = _input_int("  Booking ID to cancel: ")
            confirm = input(
                f"  ⚠️  Cancel booking {bid}? (y/n): "
            ).strip().lower()
            if confirm == "y":
                cancel_booking(bid)
        elif choice == "6":
            view_hotels()
        elif choice == "7":
            view_transport()
        elif choice == "8":
            user_menu()
        elif choice == "9":
            print("\n👋 Goodbye! Thank you for using the system.\n")
            break
        else:
            print("⚠️  Invalid option. Please try again.")


if __name__ == "__main__":
    main()
