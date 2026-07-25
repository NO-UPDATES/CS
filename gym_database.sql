-- ==========================================
-- GYM MANAGEMENT SYSTEM DATABASE SCRIPT
-- ==========================================

DROP DATABASE IF EXISTS gym;
CREATE DATABASE gym;
USE gym;

START TRANSACTION;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- MEMBERS TABLE
CREATE TABLE members (
    regdno INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20),
    membership VARCHAR(50),
    phone VARCHAR(20)
) ENGINE=InnoDB;

-- TRAINERS TABLE
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    salary DECIMAL(10,2)
) ENGINE=InnoDB;

-- ATTENDANCE TABLE
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    check_in_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (member_id) REFERENCES members(regdno) ON DELETE CASCADE
) ENGINE=InnoDB;

-- PAYMENTS TABLE
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    amount DECIMAL(10,2),
    payment_date DATE,
    method VARCHAR(50),
    FOREIGN KEY (member_id) REFERENCES members(regdno) ON DELETE CASCADE
) ENGINE=InnoDB;

-- DEFAULT ADMIN ACCOUNT
INSERT INTO users (username, password) VALUES ('admin', 'admin123');

COMMIT;
