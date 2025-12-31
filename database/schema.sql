-- VELOCITY NEXUS PRIME - MASTER SCHEMA
-- 3NF Compliant | 12 Tables | Advanced Relations

IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'VelocityNexusPrime')
    CREATE DATABASE VelocityNexusPrime;
GO
USE VelocityNexusPrime;
GO

-- 1. Locations (City/Province Lookup for Dealerships) - 3NF
CREATE TABLE Locations (
    LocationID INT IDENTITY(1,1) PRIMARY KEY,
    City NVARCHAR(50) NOT NULL,
    Province NVARCHAR(50) NOT NULL
);

-- 2. Manufacturers (Global vs Local)
CREATE TABLE Manufacturers (
    ManufacturerID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL UNIQUE, -- Honda, Suzuki, MG
    OriginCountry NVARCHAR(50),
    LicenseType NVARCHAR(50) -- 'Joint Venture', 'Import Permit'
);

-- 3. VehicleModels (The definitions)
CREATE TABLE VehicleModels (
    ModelID INT IDENTITY(1,1) PRIMARY KEY,
    ManufacturerID INT FOREIGN KEY REFERENCES Manufacturers(ManufacturerID),
    ModelName NVARCHAR(100) NOT NULL, -- Civic, Alto
    Generation NVARCHAR(50), -- "11th Gen"
    BodyType NVARCHAR(50),
    EngineCapacityCC INT,
    BasePricePKR DECIMAL(18,2) NOT NULL
);

-- 4. Dealerships (The Physical Stores)
CREATE TABLE Dealerships (
    DealershipID INT IDENTITY(1,1) PRIMARY KEY,
    LocationID INT FOREIGN KEY REFERENCES Locations(LocationID),
    Name NVARCHAR(100), -- "Honda Point"
    Capacity INT,
    IsActive BIT DEFAULT 1
);

-- 5. Employees (Sales & Service Staff)
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    DealershipID INT FOREIGN KEY REFERENCES Dealerships(DealershipID),
    FullName NVARCHAR(100),
    Role NVARCHAR(50), -- Manager, Sales Rep, Mechanic
    HireDate DATE
);

-- 6. Inventory (Physical Cars)
CREATE TABLE Inventory (
    VehicleID INT IDENTITY(1,1) PRIMARY KEY,
    ModelID INT FOREIGN KEY REFERENCES VehicleModels(ModelID),
    DealershipID INT FOREIGN KEY REFERENCES Dealerships(DealershipID),
    VIN NVARCHAR(50) UNIQUE NOT NULL, -- Chassis Number
    Color NVARCHAR(30),
    ManufacturingYear INT,
    ImportStatus NVARCHAR(20) CHECK (ImportStatus IN ('Local', 'Imported')),
    Status NVARCHAR(20) DEFAULT 'Available' -- Available, Reserved, Sold
);

-- 7. Customers
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CNIC NVARCHAR(20) UNIQUE NOT NULL,
    FullName NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(200)
);

-- 8. Sales (Transactions)
CREATE TABLE Sales (
    SaleID INT IDENTITY(1,1) PRIMARY KEY,
    VehicleID INT FOREIGN KEY REFERENCES Inventory(VehicleID),
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    EmployeeID INT FOREIGN KEY REFERENCES Employees(EmployeeID),
    SaleDate DATETIME DEFAULT GETDATE(),
    BaseAmount DECIMAL(18,2),
    TaxAmount DECIMAL(18,2), -- 17% or 35%
    FinalAmount DECIMAL(18,2),
    PaymentMethod NVARCHAR(50)
);

-- 9. ServiceRecords (Maintenance History)
CREATE TABLE ServiceRecords (
    ServiceID INT IDENTITY(1,1) PRIMARY KEY,
    VehicleID INT FOREIGN KEY REFERENCES Inventory(VehicleID),
    ServiceDate DATE,
    Description NVARCHAR(MAX),
    Cost DECIMAL(18,2)
);

-- 10. AuditLogs (SCD Requirement: Tracking Changes)
CREATE TABLE AuditLogs (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    ActionType NVARCHAR(50), -- 'LOGIN', 'SALE', 'UPDATE'
    Description NVARCHAR(MAX),
    Timestamp DATETIME DEFAULT GETDATE()
);

-- 11. AppUsers (Login System)
CREATE TABLE AppUsers (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE,
    PasswordHash NVARCHAR(256), -- In real app, hash this!
    Role NVARCHAR(20) -- Admin, User
);

-- SEED DATA (For Testing)
INSERT INTO Locations (City, Province) VALUES ('Lahore', 'Punjab'), ('Karachi', 'Sindh');
INSERT INTO Manufacturers (Name, OriginCountry) VALUES ('Honda Atlas', 'Pakistan'), ('MG Motors', 'China');
INSERT INTO VehicleModels (ManufacturerID, ModelName, BasePricePKR) VALUES (1, 'Civic RS', 8500000), (2, 'HS Essence', 8900000);
INSERT INTO Dealerships (LocationID, Name, Capacity) VALUES (1, 'Honda Fort', 50);
GO