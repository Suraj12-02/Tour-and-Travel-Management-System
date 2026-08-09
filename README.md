<div align="center">

# Tour & Travel Management System

A full-featured **Database Management System** built with **Python** and **MySQL** that allows travel agencies to manage tour packages, guides, hotels, transportation, customers, and bookings through an interactive command-line interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1)
![CLI](https://img.shields.io/badge/Interface-CLI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Example Workflow](#example-workflow)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Interactive CLI Menu** - A user-friendly terminal interface with nested sub-menus for every module.
- **Package Management** - Add, view, update, and delete tour packages.
- **Guide Management** - Register tour guides, view their profiles, and toggle availability status.
- **Booking Wizard** - Step-by-step guided booking process with live reference lists.
- **Smart Guide Assignment** - Automatically assigns the first *Available* guide to each new booking.
- **Automatic Cost Calculation** - Computes `total_cost = package price + (hotel price x duration)`.
- **Active Booking Reports** - View all active bookings with a multi-table `INNER JOIN` showing customer, package, guide, hotel, and transport detail.
- **Booking Cancellation** - Cancel bookings atomically and automatically release the assigned guide back to *Available*.
- **Automatic Schema Bootstrap** - Creates the database and all tables on first run.
- **Seed Data** - Populate all tables with realistic sample data for quick testing.
- **ACID Transactions** - Every multi-table write runs inside an explicit transaction with rollback on failure.
- **SQL Injection Protection** - All queries are fully parameterized.

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Language  | Python 3.8+                         |
| Database  | MySQL 8.0                           |
| Connector | `PyMySQL`                           |
| Interface | Command-Line Interface (Terminal)   |

---

## Project Structure

```
DBMS/
├── main.py            # Entry point - interactive CLI menu & main loop
├── db_config.py       # MySQL connection management & schema bootstrap
├── operations.py      # All CRUD, reporting & booking operations
├── schema.sql         # Relational database schema (DDL)
├── seed_data.py       # Populates tables with realistic sample data
├── .env               # Environment variables (ignored by git)
├── .gitignore         # Git ignore rules
└── requirements.txt   # Python dependencies  (optional)
```

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python** 3.8 or higher installed on your machine.
- **MySQL Server** 8.0 running locally or accessible remotely.
- Basic familiarity with the command line / terminal.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tour-travel-dbms.git
cd tour-travel-dbms
```

### 2. Create and activate a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pymysql python-dotenv
```

> **Note:** If you choose to use a `requirements.txt`, run `pip install -r requirements.txt` instead.

---

## Configuration

The application reads database credentials from environment variables using the configuration block in `db_config.py`. Create a `.env` file in the project root (already git-ignored) with the following values:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=tour_travel_db
DB_PORT=3306
```

| Variable      | Description                       | Example         |
|---------------|-----------------------------------|-----------------|
| `DB_HOST`     | MySQL server hostname             | `localhost`     |
| `DB_USER`     | MySQL username                    | `root`          |
| `DB_PASSWORD` | MySQL password                    | `secret123`     |
| `DB_NAME`     | Target database name              | `tour_travel_db`|
| `DB_PORT`     | MySQL port (default `3306`)       | `3306`          |

> **Note:** Ensure the module imports `os` and `dotenv` to load the `.env` file, or export these variables in your shell environment.

---

## Database Setup

The system handles database creation automatically. You have three options:

### Option A - Automatic bootstrap (recommended)

Just run the application, `main.py` calls `initialize_database()`, which creates the database and all tables if they don't already exist.

```bash
python main.py
```

### Option B - Initialize via config module

```bash
python db_config.py
```

### Option C - Manual schema import

If you prefer to create the schema manually:

```bash
mysql -u root -p < schema.sql
```

---

## Usage

### Run the application

```bash
python main.py
```

### Seed sample data (optional)

Populate all tables with realistic dummy data for testing:

```bash
python seed_data.py
```

### Main Menu

Upon launch, you'll see the main menu:

```
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
```

Select a number to navigate. Sub-menus are provided for **Packages**, **Guides**, and **Users**.

---

## Database Schema

The relational schema consists of **6 interconnected tables**. The `Bookings` table serves as the central transactional entity linking all others via foreign keys.

```
┌────────────┐      ┌──────────────────┐      ┌──────────────┐
│   Users    │      │  Tour_Packages   │      │  Tour_Guides │
├────────────┤      ├──────────────────┤      ├──────────────┤
│ user_id PK │      │ package_id PK    │      │ guide_id PK  │
│ name       │      │ package_name     │      │ name         │
│ email (UQ) │      │ destination      │      │ languages    │
│ phone      │      │ duration_days    │      │ availability │
└────────────┘      │ price            │      └──────────────┘
        │           └──────────────────┘              │
        │                │                            │
        └────────────────┼────────────────────────────┘
                         ▼
              ┌──────────────────────┐
              │       Bookings       │
              ├──────────────────────┤
              │ booking_id PK        │
              │ user_id     FK ──────│──── Users
              │ package_id  FK ──────│──── Tour_Packages
              │ guide_id    FK ──────│──── Tour_Guides
              │ hotel_id    FK ──────│──── Hotels
              │ transport_id FK ─────│──── Transportation
              │ booking_date         │
              │ total_cost           │
              │ status               │
              └──────────────────────┘

┌────────────┐                        ┌──────────────────┐
│   Hotels   │                        │ Transportation   │
├────────────┤                        ├──────────────────┤
│ hotel_id PK│                        │ transport_id PK  │
│ hotel_name │                        │ vehicle_type     │
│ location   │                        │ capacity         │
│ rating     │                        │ driver_name      │
│ price/night│                        └──────────────────┘
└────────────┘
```

### Table Details

| Table           | Purpose                                                      | Key Constraints          |
|-----------------|--------------------------------------------------------------|--------------------------|
| `Users`         | Registered customers                                         | `email` UNIQUE           |
| `Tour_Packages` | Available travel packages                                    | -                        |
| `Tour_Guides`   | Guide profiles & availability (`Available`/`Assigned`)       | `ENUM` status            |
| `Hotels`        | Partner hotels with ratings (1.0-5.0)                        | `CHECK` rating range     |
| `Transportation`| Vehicles & driver details                                    | -                        |
| `Bookings`      | Transactional records linking all entities                   | 5 FKs with `CASCADE`     |

---

## Security Features

- **Parameterized Queries** - Every SQL statement uses `%s` placeholders, fully preventing **SQL injection** attacks.
- **ACID Transactions** - Multi-step operations (booking creation, cancellation) run inside explicit transactions with `commit()`/`rollback()` for data integrity.
- **Foreign Key Integrity** - `ON DELETE CASCADE` ensures referential integrity when related records are removed.
- **Safe Error Handling** - Meaningful, user-friendly error messages are shown without leaking stack traces.
- **Credentials Protection** - Database credentials are stored in `.env` and excluded from version control via `.gitignore`.

---

## Example Workflow

1. **Run the app** - `python main.py` (database auto-creates).
2. **Seed data** - `python seed_data.py` (optional, loads sample users, packages, guides, hotels, transport).
3. **Register a user** - Main Menu - **8. Manage Users** - **1. Register New User**.
4. **Add a package** - Main Menu - **1. Manage Packages** - **1. Add Package**.
5. **Create a booking** - Main Menu - **3. Create New Booking** - follow the wizard selecting a user, package, hotel, and transport. The system auto-assigns an available guide and calculates the total cost.
6. **View bookings** - Main Menu - **4. View All Active Bookings**.
7. **Cancel a booking** - Main Menu - **5. Cancel a Booking** - the guide is released back to *Available*.

---

## Troubleshooting

| Problem                                   | Solution                                                                    |
|-------------------------------------------|-----------------------------------------------------------------------------|
| `Could not connect to MySQL`              | Verify MySQL is running and `.env` credentials are correct.                 |
| `host 'x' is not allowed to connect`      | Ensure the MySQL user has remote-access privileges if connecting remotely.  |
| `ModuleNotFoundError: pymysql`            | Install dependencies: `pip install pymysql python-dotenv`.                  |
| `NameError: name 'os' is not defined`     | Add `import os` and `from dotenv import load_dotenv` to `db_config.py`.    |
| No results in booking wizard              | Register users and add packages/guides first (or run the seed script).      |
| `No guides are currently available`       | Add guides or cancel existing bookings to free up availability.             |

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with Python & MySQL
</div>
