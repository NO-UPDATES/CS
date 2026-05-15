CREATE DATABASE IF NOT EXISTS gym;
USE gym;

CREATE TABLE IF NOT EXISTS admin (
    username VARCHAR(30),
    password VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS members (
    regdno VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15),
    membership VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS items (
    itemid INT PRIMARY KEY AUTO_INCREMENT,
    itemname VARCHAR(100),
    quantity INT
);

CREATE TABLE IF NOT EXISTS trainers (
    trainerid INT PRIMARY KEY AUTO_INCREMENT,
    trainername VARCHAR(50),
    specialization VARCHAR(50),
    rating FLOAT
);

CREATE TABLE IF NOT EXISTS payments (
    paymentid INT PRIMARY KEY AUTO_INCREMENT,
    regdno VARCHAR(20),
    paymentstatus VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS logs (
    logid INT PRIMARY KEY AUTO_INCREMENT,
    regdno VARCHAR(20),
    intime DATETIME,
    outtime DATETIME
);

DELETE FROM admin;
INSERT INTO admin(username,password) VALUES ('admin','admin123');

DELETE FROM items;
INSERT INTO items(itemname,quantity) VALUES
('2KG Dumbbells', 24),
('5KG Dumbbells', 20),
('10KG Dumbbells', 18),
('20KG Olympic Barbell', 8),
('Adjustable Bench Press', 6),
('Incline Bench', 5),
('Cable Crossover Machine', 2),
('Smith Machine', 2),
('Leg Press Machine', 3),
('Lat Pulldown Machine', 3),
('Treadmill Pro X1', 7),
('Exercise Cycle', 6),
('Rowing Machine', 4),
('EZ Curl Rod', 10),
('Squat Rack', 4);

DELETE FROM trainers;
INSERT INTO trainers(trainername,specialization,rating) VALUES
('Arun', 'Strength Training', 4.8),
('Vijay', 'Cardio Fitness', 4.5),
('Karthik', 'Weight Loss', 4.7),
('Neha', 'Yoga Coach', 4.6),
('Rahul', 'Functional Training', 4.4);
