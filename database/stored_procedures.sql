USE VelocityNexusPrime;
GO

-- ==================== STORED PROCEDURES ====================

-- 1. Get High Performance Vehicles
CREATE PROCEDURE sp_GetHighPerformanceVehicles
    @min_horsepower INT = 300,
    @max_price DECIMAL(12,2) = 50000000,
    @location NVARCHAR(50) = NULL
AS
BEGIN
    SELECT 
        v.vehicle_id,
        m.name AS manufacturer,
        vm.model_name,
        v.color,
        v.manufacturing_year,
        vm.horsepower,
        vm.fuel_type,
        v.current_price,
        d.name AS dealership,
        d.city,
        v.status
    FROM Vehicles v
    JOIN VehicleModels vm ON v.model_id = vm.model_id
    JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
    JOIN Dealerships d ON v.dealership_id = d.dealership_id
    WHERE vm.horsepower >= @min_horsepower
        AND v.current_price <= @max_price
        AND v.status = 'Available'
        AND (@location IS NULL OR d.city = @location)
    ORDER BY vm.horsepower DESC, v.current_price DESC;
END;
GO

-- 2. Process Vehicle Sale
CREATE PROCEDURE sp_ProcessVehicleSale
    @vehicle_id INT,
    @customer_id INT,
    @employee_id INT,
    @sale_price DECIMAL(12,2),
    @payment_method NVARCHAR(30),
    @sale_id INT OUTPUT,
    @message NVARCHAR(200) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Check vehicle availability
        DECLARE @current_status NVARCHAR(20);
        SELECT @current_status = status FROM Vehicles WHERE vehicle_id = @vehicle_id;
        
        IF @current_status != 'Available'
        BEGIN
            SET @message = 'Vehicle is not available. Current status: ' + @current_status;
            SET @sale_id = -1;
            ROLLBACK;
            RETURN;
        END
        
        -- Get employee commission rate
        DECLARE @commission_rate DECIMAL(5,2);
        SELECT @commission_rate = commission_rate FROM Employees WHERE employee_id = @employee_id;
        
        -- Calculate tax (17% standard, 35% for imported)
        DECLARE @import_status NVARCHAR(20);
        DECLARE @tax_rate DECIMAL(5,2);
        
        SELECT @import_status = import_status FROM Vehicles WHERE vehicle_id = @vehicle_id;
        SET @tax_rate = CASE WHEN @import_status = 'Imported' THEN 35.0 ELSE 17.0 END;
        
        DECLARE @tax_amount DECIMAL(10,2) = @sale_price * (@tax_rate / 100);
        DECLARE @commission_amount DECIMAL(10,2) = @sale_price * (@commission_rate / 100);
        DECLARE @final_amount DECIMAL(12,2) = @sale_price + @tax_amount;
        
        -- Insert sale record
        INSERT INTO Sales (
            vehicle_id, customer_id, employee_id, 
            sale_price, base_price, tax_rate, tax_amount, 
            final_amount, commission_rate, commission_amount,
            payment_method, sale_status
        )
        VALUES (
            @vehicle_id, @customer_id, @employee_id,
            @sale_price, @sale_price, @tax_rate, @tax_amount,
            @final_amount, @commission_rate, @commission_amount,
            @payment_method, 'Completed'
        );
        
        SET @sale_id = SCOPE_IDENTITY();
        
        -- Update vehicle status
        UPDATE Vehicles 
        SET status = 'Sold', 
            sold_date = GETDATE(),
            last_updated = GETDATE()
        WHERE vehicle_id = @vehicle_id;
        
        -- Update customer total spent
        UPDATE Customers 
        SET total_purchases = total_purchases + 1,
            total_spent = total_spent + @final_amount,
            last_purchase_date = GETDATE()
        WHERE customer_id = @customer_id;
        
        -- Log inventory audit
        INSERT INTO InventoryAudit (vehicle_id, action_type, old_value, new_value, performed_by, notes)
        VALUES (@vehicle_id, 'Sale', 'Available', 'Sold', @employee_id, 
                'Sold to customer ID: ' + CAST(@customer_id AS NVARCHAR));
        
        SET @message = 'Sale processed successfully. Sale ID: ' + CAST(@sale_id AS NVARCHAR);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SET @message = 'Error: ' + ERROR_MESSAGE();
        SET @sale_id = -1;
    END CATCH
END;
GO

-- 3. Get Monthly Sales Report
CREATE PROCEDURE sp_GetMonthlySalesReport
    @year INT = NULL,
    @month INT = NULL
AS
BEGIN
    IF @year IS NULL SET @year = YEAR(GETDATE());
    IF @month IS NULL SET @month = MONTH(GETDATE());
    
    SELECT 
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.position,
        d.name AS dealership,
        COUNT(s.sale_id) AS total_sales,
        SUM(s.final_amount) AS total_revenue,
        SUM(s.commission_amount) AS total_commission,
        AVG(s.final_amount) AS average_sale
    FROM Sales s
    JOIN Employees e ON s.employee_id = e.employee_id
    JOIN Dealerships d ON e.dealership_id = d.dealership_id
    WHERE YEAR(s.sale_date) = @year 
        AND MONTH(s.sale_date) = @month
        AND s.sale_status = 'Completed'
    GROUP BY e.employee_id, e.first_name, e.last_name, e.position, d.name
    ORDER BY total_revenue DESC;
END;
GO

-- 4. Get Customer Purchase History
CREATE PROCEDURE sp_GetCustomerPurchaseHistory
    @customer_id INT
AS
BEGIN
    SELECT 
        s.sale_id,
        s.sale_date,
        m.name AS manufacturer,
        vm.model_name,
        v.color,
        v.manufacturing_year,
        s.sale_price,
        s.tax_amount,
        s.final_amount,
        s.payment_method,
        e.first_name + ' ' + e.last_name AS sales_person
    FROM Sales s
    JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN VehicleModels vm ON v.model_id = vm.model_id
    JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
    JOIN Employees e ON s.employee_id = e.employee_id
    WHERE s.customer_id = @customer_id
    ORDER BY s.sale_date DESC;
END;
GO

-- 5. Update Vehicle Price with History
CREATE PROCEDURE sp_UpdateVehiclePrice
    @vehicle_id INT,
    @new_price DECIMAL(12,2),
    @reason NVARCHAR(100),
    @employee_id INT
AS
BEGIN
    BEGIN TRANSACTION;
    
    DECLARE @old_price DECIMAL(12,2);
    
    -- Get current price
    SELECT @old_price = current_price FROM Vehicles WHERE vehicle_id = @vehicle_id;
    
    -- Update vehicle price
    UPDATE Vehicles 
    SET current_price = @new_price,
        last_updated = GETDATE()
    WHERE vehicle_id = @vehicle_id;
    
    -- Record price history
    INSERT INTO PriceHistory (vehicle_id, old_price, new_price, change_reason, changed_by)
    VALUES (@vehicle_id, @old_price, @new_price, @reason, @employee_id);
    
    -- Log audit
    INSERT INTO InventoryAudit (vehicle_id, action_type, old_value, new_value, performed_by, notes)
    VALUES (@vehicle_id, 'Price Update', 
            CAST(@old_price AS NVARCHAR), 
            CAST(@new_price AS NVARCHAR),
            @employee_id, @reason);
    
    COMMIT TRANSACTION;
    
    PRINT 'Price updated from ' + CAST(@old_price AS NVARCHAR) + ' to ' + CAST(@new_price AS NVARCHAR);
END;
GO

-- ==================== TRIGGERS ====================

-- 1. Auto-update commission when sale price changes
CREATE TRIGGER trg_UpdateCommission
ON Sales
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE s
    SET s.commission_amount = s.sale_price * (s.commission_rate / 100),
        s.final_amount = s.sale_price + s.tax_amount - ISNULL(s.discount_amount, 0)
    FROM Sales s
    INNER JOIN inserted i ON s.sale_id = i.sale_id;
END;
GO

-- 2. Log vehicle status changes
CREATE TRIGGER trg_LogStatusChange
ON Vehicles
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO InventoryAudit (vehicle_id, action_type, old_value, new_value, notes)
    SELECT 
        i.vehicle_id,
        'Status Change',
        d.status,
        i.status,
        'Status changed via system'
    FROM inserted i
    INNER JOIN deleted d ON i.vehicle_id = d.vehicle_id
    WHERE i.status != d.status;
END;
GO

-- 3. Auto-update last_updated timestamp
CREATE TRIGGER trg_UpdateTimestamp
ON Vehicles
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE v
    SET last_updated = GETDATE()
    FROM Vehicles v
    INNER JOIN inserted i ON v.vehicle_id = i.vehicle_id;
END;
GO

PRINT '✅ Stored procedures and triggers created successfully!';
GO