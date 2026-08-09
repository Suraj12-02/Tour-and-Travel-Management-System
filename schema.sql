-- ============================================================
-- Tour and Travel Management System - Database Schema
-- Database: tour_travel_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS tour_travel_db;
USE tour_travel_db;

-- ------------------------------------------------------------
-- Table: Users / Customers
-- Stores registered customer information.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100)  NOT NULL,
    email         VARCHAR(150)  NOT NULL UNIQUE,
    phone         VARCHAR(15)   NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: Tour_Packages
-- Stores available travel packages offered by the agency.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Tour_Packages (
    package_id    INT AUTO_INCREMENT PRIMARY KEY,
    package_name  VARCHAR(150)  NOT NULL,
    destination   VARCHAR(150)  NOT NULL,
    duration_days INT           NOT NULL,
    price         DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: Tour_Guides
-- Stores guide profiles and their current availability.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Tour_Guides (
    guide_id            INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(100) NOT NULL,
    language_expertise  VARCHAR(200) NOT NULL,
    availability_status ENUM('Available', 'Assigned') NOT NULL DEFAULT 'Available'
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: Hotels
-- Stores partner hotel information.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Hotels (
    hotel_id        INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name      VARCHAR(150)  NOT NULL,
    location        VARCHAR(150)  NOT NULL,
    rating          DECIMAL(2,1)  NOT NULL CHECK (rating BETWEEN 1.0 AND 5.0),
    price_per_night DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: Transportation
-- Stores available transport vehicles and driver details.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Transportation (
    transport_id  INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_type  VARCHAR(50)  NOT NULL,
    capacity      INT          NOT NULL,
    driver_name   VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: Bookings
-- Central transactional table linking customers to packages,
-- guides, hotels, and transport with CASCADE delete rules.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT            NOT NULL,
    package_id    INT            NOT NULL,
    guide_id      INT            NOT NULL,
    hotel_id      INT            NOT NULL,
    transport_id  INT            NOT NULL,
    booking_date  DATE           NOT NULL,
    total_cost    DECIMAL(12,2)  NOT NULL,
    status        ENUM('Active', 'Cancelled') NOT NULL DEFAULT 'Active',

    FOREIGN KEY (user_id)      REFERENCES Users(user_id)            ON DELETE CASCADE,
    FOREIGN KEY (package_id)   REFERENCES Tour_Packages(package_id) ON DELETE CASCADE,
    FOREIGN KEY (guide_id)     REFERENCES Tour_Guides(guide_id)     ON DELETE CASCADE,
    FOREIGN KEY (hotel_id)     REFERENCES Hotels(hotel_id)          ON DELETE CASCADE,
    FOREIGN KEY (transport_id) REFERENCES Transportation(transport_id) ON DELETE CASCADE
) ENGINE=InnoDB;
