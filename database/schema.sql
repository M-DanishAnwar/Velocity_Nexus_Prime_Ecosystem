-- ============================================================
-- VELOCITY NEXUS PRIME - COMPLETE DATABASE SCHEMA
-- 3NF Normalized | 12+ Tables | Advanced Features
-- ============================================================

USE master;
GO

-- Create database if not exists
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'VelocityNexusPrime')
BEGIN
    CREATE DATABASE VelocityNexusPrime;
    PRINT '✅ Database created successfully!';
END
ELSE
BEGIN
    PRINT 'ℹ️ Database already exists.';
END
GO

USE VelocityNexusPrime;
GO

-- ==================== 1. MANUFACTURERS (1NF) ====================
CREATE TABLE Manufacturers (
    manufacturer_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL UNIQUE,
    country NVARCHAR(50) NOT NULL,
    founded_year INT,
    is_luxury BIT DEFAULT 0,
    market_segment NVARCHAR(30) CHECK (market_segment IN ('Global', 'Regional', 'Local')),
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 2. VEHICLE_TYPES (Lookup Table) ====================
CREATE TABLE VehicleTypes (
    type_id INT PRIMARY KEY IDENTITY(1,1),
    type_name NVARCHAR(50) NOT NULL UNIQUE,
    category NVARCHAR(30) CHECK (category IN ('Hypercar', 'Sports', 'Luxury', 'SUV', 'Sedan', 'Hatchback', 'Commercial')),
    description NVARCHAR(200)
);
GO

-- ==================== 3. VEHICLE_MODELS (2NF - Separated from Manufacturers) ====================
CREATE TABLE VehicleModels (
    model_id INT PRIMARY KEY IDENTITY(1,1),
    manufacturer_id INT NOT NULL FOREIGN KEY REFERENCES Manufacturers(manufacturer_id),
    type_id INT NOT NULL FOREIGN KEY REFERENCES VehicleTypes(type_id),
    model_name NVARCHAR(100) NOT NULL,
    generation NVARCHAR(20),
    body_style NVARCHAR(30),
    engine_capacity_cc INT,
    horsepower INT,
    fuel_type NVARCHAR(20) CHECK (fuel_type IN ('Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG')),
    transmission NVARCHAR(20) DEFAULT 'Automatic',
    seating_capacity INT DEFAULT 5,
    base_price DECIMAL(12,2) NOT NULL,
    production_year INT,
    created_date DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT UQ_ModelName_Manufacturer UNIQUE (manufacturer_id, model_name, generation)
);
GO

-- ==================== 4. DEALERSHIPS (Physical Locations) ====================
CREATE TABLE Dealerships (
    dealership_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL,
    location NVARCHAR(150) NOT NULL,
    city NVARCHAR(50) NOT NULL,
    province NVARCHAR(50) NOT NULL,
    phone NVARCHAR(20),
    email NVARCHAR(100),
    manager_name NVARCHAR(100),
    total_capacity INT DEFAULT 50,
    current_stock INT DEFAULT 0,
    is_active BIT DEFAULT 1,
    created_date DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CHK_StockCapacity CHECK (current_stock <= total_capacity)
);
GO

-- ==================== 5. EMPLOYEES (Staff Management) ====================
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY IDENTITY(1,1),
    dealership_id INT NOT NULL FOREIGN KEY REFERENCES Dealerships(dealership_id),
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    phone NVARCHAR(20),
    position NVARCHAR(50) CHECK (position IN ('Manager', 'Sales Executive', 'Finance Officer', 'Service Technician', 'Admin')),
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2),
    commission_rate DECIMAL(5,2) DEFAULT 5.0,
    is_active BIT DEFAULT 1,
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 6. CUSTOMERS (3NF - No Transitive Dependencies) ====================
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY IDENTITY(1,1),
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE,
    phone NVARCHAR(20) NOT NULL,
    cnic NVARCHAR(15) UNIQUE NOT NULL,
    address NVARCHAR(200),
    city NVARCHAR(50),
    province NVARCHAR(50),
    date_of_birth DATE,
    registration_date DATE DEFAULT GETDATE(),
    last_purchase_date DATE,
    total_purchases INT DEFAULT 0,
    total_spent DECIMAL(15,2) DEFAULT 0.00,
    customer_type NVARCHAR(20) DEFAULT 'Individual' CHECK (customer_type IN ('Individual', 'Corporate', 'Government')),
    is_vip BIT DEFAULT 0,
    notes NVARCHAR(500),
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 7. VEHICLES (Physical Inventory) ====================
CREATE TABLE Vehicles (
    vehicle_id INT PRIMARY KEY IDENTITY(1,1),
    model_id INT NOT NULL FOREIGN KEY REFERENCES VehicleModels(model_id),
    dealership_id INT NOT NULL FOREIGN KEY REFERENCES Dealerships(dealership_id),
    vin NVARCHAR(17) UNIQUE NOT NULL CHECK (LEN(vin) = 17),
    chassis_number NVARCHAR(50) UNIQUE,
    color NVARCHAR(30) NOT NULL,
    manufacturing_year INT NOT NULL CHECK (manufacturing_year BETWEEN 2000 AND 2025),
    registration_number NVARCHAR(20),
    mileage_km INT DEFAULT 0,
    purchase_price DECIMAL(12,2) NOT NULL,
    current_price DECIMAL(12,2) NOT NULL,
    status NVARCHAR(20) DEFAULT 'Available' CHECK (status IN ('Available', 'Sold', 'Reserved', 'Test Drive', 'Under Maintenance')),
    import_status NVARCHAR(20) DEFAULT 'Local' CHECK (import_status IN ('Local', 'Imported', 'CBU')),
    condition NVARCHAR(20) DEFAULT 'New' CHECK (condition IN ('New', 'Used', 'Certified Pre-Owned')),
    arrival_date DATE DEFAULT GETDATE(),
    sold_date DATE,
    created_date DATETIME DEFAULT GETDATE(),
    last_updated DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CHK_Price CHECK (current_price > 0),
    CONSTRAINT CHK_Mileage CHECK (mileage_km >= 0)
);
GO

-- ==================== 8. SALES (Transaction Records) ====================
CREATE TABLE Sales (
    sale_id INT PRIMARY KEY IDENTITY(1,1),
    vehicle_id INT NOT NULL FOREIGN KEY REFERENCES Vehicles(vehicle_id),
    customer_id INT NOT NULL FOREIGN KEY REFERENCES Customers(customer_id),
    employee_id INT NOT NULL FOREIGN KEY REFERENCES Employees(employee_id),
    sale_date DATETIME DEFAULT GETDATE(),
    sale_price DECIMAL(12,2) NOT NULL,
    base_price DECIMAL(12,2) NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 17.0,
    tax_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(12,2) NOT NULL,
    commission_rate DECIMAL(5,2) DEFAULT 5.0,
    commission_amount DECIMAL(10,2) NOT NULL,
    payment_method NVARCHAR(30) CHECK (payment_method IN ('Cash', 'Bank Transfer', 'Credit Card', 'Financing', 'Lease')),
    financing_details NVARCHAR(500),
    sale_status NVARCHAR(20) DEFAULT 'Completed' CHECK (sale_status IN ('Pending', 'Completed', 'Cancelled', 'Refunded')),
    notes NVARCHAR(500),
    created_date DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CHK_FinalAmount CHECK (final_amount = sale_price + tax_amount - discount_amount),
    CONSTRAINT CHK_Commission CHECK (commission_amount = sale_price * commission_rate / 100)
);
GO

-- ==================== 9. SERVICE_RECORDS (Maintenance History) ====================
CREATE TABLE ServiceRecords (
    service_id INT PRIMARY KEY IDENTITY(1,1),
    vehicle_id INT NOT NULL FOREIGN KEY REFERENCES Vehicles(vehicle_id),
    service_date DATE NOT NULL,
    service_type NVARCHAR(50) CHECK (service_type IN ('Regular Maintenance', 'Oil Change', 'Brake Service', 'Engine Repair', 'Electrical', 'AC Service', 'Body Repair', 'Warranty Claim')),
    description NVARCHAR(500) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    parts_cost DECIMAL(10,2) DEFAULT 0,
    labor_cost DECIMAL(10,2) DEFAULT 0,
    service_center NVARCHAR(100),
    next_service_km INT,
    next_service_date DATE,
    is_warranty BIT DEFAULT 0,
    technician_name NVARCHAR(100),
    created_date DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT CHK_ServiceCost CHECK (cost = parts_cost + labor_cost)
);
GO

-- ==================== 10. TEST_DRIVES (Customer Experience) ====================
CREATE TABLE TestDrives (
    test_drive_id INT PRIMARY KEY IDENTITY(1,1),
    vehicle_id INT NOT NULL FOREIGN KEY REFERENCES Vehicles(vehicle_id),
    customer_id INT NOT NULL FOREIGN KEY REFERENCES Customers(customer_id),
    employee_id INT NOT NULL FOREIGN KEY REFERENCES Employees(employee_id),
    scheduled_date DATETIME NOT NULL,
    duration_minutes INT DEFAULT 30,
    status NVARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Completed', 'Cancelled', 'No Show')),
    feedback NVARCHAR(500),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 11. PRICE_HISTORY (Audit Trail) ====================
CREATE TABLE PriceHistory (
    history_id INT PRIMARY KEY IDENTITY(1,1),
    vehicle_id INT NOT NULL FOREIGN KEY REFERENCES Vehicles(vehicle_id),
    old_price DECIMAL(12,2) NOT NULL,
    new_price DECIMAL(12,2) NOT NULL,
    change_reason NVARCHAR(100) CHECK (change_reason IN ('Market Adjustment', 'Demand Increase', 'Clearance Sale', 'Seasonal Offer', 'VIP Discount', 'System Update')),
    changed_by INT, -- employee_id
    change_date DATETIME DEFAULT GETDATE(),
    notes NVARCHAR(200)
);
GO

-- ==================== 12. INVENTORY_AUDIT (Change Tracking) ====================
CREATE TABLE InventoryAudit (
    audit_id INT PRIMARY KEY IDENTITY(1,1),
    vehicle_id INT NOT NULL FOREIGN KEY REFERENCES Vehicles(vehicle_id),
    action_type NVARCHAR(50) NOT NULL CHECK (action_type IN ('Status Change', 'Price Update', 'Location Transfer', 'Service Record', 'Sale', 'Test Drive')),
    old_value NVARCHAR(100),
    new_value NVARCHAR(100),
    performed_by INT, -- employee_id
    notes NVARCHAR(500),
    audit_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 13. CREDIT_SCORES (Customer Finance) ====================
CREATE TABLE CreditScores (
    score_id INT PRIMARY KEY IDENTITY(1,1),
    customer_id INT NOT NULL FOREIGN KEY REFERENCES Customers(customer_id),
    score INT CHECK (score BETWEEN 300 AND 850),
    rating NVARCHAR(20) CHECK (rating IN ('Poor', 'Fair', 'Good', 'Very Good', 'Excellent')),
    provider NVARCHAR(50),
    report_date DATE DEFAULT GETDATE(),
    expiry_date DATE,
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== 14. PAYMENTS (Financial Records) ====================
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY IDENTITY(1,1),
    sale_id INT NOT NULL FOREIGN KEY REFERENCES Sales(sale_id),
    amount DECIMAL(12,2) NOT NULL,
    payment_date DATETIME DEFAULT GETDATE(),
    payment_method NVARCHAR(30),
    transaction_id NVARCHAR(100),
    status NVARCHAR(20) DEFAULT 'Completed' CHECK (status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
    bank_name NVARCHAR(100),
    account_number NVARCHAR(50),
    created_date DATETIME DEFAULT GETDATE()
);
GO

-- ==================== INDEXES FOR PERFORMANCE ====================
CREATE INDEX IX_Vehicles_Status ON Vehicles(status);
CREATE INDEX IX_Vehicles_Price ON Vehicles(current_price);
CREATE INDEX IX_Vehicles_Dealership ON Vehicles(dealership_id);
CREATE INDEX IX_Sales_Date ON Sales(sale_date);
CREATE INDEX IX_Customers_Email ON Customers(email);
CREATE INDEX IX_Customers_Phone ON Customers(phone);
CREATE INDEX IX_Employees_Dealership ON Employees(dealership_id);
GO

-- ==================== VIEWS FOR REPORTING ====================

-- View 1: Available Vehicles with Details
CREATE VIEW vw_AvailableVehicles AS
SELECT 
    v.vehicle_id,
    m.name AS manufacturer,
    vm.model_name,
    vt.type_name,
    v.color,
    v.manufacturing_year,
    v.mileage_km,
    v.current_price,
    d.name AS dealership,
    d.city,
    v.status,
    v.import_status,
    vm.horsepower,
    vm.fuel_type,
    vm.transmission
FROM Vehicles v
JOIN VehicleModels vm ON v.model_id = vm.model_id
JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
JOIN VehicleTypes vt ON vm.type_id = vt.type_id
JOIN Dealerships d ON v.dealership_id = d.dealership_id
WHERE v.status = 'Available';
GO

-- View 2: Monthly Sales Summary
CREATE VIEW vw_MonthlySales AS
SELECT 
    YEAR(s.sale_date) AS sale_year,
    MONTH(s.sale_date) AS sale_month,
    COUNT(*) AS total_sales,
    SUM(s.final_amount) AS total_revenue,
    AVG(s.final_amount) AS average_sale,
    SUM(s.commission_amount) AS total_commission
FROM Sales s
WHERE s.sale_status = 'Completed'
GROUP BY YEAR(s.sale_date), MONTH(s.sale_date);
GO

-- View 3: Customer Purchase History
CREATE VIEW vw_CustomerPurchases AS
SELECT 
    c.customer_id,
    c.first_name + ' ' + c.last_name AS customer_name,
    c.phone,
    c.email,
    COUNT(s.sale_id) AS total_purchases,
    SUM(s.final_amount) AS total_spent,
    MAX(s.sale_date) AS last_purchase_date,
    c.is_vip
FROM Customers c
LEFT JOIN Sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.phone, c.email, c.is_vip;
GO

-- View 4: Employee Performance
CREATE VIEW vw_EmployeePerformance AS
SELECT 
    e.employee_id,
    e.first_name + ' ' + e.last_name AS employee_name,
    e.position,
    d.name AS dealership,
    COUNT(s.sale_id) AS total_sales,
    SUM(s.final_amount) AS total_revenue,
    SUM(s.commission_amount) AS total_commission,
    AVG(s.commission_amount) AS avg_commission
FROM Employees e
LEFT JOIN Sales s ON e.employee_id = s.employee_id
JOIN Dealerships d ON e.dealership_id = d.dealership_id
WHERE e.is_active = 1
GROUP BY e.employee_id, e.first_name, e.last_name, e.position, d.name;
GO

-- View 5: Inventory Value by Dealership
CREATE VIEW vw_InventoryValue AS
SELECT 
    d.dealership_id,
    d.name AS dealership,
    d.city,
    d.province,
    COUNT(v.vehicle_id) AS total_vehicles,
    SUM(v.current_price) AS total_value,
    AVG(v.current_price) AS average_price,
    MIN(v.current_price) AS min_price,
    MAX(v.current_price) AS max_price
FROM Dealerships d
JOIN Vehicles v ON d.dealership_id = v.dealership_id
WHERE v.status = 'Available'
GROUP BY d.dealership_id, d.name, d.city, d.province;
GO

PRINT '✅ Database schema created successfully with 14 tables and 5 views!';
GO