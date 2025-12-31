"""
Database Tests for Velocity Nexus Prime
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestDatabaseConnection:
    """Test database connection functionality"""
    
    def test_connection_string_building(self):
        """Test connection string construction"""
        from src.database.config import DatabaseConfig
        
        # Test Windows authentication
        config = DatabaseConfig(
            server='localhost\\SQLEXPRESS',
            database='TestDB',
            trusted_connection=True
        )
        
        conn_str = config.connection_string
        assert 'Trusted_Connection=yes' in conn_str
        assert 'localhost\\SQLEXPRESS' in conn_str
        assert 'TestDB' in conn_str
        
        # Test SQL authentication
        config2 = DatabaseConfig(
            server='localhost',
            database='TestDB',
            username='sa',
            password='password',
            trusted_connection=False
        )
        
        conn_str2 = config2.connection_string
        assert 'UID=sa' in conn_str2
        assert 'PWD=password' in conn_str2
    
    def test_config_validation(self):
        """Test configuration validation"""
        from src.database.config import DatabaseConfig
        
        # Valid config
        config = DatabaseConfig(
            server='localhost',
            database='TestDB',
            trusted_connection=True
        )
        
        valid, message = config.validate()
        assert valid == True
        assert message == "Configuration is valid"
        
        # Invalid config (missing server)
        config2 = DatabaseConfig(
            server='',
            database='TestDB',
            trusted_connection=True
        )
        
        valid2, message2 = config2.validate()
        assert valid2 == False
        assert "server is required" in message2
    
    @patch('src.database.connection.pyodbc.connect')
    def test_connection_test(self, mock_connect):
        """Test database connection test"""
        from src.database.connection import DatabaseConnection
        
        # Mock successful connection
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        result = db.test_connection()
        
        assert result == True
        mock_connect.assert_called_once()
    
    @patch('src.database.connection.pyodbc.connect')
    def test_query_execution(self, mock_connect):
        """Test query execution"""
        from src.database.connection import DatabaseConnection
        
        # Mock connection and cursor
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchall.return_value = [(1, 'Test')]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        results = db.execute_query("SELECT * FROM test")
        
        assert len(results) == 1
        assert results[0]['id'] == 1
        assert results[0]['name'] == 'Test'
    
    def test_insert_data(self):
        """Test data insertion"""
        from src.database.connection import DatabaseConnection
        
        with patch.object(DatabaseConnection, 'execute_query') as mock_execute:
            mock_execute.return_value = [{'': 100}]
            
            db = DatabaseConnection()
            table = 'test_table'
            data = {'name': 'Test', 'value': 123}
            
            result = db.insert_data(table, data)
            
            assert result == 100
            mock_execute.assert_called_once()


class TestRepositories:
    """Test repository classes"""
    
    def test_vehicle_repository_creation(self):
        """Test vehicle repository initialization"""
        from src.repositories.vehicle_repo import VehicleRepository
        
        repo = VehicleRepository()
        assert repo.table_name == 'Vehicles'
        assert repo.logger is not None
    
    def test_customer_repository_creation(self):
        """Test customer repository initialization"""
        from src.repositories.customer_repo import CustomerRepository
        
        repo = CustomerRepository()
        assert repo.table_name == 'Customers'
        assert repo.logger is not None
    
    def test_vehicle_entity_conversion(self):
        """Test vehicle entity to/from dict conversion"""
        from src.repositories.vehicle_repo import Vehicle
        from datetime import datetime
        
        # Create vehicle entity
        vehicle = Vehicle(
            vehicle_id=1,
            model_id=2,
            dealership_id=3,
            vin='TESTVIN123456789',
            color='Red',
            current_price=5000000,
            status='Available'
        )
        
        # Convert to dict
        from src.repositories.vehicle_repo import VehicleRepository
        repo = VehicleRepository()
        data = repo.to_dict(vehicle)
        
        # Verify conversion
        assert data['vehicle_id'] == 1
        assert data['model_id'] == 2
        assert data['vin'] == 'TESTVIN123456789'
        assert data['color'] == 'Red'
        assert data['current_price'] == 5000000
        assert data['status'] == 'Available'
        
        # Convert back to entity
        vehicle2 = repo.to_entity(data)
        
        assert vehicle2.vehicle_id == 1
        assert vehicle2.model_id == 2
        assert vehicle2.vin == 'TESTVIN123456789'
    
    def test_customer_entity_conversion(self):
        """Test customer entity to/from dict conversion"""
        from src.repositories.customer_repo import Customer
        
        # Create customer entity
        customer = Customer(
            customer_id=1,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            total_spent=1000000,
            is_vip=True
        )
        
        # Convert to dict
        from src.repositories.customer_repo import CustomerRepository
        repo = CustomerRepository()
        data = repo.to_dict(customer)
        
        # Verify conversion
        assert data['customer_id'] == 1
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'
        assert data['email'] == 'john@example.com'
        assert data['phone'] == '1234567890'
        assert data['total_spent'] == 1000000
        assert data['is_vip'] == True
        
        # Test full_name property
        assert customer.full_name == 'John Doe'


class TestAnalyticsService:
    """Test analytics service"""
    
    def test_analytics_service_creation(self):
        """Test analytics service initialization"""
        from src.services.analytics_service import AnalyticsService
        
        service = AnalyticsService()
        assert service.demo_data is not None
        assert 'monthly_sales' in service.demo_data
        assert 'sales_by_category' in service.demo_data
    
    def test_demo_data_structure(self):
        """Test demo data structure"""
        from src.services.analytics_service import AnalyticsService
        
        service = AnalyticsService()
        demo_data = service.demo_data
        
        # Check monthly sales data
        assert 'months' in demo_data['monthly_sales']
        assert 'revenue' in demo_data['monthly_sales']
        assert 'units' in demo_data['monthly_sales']
        
        # Check sales by category
        assert 'categories' in demo_data['sales_by_category']
        assert 'values' in demo_data['sales_by_category']
        assert 'colors' in demo_data['sales_by_category']
        
        # Verify array lengths match
        months = demo_data['monthly_sales']['months']
        revenue = demo_data['monthly_sales']['revenue']
        assert len(months) == len(revenue)
    
    @patch('src.services.analytics_service.db.execute_query')
    def test_get_vehicle_statistics(self, mock_execute):
        """Test vehicle statistics retrieval"""
        from src.services.analytics_service import AnalyticsService
        
        # Mock database response
        mock_execute.return_value = [
            {'total': 10, 'available': 5, 'sold': 3, 'reserved': 2, 
             'avg_price': 5000000, 'min_price': 1000000, 'max_price': 10000000}
        ]
        
        service = AnalyticsService()
        stats = service.get_vehicle_statistics()
        
        assert 'total' in stats
        assert 'available' in stats
        assert 'sold' in stats
        assert 'avg_price' in stats
    
    @patch('src.services.analytics_service.config.is_demo_mode')
    def test_demo_mode_fallback(self, mock_demo_mode):
        """Test demo mode fallback"""
        from src.services.analytics_service import AnalyticsService
        
        # Force demo mode
        mock_demo_mode.return_value = True
        
        service = AnalyticsService()
        stats = service.get_vehicle_statistics()
        
        # Should return demo data
        assert 'total' in stats
        assert stats['total'] == 48  # From demo data


class TestConfigManager:
    """Test configuration manager"""
    
    def test_config_loading(self):
        """Test configuration loading from environment"""
        import os
        from src.database.config import ConfigManager
        
        # Set environment variables
        os.environ['DB_SERVER'] = 'test-server'
        os.environ['DB_DATABASE'] = 'test-db'
        os.environ['APP_TITLE'] = 'Test App'
        
        # Create config manager (will load from env)
        config = ConfigManager()
        
        assert config.db_config.server == 'test-server'
        assert config.db_config.database == 'test-db'
        assert config.app_config.title == 'Test App'
        
        # Cleanup
        del os.environ['DB_SERVER']
        del os.environ['DB_DATABASE']
        del os.environ['APP_TITLE']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])