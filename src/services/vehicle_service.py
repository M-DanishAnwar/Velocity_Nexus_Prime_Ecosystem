"""
Vehicle Service Layer - Business Logic for Your Schema
"""
import logging
from typing import List, Dict, Any, Optional
from Velocity_Nexus_Prime_Ecosystem.src.repositories.vehicle_repo import VehicleRepository

logger = logging.getLogger(__name__)

class VehicleService:
    """Service for vehicle operations using your schema"""
    
    def __init__(self, repository: VehicleRepository = None):
        self.repository = repository or VehicleRepository()
    
    def get_global_performance_vehicles(self) -> List[Dict[str, Any]]:
        """Get global performance vehicles"""
        try:
            vehicles = self.repository.get_global_sports_cars()
            return self._enhance_vehicle_data(vehicles)
        except Exception as e:
            logger.error(f"Error getting global vehicles: {e}")
            return []
    
    def get_pakistani_inventory(self) -> List[Dict[str, Any]]:
        """Get Pakistani vehicles"""
        try:
            vehicles = self.repository.get_pakistani_vehicles()
            return self._enhance_vehicle_data(vehicles)
        except Exception as e:
            logger.error(f"Error getting Pakistani vehicles: {e}")
            return []
    
    def get_high_performance_vehicles(self, min_horsepower: int = 300) -> List[Dict[str, Any]]:
        """Get high performance vehicles"""
        try:
            vehicles = self.repository.get_high_performance_vehicles(min_horsepower)
            return self._enhance_vehicle_data(vehicles)
        except Exception as e:
            logger.error(f"Error getting high performance vehicles: {e}")
            return []
    
    def get_all_vehicles(self) -> List[Dict[str, Any]]:
        """Get all vehicles"""
        try:
            vehicles = self.repository.get_all_vehicles()
            return self._enhance_vehicle_data(vehicles)
        except Exception as e:
            logger.error(f"Error getting all vehicles: {e}")
            return []
    
    def search_vehicles(self, search_term: str = None, 
                       min_price: float = None, 
                       max_price: float = None,
                       vehicle_type: str = None) -> List[Dict[str, Any]]:
        """Search vehicles with filters"""
        try:
            vehicles = self.repository.search_vehicles(search_term, min_price, max_price, vehicle_type)
            return self._enhance_vehicle_data(vehicles)
        except Exception as e:
            logger.error(f"Error searching vehicles: {e}")
            return []
    
    def _enhance_vehicle_data(self, vehicles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance vehicle data with business logic"""
        for vehicle in vehicles:
            # Format price
            if 'current_price' in vehicle:
                vehicle['formatted_price'] = f"PKR {vehicle['current_price']:,.0f}"
            
            # Calculate performance rating
            if 'horsepower' in vehicle:
                vehicle['performance_rating'] = self._calculate_performance_rating(
                    vehicle.get('horsepower', 0),
                    vehicle.get('acceleration_0_100', 10)
                )
            
            # Determine category
            vehicle['category'] = self._determine_category(vehicle)
            
            # Add icon
            vehicle['icon'] = self._get_vehicle_icon(vehicle)
        
        return vehicles
    
    def _calculate_performance_rating(self, horsepower: int, acceleration: float) -> str:
        """Calculate performance rating"""
        if horsepower >= 800:
            return "🔥 Hypercar Performance"
        elif horsepower >= 500:
            return "⚡ High Performance"
        elif horsepower >= 300:
            return "⚡ Sports Performance"
        elif horsepower >= 150:
            return "✅ Standard Performance"
        else:
            return "💰 Economy"
    
    def _determine_category(self, vehicle: Dict[str, Any]) -> str:
        """Determine vehicle category"""
        brand = vehicle.get('brand_name', '').lower()
        horsepower = vehicle.get('horsepower', 0)
        
        if 'bugatti' in brand or horsepower > 1000:
            return "🌍 Global Hypercar"
        elif 'bmw' in brand or 'mercedes' in brand:
            return "🌍 Global Luxury"
        elif 'honda' in brand or 'toyota' in brand or 'suzuki' in brand:
            return "🇵🇰 Pakistani Local"
        else:
            return "🌏 Regional"
    
    def _get_vehicle_icon(self, vehicle: Dict[str, Any]) -> str:
        """Get emoji icon for vehicle"""
        category = vehicle.get('category', '').lower()
        
        if 'hypercar' in category:
            return "🚀"
        elif 'luxury' in category:
            return "🏎️"
        elif 'sports' in category:
            return "⚡"
        elif 'pakistani' in category:
            return "🇵🇰"
        else:
            return "🚗"
    
    def calculate_tax(self, vehicle_price: float, import_status: str = 'Local') -> Dict[str, float]:
        """Calculate tax for vehicle"""
        tax_rates = {
            'Local': 0.17,      # 17% GST
            'Imported': 0.35,    # 35% Luxury Tax
            'Electric': 0.05     # 5% for electric
        }
        
        rate = tax_rates.get(import_status, 0.17)
        tax_amount = vehicle_price * rate
        total = vehicle_price + tax_amount
        
        return {
            'base_price': vehicle_price,
            'tax_rate': rate * 100,
            'tax_amount': tax_amount,
            'total_price': total
        }