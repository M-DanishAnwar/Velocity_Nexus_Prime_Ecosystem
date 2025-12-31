"""
Vehicle Repository with Business-Specific Operations
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from src.repositories.base_repository import BaseRepository

@dataclass
class Vehicle:
    """Vehicle entity class"""
    vehicle_id: int = 0
    model_id: int = 0
    dealership_id: int = 0
    vin: str = ""
    chassis_number: str = ""
    color: str = ""
    manufacturing_year: int = 2024
    registration_number: str = ""
    mileage_km: int = 0
    purchase_price: float = 0.0
    current_price: float = 0.0
    status: str = "Available"
    import_status: str = "Local"
    condition: str = "New"
    arrival_date: datetime = None
    sold_date: datetime = None
    created_date: datetime = None
    last_updated: datetime = None
    
    # Joined fields (for display)
    manufacturer_name: str = ""
    model_name: str = ""
    type_name: str = ""
    dealership_name: str = ""
    city: str = ""
    province: str = ""
    
    def __post_init__(self):
        if self.arrival_date is None:
            self.arrival_date = datetime.now()
        if self.created_date is None:
            self.created_date = datetime.now()
        if self.last_updated is None:
            self.last_updated = datetime.now()


class VehicleRepository(BaseRepository[Vehicle]):
    """Repository for vehicle operations"""
    
    def __init__(self):
        super().__init__("Vehicles")
    
    def to_entity(self, data: Dict) -> Vehicle:
        """Convert database row to Vehicle entity"""
        return Vehicle(
            vehicle_id=data.get('vehicle_id', 0),
            model_id=data.get('model_id', 0),
            dealership_id=data.get('dealership_id', 0),
            vin=data.get('vin', ''),
            chassis_number=data.get('chassis_number', ''),
            color=data.get('color', ''),
            manufacturing_year=data.get('manufacturing_year', 2024),
            registration_number=data.get('registration_number', ''),
            mileage_km=data.get('mileage_km', 0),
            purchase_price=float(data.get('purchase_price', 0)),
            current_price=float(data.get('current_price', 0)),
            status=data.get('status', 'Available'),
            import_status=data.get('import_status', 'Local'),
            condition=data.get('condition', 'New'),
            arrival_date=self._parse_date(data.get('arrival_date')),
            sold_date=self._parse_date(data.get('sold_date')),
            created_date=self._parse_date(data.get('created_date')),
            last_updated=self._parse_date(data.get('last_updated')),
            manufacturer_name=data.get('manufacturer_name', ''),
            model_name=data.get('model_name', ''),
            type_name=data.get('type_name', ''),
            dealership_name=data.get('dealership_name', ''),
            city=data.get('city', ''),
            province=data.get('province', '')
        )
    
    def to_dict(self, vehicle: Vehicle) -> Dict:
        """Convert Vehicle entity to database dictionary"""
        return {
            'vehicle_id': vehicle.vehicle_id,
            'model_id': vehicle.model_id,
            'dealership_id': vehicle.dealership_id,
            'vin': vehicle.vin,
            'chassis_number': vehicle.chassis_number,
            'color': vehicle.color,
            'manufacturing_year': vehicle.manufacturing_year,
            'registration_number': vehicle.registration_number,
            'mileage_km': vehicle.mileage_km,
            'purchase_price': vehicle.purchase_price,
            'current_price': vehicle.current_price,
            'status': vehicle.status,
            'import_status': vehicle.import_status,
            'condition': vehicle.condition,
            'arrival_date': vehicle.arrival_date,
            'sold_date': vehicle.sold_date,
            'created_date': vehicle.created_date,
            'last_updated': vehicle.last_updated
        }
    
    def _parse_date(self, date_str):
        """Parse date string to datetime"""
        if not date_str:
            return None
        if isinstance(date_str, datetime):
            return date_str
        try:
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f')
        except:
            try:
                return datetime.strptime(str(date_str), '%Y-%m-%d')
            except:
                return None
    
    def get_available_vehicles(self) -> List[Vehicle]:
        """Get all available vehicles"""
        return self.get_by_field('status', 'Available')
    
    def get_vehicles_by_dealership(self, dealership_id: int) -> List[Vehicle]:
        """Get vehicles by dealership"""
        return self.get_by_field('dealership_id', dealership_id)
    
    def get_vehicles_by_status(self, status: str) -> List[Vehicle]:
        """Get vehicles by status"""
        return self.get_by_field('status', status)
    
    def get_vehicles_by_price_range(self, min_price: float, max_price: float) -> List[Vehicle]:
        """Get vehicles within price range"""
        try:
            query = """
            SELECT * FROM Vehicles 
            WHERE current_price BETWEEN ? AND ? 
                AND status = 'Available'
            ORDER BY current_price
            """
            results = db.execute_query(query, (min_price, max_price))
            return [self.to_entity(row) for row in results]
        except Exception as e:
            self.logger.error(f"Error getting vehicles by price range: {e}")
            return []
    
    def get_vehicles_by_year_range(self, start_year: int, end_year: int) -> List[Vehicle]:
        """Get vehicles by manufacturing year range"""
        try:
            query = """
            SELECT * FROM Vehicles 
            WHERE manufacturing_year BETWEEN ? AND ? 
                AND status = 'Available'
            ORDER BY manufacturing_year DESC
            """
            results = db.execute_query(query, (start_year, end_year))
            return [self.to_entity(row) for row in results]
        except Exception as e:
            self.logger.error(f"Error getting vehicles by year range: {e}")
            return []
    
    def get_vehicle_with_details(self, vehicle_id: int) -> Optional[Vehicle]:
        """Get vehicle with all joined details"""
        try:
            query = """
            SELECT 
                v.*,
                m.name as manufacturer_name,
                vm.model_name,
                vt.type_name,
                d.name as dealership_name,
                d.city,
                d.province
            FROM Vehicles v
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
            JOIN VehicleTypes vt ON vm.type_id = vt.type_id
            JOIN Dealerships d ON v.dealership_id = d.dealership_id
            WHERE v.vehicle_id = ?
            """
            
            results = db.execute_query(query, (vehicle_id,))
            if results:
                return self.to_entity(results[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting vehicle with details ID {vehicle_id}: {e}")
            return None
    
    def search_vehicles(self, search_term: str) -> List[Vehicle]:
        """Search vehicles across multiple fields"""
        try:
            query = """
            SELECT 
                v.*,
                m.name as manufacturer_name,
                vm.model_name,
                vt.type_name,
                d.name as dealership_name,
                d.city
            FROM Vehicles v
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
            JOIN VehicleTypes vt ON vm.type_id = vt.type_id
            JOIN Dealerships d ON v.dealership_id = d.dealership_id
            WHERE v.status = 'Available'
                AND (
                    v.vin LIKE ? OR
                    v.color LIKE ? OR
                    v.registration_number LIKE ? OR
                    m.name LIKE ? OR
                    vm.model_name LIKE ? OR
                    d.name LIKE ? OR
                    d.city LIKE ?
                )
            ORDER BY v.current_price
            """
            
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern,
                     search_pattern, search_pattern, search_pattern, search_pattern)
            
            results = db.execute_query(query, params)
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error searching vehicles: {e}")
            return []
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get inventory summary statistics"""
        try:
            # Get counts by status
            status_query = """
            SELECT 
                status,
                COUNT(*) as count,
                SUM(current_price) as total_value
            FROM Vehicles
            GROUP BY status
            """
            
            status_results = db.execute_query(status_query)
            status_summary = {row['status']: row['count'] for row in status_results}
            total_value = sum(row['total_value'] or 0 for row in status_results)
            
            # Get counts by type
            type_query = """
            SELECT 
                vt.type_name,
                COUNT(v.vehicle_id) as count
            FROM Vehicles v
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN VehicleTypes vt ON vm.type_id = vt.type_id
            WHERE v.status = 'Available'
            GROUP BY vt.type_name
            """
            
            type_results = db.execute_query(type_query)
            type_summary = {row['type_name']: row['count'] for row in type_results}
            
            # Get counts by dealership
            dealership_query = """
            SELECT 
                d.name,
                COUNT(v.vehicle_id) as count,
                SUM(v.current_price) as value
            FROM Vehicles v
            JOIN Dealerships d ON v.dealership_id = d.dealership_id
            WHERE v.status = 'Available'
            GROUP BY d.name
            """
            
            dealership_results = db.execute_query(dealership_query)
            dealership_summary = [
                {'name': row['name'], 'count': row['count'], 'value': row['value']}
                for row in dealership_results
            ]
            
            return {
                'total_count': self.count(),
                'available_count': status_summary.get('Available', 0),
                'sold_count': status_summary.get('Sold', 0),
                'total_value': total_value,
                'by_status': status_summary,
                'by_type': type_summary,
                'by_dealership': dealership_summary
            }
            
        except Exception as e:
            self.logger.error(f"Error getting inventory summary: {e}")
            return {
                'total_count': 0,
                'available_count': 0,
                'sold_count': 0,
                'total_value': 0,
                'by_status': {},
                'by_type': {},
                'by_dealership': []
            }
    
    def update_vehicle_status(self, vehicle_id: int, new_status: str, 
                            employee_id: int = None) -> bool:
        """Update vehicle status with audit trail"""
        try:
            # Get current vehicle
            vehicle = self.get_by_id(vehicle_id)
            if not vehicle:
                self.logger.error(f"Vehicle {vehicle_id} not found")
                return False
            
            old_status = vehicle.status
            vehicle.status = new_status
            vehicle.last_updated = datetime.now()
            
            # Update vehicle
            success = self.update(vehicle)
            
            if success and employee_id:
                # Log to inventory audit
                audit_query = """
                INSERT INTO InventoryAudit (
                    vehicle_id, action_type, old_value, new_value,
                    performed_by, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                db.execute_query(audit_query, (
                    vehicle_id, 'Status Change', old_status, new_status,
                    employee_id, f'Status changed from {old_status} to {new_status}'
                ))
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating vehicle status: {e}")
            return False
    
    def update_vehicle_price(self, vehicle_id: int, new_price: float, 
                           reason: str, employee_id: int) -> bool:
        """Update vehicle price with history tracking"""
        try:
            # Get current vehicle
            vehicle = self.get_by_id(vehicle_id)
            if not vehicle:
                self.logger.error(f"Vehicle {vehicle_id} not found")
                return False
            
            old_price = vehicle.current_price
            vehicle.current_price = new_price
            vehicle.last_updated = datetime.now()
            
            # Update vehicle
            success = self.update(vehicle)
            
            if success:
                # Record price history
                history_query = """
                INSERT INTO PriceHistory (
                    vehicle_id, old_price, new_price,
                    change_reason, changed_by
                )
                VALUES (?, ?, ?, ?, ?)
                """
                
                db.execute_query(history_query, (
                    vehicle_id, old_price, new_price,
                    reason, employee_id
                ))
                
                # Log to inventory audit
                audit_query = """
                INSERT INTO InventoryAudit (
                    vehicle_id, action_type, old_value, new_value,
                    performed_by, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                db.execute_query(audit_query, (
                    vehicle_id, 'Price Update', 
                    str(old_price), str(new_price),
                    employee_id, f'Price changed: {reason}'
                ))
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating vehicle price: {e}")
            return False
    
    def get_price_history(self, vehicle_id: int) -> List[Dict]:
        """Get price history for a vehicle"""
        try:
            query = """
            SELECT 
                ph.*,
                e.first_name + ' ' + e.last_name as changed_by_name
            FROM PriceHistory ph
            LEFT JOIN Employees e ON ph.changed_by = e.employee_id
            WHERE ph.vehicle_id = ?
            ORDER BY ph.change_date DESC
            """
            
            return db.execute_query(query, (vehicle_id,))
            
        except Exception as e:
            self.logger.error(f"Error getting price history for vehicle {vehicle_id}: {e}")
            return []
    
    def get_vehicle_audit_trail(self, vehicle_id: int) -> List[Dict]:
        """Get audit trail for a vehicle"""
        try:
            query = """
            SELECT 
                ia.*,
                e.first_name + ' ' + e.last_name as performed_by_name
            FROM InventoryAudit ia
            LEFT JOIN Employees e ON ia.performed_by = e.employee_id
            WHERE ia.vehicle_id = ?
            ORDER BY ia.audit_date DESC
            """
            
            return db.execute_query(query, (vehicle_id,))
            
        except Exception as e:
            self.logger.error(f"Error getting audit trail for vehicle {vehicle_id}: {e}")
            return []


# Global repository instance
vehicle_repository = VehicleRepository()