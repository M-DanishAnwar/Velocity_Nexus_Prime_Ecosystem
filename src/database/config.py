"""
Database Configuration Manager
"""
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration data class"""
    server: str
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    driver: str = "ODBC Driver 17 for SQL Server"
    trusted_connection: bool = True
    timeout: int = 30
    pool_size: int = 5
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create config from environment variables"""
        return cls(
            server=os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS'),
            database=os.getenv('DB_DATABASE', 'VelocityNexusPrime'),
            username=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            driver=os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
            trusted_connection=os.getenv('DB_TRUSTED_CONNECTION', 'yes').lower() == 'yes',
            timeout=int(os.getenv('DB_TIMEOUT', '30')),
            pool_size=int(os.getenv('DB_POOL_SIZE', '5'))
        )
    
    @property
    def connection_string(self) -> str:
        """Build connection string"""
        if self.trusted_connection:
            return (
                f'DRIVER={{{self.driver}}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'Trusted_Connection=yes;'
                f'Connection Timeout={self.timeout};'
            )
        else:
            return (
                f'DRIVER={{{self.driver}}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                f'Connection Timeout={self.timeout};'
            )
    
    def validate(self) -> tuple[bool, str]:
        """Validate configuration"""
        if not self.server:
            return False, "Database server is required"
        if not self.database:
            return False, "Database name is required"
        if not self.trusted_connection and (not self.username or not self.password):
            return False, "Username and password required for SQL authentication"
        return True, "Configuration is valid"


@dataclass
class AppConfig:
    """Application configuration"""
    title: str = "Velocity Nexus Prime"
    version: str = "1.0.0"
    debug: bool = False
    demo_mode: bool = False
    currency: str = "PKR"
    tax_rate: float = 17.0
    default_commission: float = 5.0
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create app config from environment variables"""
        return cls(
            title=os.getenv('APP_TITLE', 'Velocity Nexus Prime'),
            version=os.getenv('APP_VERSION', '1.0.0'),
            debug=os.getenv('APP_DEBUG', 'False').lower() == 'true',
            demo_mode=os.getenv('DEMO_MODE', 'False').lower() == 'true',
            currency=os.getenv('CURRENCY', 'PKR'),
            tax_rate=float(os.getenv('DEFAULT_TAX_RATE', '17.0')),
            default_commission=float(os.getenv('DEFAULT_COMMISSION_RATE', '5.0'))
        )


class ConfigManager:
    """Central configuration manager"""
    
    def __init__(self):
        self.db_config = DatabaseConfig.from_env()
        self.app_config = AppConfig.from_env()
        self._validate_configs()
    
    def _validate_configs(self):
        """Validate all configurations"""
        # Validate database config
        db_valid, db_message = self.db_config.validate()
        if not db_valid:
            print(f"⚠️ Database config warning: {db_message}")
            print("⚠️ Running in DEMO MODE")
            self.app_config.demo_mode = True
        
        # Validate app config
        if self.app_config.debug:
            print("🔧 Running in DEBUG mode")
    
    def print_config(self):
        """Print current configuration"""
        print("=" * 50)
        print("📋 CURRENT CONFIGURATION")
        print("=" * 50)
        
        print("\n🗄️ DATABASE CONFIG:")
        print(f"   Server: {self.db_config.server}")
        print(f"   Database: {self.db_config.database}")
        print(f"   Authentication: {'Windows' if self.db_config.trusted_connection else 'SQL Server'}")
        print(f"   Driver: {self.db_config.driver}")
        
        print("\n📱 APPLICATION CONFIG:")
        print(f"   Title: {self.app_config.title}")
        print(f"   Version: {self.app_config.version}")
        print(f"   Demo Mode: {self.app_config.demo_mode}")
        print(f"   Currency: {self.app_config.currency}")
        print(f"   Tax Rate: {self.app_config.tax_rate}%")
        print(f"   Commission: {self.app_config.default_commission}%")
        print("=" * 50)
    
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode"""
        return self.app_config.demo_mode
    
    def get_database_stats_query(self) -> dict:
        """Get queries for database statistics"""
        return {
            'total_vehicles': "SELECT COUNT(*) as count FROM Vehicles",
            'available_vehicles': "SELECT COUNT(*) as count FROM Vehicles WHERE status = 'Available'",
            'total_customers': "SELECT COUNT(*) as count FROM Customers",
            'total_sales': "SELECT COUNT(*) as count FROM Sales",
            'monthly_revenue': """
                SELECT 
                    FORMAT(sale_date, 'yyyy-MM') as month,
                    SUM(final_amount) as revenue
                FROM Sales
                WHERE sale_status = 'Completed'
                GROUP BY FORMAT(sale_date, 'yyyy-MM')
                ORDER BY month DESC
            """,
            'top_selling_models': """
                SELECT TOP 5
                    m.name as manufacturer,
                    vm.model_name,
                    COUNT(s.sale_id) as units_sold,
                    SUM(s.final_amount) as revenue
                FROM Sales s
                JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
                JOIN VehicleModels vm ON v.model_id = vm.model_id
                JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
                GROUP BY m.name, vm.model_name
                ORDER BY units_sold DESC
            """
        }


# Global config instance
config = ConfigManager()