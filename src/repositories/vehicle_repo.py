from src.database.connection import DatabaseConnection

class VehicleRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_dashboard_stats(self):
        """Advanced Aggregation for Dashboard"""
        conn = self.db.connect()
        cursor = conn.cursor()
        
        stats = {}
        # Total Inventory
        cursor.execute("SELECT COUNT(*) FROM Inventory WHERE Status='Available'")
        stats['inventory'] = cursor.fetchone()[0]
        
        # Total Sales Value
        cursor.execute("SELECT ISNULL(SUM(FinalAmount), 0) FROM Sales")
        stats['sales_volume'] = cursor.fetchone()[0]
        
        return stats

    def get_detailed_inventory(self):
        """
        Complex JOIN query fetching data across 4 tables:
        Inventory -> VehicleModels -> Manufacturers
        Inventory -> Dealerships -> Locations
        """
        query = """
        SELECT 
            i.VehicleID, 
            m.Name as Make, 
            vm.ModelName, 
            i.Color, 
            vm.BasePricePKR, 
            d.Name as Dealership,
            l.City,
            i.Status,
            i.ImportStatus
        FROM Inventory i
        JOIN VehicleModels vm ON i.ModelID = vm.ModelID
        JOIN Manufacturers m ON vm.ManufacturerID = m.ManufacturerID
        JOIN Dealerships d ON i.DealershipID = d.DealershipID
        JOIN Locations l ON d.LocationID = l.LocationID
        """
        cursor = self.db.get_cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def execute_sale(self, vehicle_id, customer_cnic, customer_name, employee_id, price, tax):
        """Transactional Sale Logic"""
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # 1. Check/Create Customer
            cursor.execute("SELECT CustomerID FROM Customers WHERE CNIC = ?", (customer_cnic,))
            cust = cursor.fetchone()
            if cust:
                cust_id = cust[0]
            else:
                cursor.execute("INSERT INTO Customers (CNIC, FullName) OUTPUT INSERTED.CustomerID VALUES (?, ?)", 
                               (customer_cnic, customer_name))
                cust_id = cursor.fetchone()[0]

            # 2. Update Inventory
            cursor.execute("UPDATE Inventory SET Status = 'Sold' WHERE VehicleID = ?", (vehicle_id,))

            # 3. Record Sale
            total = price + tax
            cursor.execute("""
                INSERT INTO Sales (VehicleID, CustomerID, EmployeeID, BaseAmount, TaxAmount, FinalAmount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (vehicle_id, cust_id, employee_id, price, tax, total))

            # 4. Audit Log
            cursor.execute("INSERT INTO AuditLogs (ActionType, Description) VALUES ('SALE', ?)", 
                           (f"Vehicle {vehicle_id} sold to {customer_name}",))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Transaction Failed: {e}")
            return False