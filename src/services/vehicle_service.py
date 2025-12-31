from src.repositories.vehicle_repo import VehicleRepository

class VehicleService:
    def __init__(self):
        self.repo = VehicleRepository()

    def get_dashboard_data(self):
        return self.repo.get_all_inventory()

    def calculate_price_with_tax(self, base_price, import_status):
        """Business Logic: Calculates Tax based on Local vs Imported"""
        tax_rate = 0.17  # 17% GST Standard
        
        if import_status == 'Imported':
            tax_rate = 0.35  # 35% Luxury Tax for Imported
        
        tax_amount = float(base_price) * tax_rate
        total_price = float(base_price) + tax_amount
        return total_price, tax_amount

    def process_sale(self, vehicle_id, customer_name, final_price, tax):
        return self.repo.register_sale(vehicle_id, customer_name, final_price, tax)