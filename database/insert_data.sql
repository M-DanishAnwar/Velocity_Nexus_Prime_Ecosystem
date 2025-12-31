USE VelocityNexusPrime;
GO

-- Insert Manufacturers
INSERT INTO Manufacturers (name, country, founded_year, is_luxury, market_segment) VALUES
('Toyota', 'Japan', 1937, 0, 'Global'),
('Honda', 'Japan', 1948, 0, 'Global'),
('Suzuki', 'Japan', 1909, 0, 'Regional'),
('MG Motors', 'UK/China', 1924, 1, 'Regional'),
('BMW', 'Germany', 1916, 1, 'Global'),
('Mercedes-Benz', 'Germany', 1926, 1, 'Global'),
('Audi', 'Germany', 1909, 1, 'Global'),
('Tesla', 'USA', 2003, 1, 'Global'),
('Hyundai', 'South Korea', 1967, 0, 'Global'),
('Kia', 'South Korea', 1944, 0, 'Global'),
('Proton', 'Malaysia', 1983, 0, 'Regional'),
('Chery', 'China', 1997, 0, 'Regional');
GO

-- Insert Vehicle Types
INSERT INTO VehicleTypes (type_name, category, description) VALUES
('Hypercar', 'Hypercar', 'Ultra-high performance sports cars'),
('Sports Car', 'Sports', 'High-performance two-seaters'),
('Luxury Sedan', 'Luxury', 'Premium comfort sedans'),
('Executive Sedan', 'Sedan', 'Business class sedans'),
('Family SUV', 'SUV', 'Family sports utility vehicles'),
('Compact SUV', 'SUV', 'Small crossover SUVs'),
('Hatchback', 'Hatchback', 'Compact city cars'),
('MPV', 'Commercial', 'Multi-purpose vehicles'),
('Pickup Truck', 'Commercial', 'Utility pickup trucks'),
('Electric Vehicle', 'Sedan', 'Fully electric vehicles');
GO

-- Insert Vehicle Models
INSERT INTO VehicleModels (manufacturer_id, type_id, model_name, generation, body_style, engine_capacity_cc, horsepower, fuel_type, base_price) VALUES
-- Toyota
(1, 4, 'Corolla', '2024', 'Sedan', 1800, 139, 'Petrol', 4500000),
(1, 6, 'Fortuner', '2023', 'SUV', 2755, 201, 'Diesel', 12500000),
(1, 9, 'Hilux', '2024', 'Pickup', 2755, 201, 'Diesel', 8500000),
(1, 7, 'Yaris', '2024', 'Hatchback', 1500, 106, 'Petrol', 3200000),

-- Honda
(2, 4, 'Civic', '2024', 'Sedan', 1800, 173, 'Petrol', 6500000),
(2, 4, 'City', '2024', 'Sedan', 1500, 119, 'Petrol', 4200000),
(2, 6, 'HR-V', '2024', 'SUV', 1500, 119, 'Petrol', 5800000),

-- Suzuki
(3, 7, 'Alto', '2024', 'Hatchback', 660, 48, 'Petrol', 2200000),
(3, 7, 'Cultus', '2024', 'Hatchback', 1000, 67, 'Petrol', 2800000),
(3, 6, 'Swift', '2024', 'Hatchback', 1300, 90, 'Petrol', 3500000),

-- MG Motors
(4, 10, 'ZS EV', '2024', 'SUV', 0, 174, 'Electric', 8500000),
(4, 6, 'HS', '2024', 'SUV', 1500, 160, 'Petrol', 7500000),

-- BMW
(5, 3, '5 Series', '2024', 'Sedan', 2000, 248, 'Petrol', 25000000),
(5, 2, 'M4', '2024', 'Coupe', 3000, 473, 'Petrol', 35000000),

-- Mercedes
(6, 3, 'S-Class', '2024', 'Sedan', 3000, 362, 'Petrol', 45000000),
(6, 5, 'GLE', '2024', 'SUV', 3000, 362, 'Petrol', 32000000),

-- Tesla
(8, 10, 'Model 3', '2024', 'Sedan', 0, 283, 'Electric', 22000000),
(8, 10, 'Model Y', '2024', 'SUV', 0, 384, 'Electric', 28000000);
GO

-- Insert Dealerships
INSERT INTO Dealerships (name, location, city, province, phone, email, manager_name, total_capacity) VALUES
('Toyota Lahore Central', 'MM Alam Road, Gulberg', 'Lahore', 'Punjab', '+92 42 111 111 111', 'info@toyota-lahore.com', 'Ahmed Raza', 100),
('Honda Fort Motors', 'Fortress Stadium', 'Lahore', 'Punjab', '+92 42 222 222 222', 'sales@hondafort.com', 'Bilal Ahmed', 80),
('Suzuki Automall', 'Ferozepur Road', 'Lahore', 'Punjab', '+92 42 333 333 333', 'info@suzukiautomall.com', 'Kamran Ali', 60),
('MG Exclusive', 'DHA Phase 5', 'Lahore', 'Punjab', '+92 42 444 444 444', 'mg@exclusive.com', 'Saad Malik', 40),
('Premium Motors Karachi', 'Clifton Road', 'Karachi', 'Sindh', '+92 21 555 555 555', 'info@premiummotors.com', 'Faisal Khan', 120),
('Islamabad Auto Hub', 'Blue Area', 'Islamabad', 'ICT', '+92 51 666 666 666', 'hub@islamabadauto.com', 'Usman Tariq', 90);
GO

-- Insert Employees
INSERT INTO Employees (dealership_id, first_name, last_name, email, phone, position, hire_date, salary, commission_rate) VALUES
(1, 'Ali', 'Hassan', 'ali.hassan@toyota.com', '+92 300 1111111', 'Sales Executive', '2023-01-15', 80000, 5.0),
(1, 'Sara', 'Ahmed', 'sara.ahmed@toyota.com', '+92 300 2222222', 'Sales Executive', '2023-03-20', 85000, 5.5),
(2, 'Omar', 'Farooq', 'omar.farooq@honda.com', '+92 300 3333333', 'Manager', '2022-06-10', 150000, 3.0),
(2, 'Fatima', 'Khan', 'fatima.khan@honda.com', '+92 300 4444444', 'Finance Officer', '2023-02-15', 120000, 2.0),
(3, 'Zain', 'Ali', 'zain.ali@suzuki.com', '+92 300 5555555', 'Sales Executive', '2024-01-10', 70000, 4.5),
(4, 'Ayesha', 'Malik', 'ayesha.malik@mg.com', '+92 300 6666666', 'Sales Executive', '2023-11-01', 90000, 6.0),
(5, 'Haris', 'Rafiq', 'haris.rafiq@premium.com', '+92 300 7777777', 'Manager', '2021-08-15', 180000, 4.0),
(6, 'Nadia', 'Shah', 'nadia.shah@hub.com', '+92 300 8888888', 'Sales Executive', '2023-09-01', 95000, 5.5);
GO

-- Insert Customers
INSERT INTO Customers (first_name, last_name, email, phone, cnic, address, city, province, date_of_birth, customer_type, is_vip) VALUES
('Muhammad', 'Ahmed', 'm.ahmed@email.com', '+92 301 1111111', '35201-1234567-8', 'DHA Phase 5', 'Lahore', 'Punjab', '1985-06-15', 'Individual', 1),
('Fatima', 'Raza', 'fatima.raza@email.com', '+92 301 2222222', '35201-2345678-9', 'Gulberg III', 'Lahore', 'Punjab', '1990-03-22', 'Individual', 0),
('Ali', 'Khan', 'ali.khan@company.com', '+92 301 3333333', '35201-3456789-0', 'Cantt', 'Lahore', 'Punjab', '1978-11-30', 'Corporate', 1),
('Sara', 'Malik', 'sara.malik@email.com', '+92 301 4444444', '35201-4567890-1', 'Model Town', 'Lahore', 'Punjab', '1995-08-14', 'Individual', 0),
('Bilal', 'Arif', 'bilal.arif@business.com', '+92 301 5555555', '35201-5678901-2', 'Bahria Town', 'Lahore', 'Punjab', '1982-12-05', 'Corporate', 1),
('Ayesha', 'Butt', 'ayesha.butt@email.com', '+92 301 6666666', '35201-6789012-3', 'Johar Town', 'Lahore', 'Punjab', '1992-02-28', 'Individual', 0),
('Usman', 'Haq', 'usman.haq@gov.pk', '+92 301 7777777', '35201-7890123-4', 'Islamabad', 'ICT', '1975-07-19', 'Government', 1),
('Zainab', 'Ali', 'zainab.ali@email.com', '+92 301 8888888', '35201-8901234-5', 'Karachi', 'Sindh', '1988-04-10', 'Individual', 0);
GO

-- Insert Vehicles (Inventory)
INSERT INTO Vehicles (model_id, dealership_id, vin, chassis_number, color, manufacturing_year, mileage_km, purchase_price, current_price, status, import_status) VALUES
-- Toyota Corollas
(1, 1, 'JTNK4MEB8L1012345', 'CH123456', 'White Pearl', 2024, 50, 3800000, 4500000, 'Available', 'Local'),
(1, 1, 'JTNK4MEB8L1012346', 'CH123457', 'Silver Metallic', 2024, 120, 3850000, 4550000, 'Available', 'Local'),
(1, 1, 'JTNK4MEB8L1012347', 'CH123458', 'Black', 2024, 80, 3820000, 4520000, 'Test Drive', 'Local'),

-- Honda Civics
(5, 2, '2HGFC2F56LH543210', 'CH223456', 'Platinum White', 2024, 100, 5000000, 6500000, 'Available', 'Local'),
(5, 2, '2HGFC2F56LH543211', 'CH223457', 'Crystal Black', 2024, 150, 5050000, 6550000, 'Reserved', 'Local'),

-- Suzuki Alto
(8, 3, 'JS3TB4NV9P4100001', 'CH323456', 'Super White', 2024, 200, 1500000, 2200000, 'Available', 'Local'),
(8, 3, 'JS3TB4NV9P4100002', 'CH323457', 'Silver', 2024, 180, 1520000, 2220000, 'Available', 'Local'),

-- MG ZS EV
(12, 4, 'LSJA24W39JN000001', 'CH423456', 'Metallic Red', 2024, 50, 6500000, 8500000, 'Available', 'CBU'),
(12, 4, 'LSJA24W39JN000002', 'CH423457', 'Starry Black', 2024, 30, 6550000, 8550000, 'Available', 'CBU'),

-- BMW 5 Series
(14, 5, 'WBA5E1C50JDP12345', 'CH523456', 'Mineral White', 2024, 20, 20000000, 25000000, 'Available', 'Imported'),
(14, 5, 'WBA5E1C50JDP12346', 'CH523457', 'Carbon Black', 2024, 15, 20500000, 25500000, 'Available', 'Imported'),

-- Mercedes S-Class
(16, 5, 'WDDZF8DB2LA123456', 'CH623456', 'Obsidian Black', 2024, 10, 35000000, 45000000, 'Available', 'Imported'),

-- Tesla Model 3
(18, 6, '5YJ3E1EA0NF123456', 'CH723456', 'Midnight Silver', 2024, 5, 18000000, 22000000, 'Available', 'Imported');
GO

-- Insert Sales Records
INSERT INTO Sales (vehicle_id, customer_id, employee_id, sale_price, base_price, tax_amount, final_amount, commission_amount, payment_method, sale_status) VALUES
(1, 1, 1, 4500000, 4500000, 765000, 5265000, 225000, 'Bank Transfer', 'Completed'),
(4, 2, 2, 6500000, 6500000, 1105000, 7605000, 357500, 'Financing', 'Completed'),
(7, 3, 5, 2200000, 2200000, 374000, 2574000, 110000, 'Cash', 'Completed'),
(11, 4, 6, 25000000, 25000000, 4250000, 29250000, 1375000, 'Bank Transfer', 'Completed');
GO

-- Insert Service Records
INSERT INTO ServiceRecords (vehicle_id, service_date, service_type, description, cost, parts_cost, labor_cost, service_center) VALUES
(1, '2024-01-15', 'Regular Maintenance', 'First 1000km service - Oil change, filter replacement', 5000, 3000, 2000, 'Toyota Service Center Lahore'),
(2, '2024-02-20', 'Oil Change', 'Engine oil change and general inspection', 3500, 2000, 1500, 'Toyota Service Center Lahore'),
(4, '2024-03-10', 'Brake Service', 'Brake pad replacement and fluid change', 8000, 5000, 3000, 'Honda Service Center');
GO

-- Insert Test Drives
INSERT INTO TestDrives (vehicle_id, customer_id, employee_id, scheduled_date, status, feedback, rating) VALUES
(3, 5, 1, '2024-12-15 14:00:00', 'Completed', 'Smooth ride, comfortable interior', 5),
(6, 6, 2, '2024-12-16 11:00:00', 'Scheduled', NULL, NULL),
(9, 7, 3, '2024-12-17 16:00:00', 'Completed', 'Excellent electric vehicle, quiet and powerful', 5);
GO

-- Insert Price History
INSERT INTO PriceHistory (vehicle_id, old_price, new_price, change_reason, changed_by) VALUES
(1, 4400000, 4500000, 'Market Adjustment', 1),
(4, 6400000, 6500000, 'Demand Increase', 2),
(11, 24500000, 25000000, 'Currency Fluctuation', 6);
GO

-- Insert Credit Scores
INSERT INTO CreditScores (customer_id, score, rating, provider) VALUES
(1, 780, 'Excellent', 'CreditInfo'),
(2, 650, 'Good', 'CreditInfo'),
(3, 820, 'Excellent', 'DFCR'),
(4, 580, 'Fair', 'CreditInfo'),
(5, 720, 'Very Good', 'DFCR'),
(6, 630, 'Good', 'CreditInfo');
GO

-- Insert Payments
INSERT INTO Payments (sale_id, amount, payment_method, transaction_id, bank_name) VALUES
(1, 5265000, 'Bank Transfer', 'BT20241215001', 'HBL'),
(2, 3000000, 'Cash', 'CASH20241215001', NULL),
(2, 4605000, 'Financing', 'FIN20241215001', 'MCB'),
(3, 2574000, 'Cash', 'CASH20241216001', NULL),
(4, 29250000, 'Bank Transfer', 'BT20241217001', 'UBL');
GO

PRINT '✅ Sample data inserted successfully!';
GO
PRINT '📊 Database now contains:';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM Manufacturers) AS VARCHAR) + ' Manufacturers';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM VehicleModels) AS VARCHAR) + ' Vehicle Models';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM Vehicles) AS VARCHAR) + ' Vehicles in Inventory';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM Customers) AS VARCHAR) + ' Customers';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM Sales) AS VARCHAR) + ' Sales Records';
PRINT '   • ' + CAST((SELECT COUNT(*) FROM Employees) AS VARCHAR) + ' Employees';
GO