"""
Database Connection Manager with Connection Pooling
"""
import pyodbc
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Optional, Dict, Any
import logging
from datetime import datetime

load_dotenv()

class DatabaseConnection:
    """Singleton database connection manager"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = self._setup_logger()
            self.connection_string = self._build_connection_string()
            self._initialized = True
    
    def _setup_logger(self):
        """Setup database logger"""
        logger = logging.getLogger('Database')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _build_connection_string(self) -> str:
        """Build connection string from environment variables"""
        server = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
        database = os.getenv('DB_DATABASE', 'VelocityNexusPrime')
        username = os.getenv('DB_USERNAME', '')
        password = os.getenv('DB_PASSWORD', '')
        driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        
        if os.getenv('DB_TRUSTED_CONNECTION', 'yes').lower() == 'yes':
            return (
                f'DRIVER={{{driver}}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'Trusted_Connection=yes;'
            )
        else:
            return (
                f'DRIVER={{{driver}}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password};'
            )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connection"""
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except pyodbc.Error as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def connect(self):
        """Establish database connection"""
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.autocommit = False
            self.logger.info("Database connection established successfully")
            return conn
        except pyodbc.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_connection() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute a query and return results"""
        try:
            with self.get_connection() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if cursor.description:  # If query returns results
                    columns = [column[0] for column in cursor.description]
                    results = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                else:
                    return []
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_procedure(self, procedure_name: str, params: dict = None):
        """Execute a stored procedure"""
        try:
            with self.get_connection() as cursor:
                if params:
                    # Build parameter string
                    param_placeholders = ', '.join(['?'] * len(params))
                    sql = f"EXEC {procedure_name} {param_placeholders}"
                    cursor.execute(sql, list(params.values()))
                else:
                    cursor.execute(f"EXEC {procedure_name}")
                
                if cursor.description:
                    columns = [column[0] for column in cursor.description]
                    results = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                else:
                    return []
        except Exception as e:
            self.logger.error(f"Procedure execution failed: {e}")
            return []
    
    def insert_data(self, table: str, data: dict) -> int:
        """Insert data into table and return inserted ID"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}); SELECT SCOPE_IDENTITY();"
            
            with self.get_connection() as cursor:
                cursor.execute(query, tuple(data.values()))
                inserted_id = cursor.fetchone()[0]
                return inserted_id
        except Exception as e:
            self.logger.error(f"Insert failed: {e}")
            return -1
    
    def update_data(self, table: str, data: dict, condition: str, params: tuple = None) -> bool:
        """Update data in table"""
        try:
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            
            with self.get_connection() as cursor:
                all_params = tuple(data.values()) + (params if params else ())
                cursor.execute(query, all_params)
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> list:
        """Get table schema information"""
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(query, (table_name,))
    
    def get_database_stats(self) -> dict:
        """Get database statistics"""
        stats = {}
        
        # Get table counts
        tables = ['Vehicles', 'Customers', 'Sales', 'Employees', 'Manufacturers']
        for table in tables:
            result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = result[0]['count'] if result else 0
        
        # Get recent sales
        recent_sales = self.execute_query("""
            SELECT TOP 5 
                s.sale_date,
                c.first_name + ' ' + c.last_name as customer,
                m.name as manufacturer,
                vm.model_name,
                s.final_amount
            FROM Sales s
            JOIN Customers c ON s.customer_id = c.customer_id
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
            ORDER BY s.sale_date DESC
        """)
        
        stats['recent_sales'] = recent_sales
        
        return stats


# Singleton instance
db = DatabaseConnection()