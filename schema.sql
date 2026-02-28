CREATE DATABASE IF NOT EXISTS layered_payment_system;
USE layered_payment_system;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(60) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    wallet_uid VARCHAR(36) NOT NULL UNIQUE,
    bank_uid VARCHAR(20) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wallet (
    wallet_uid VARCHAR(36) PRIMARY KEY,
    balance FLOAT NOT NULL DEFAULT 0,
    CONSTRAINT fk_wallet_user FOREIGN KEY (wallet_uid) REFERENCES users(wallet_uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS bank_account (
    bank_uid VARCHAR(20) PRIMARY KEY,
    balance FLOAT NOT NULL DEFAULT 0,
    CONSTRAINT fk_bank_user FOREIGN KEY (bank_uid) REFERENCES users(bank_uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id VARCHAR(50) PRIMARY KEY,
    sender_uid VARCHAR(36) NOT NULL,
    receiver_uid VARCHAR(36) NOT NULL,
    amount FLOAT NOT NULL,
    txn_type VARCHAR(30) NOT NULL,
    date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL
);
