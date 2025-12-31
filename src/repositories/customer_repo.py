"""
Customer Repository Implementation
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from src.repositories.base_repository import BaseRepository

@dataclass
class Customer:
    """Customer entity class"""
    customer_id: int = 0
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    cnic: str = ""
    address: str = ""
    city: str = ""
    province: str = ""
    date_of_birth: datetime = None
    registration_date: datetime = None
    last_purchase_date: datetime = None
    total_purchases: int = 0
    total_spent: float = 0.0
    customer_type: str = "Individual"
    is_vip: bool = False
    notes: str = ""
    created_date: datetime = None
    
    def __post_init__(self):
        if self.registration_date is None:
            self.registration_date = datetime.now()
        if self.created_date is None:
            self.created_date = datetime.now()
    
    @property
    def full_name(self) -> str:
        """Get customer full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> Optional[int]:
        """Calculate customer age"""
        if self.date_of_birth:
            today = datetime.now()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or \
               (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None


class CustomerRepository(BaseRepository[Customer]):
    """Repository for customer operations"""
    
    def __init__(self):
        super().__init__("Customers")
    
    def to_entity(self, data: Dict) -> Customer:
        """Convert database row to Customer entity"""
        return Customer(
            customer_id=data.get('customer_id', 0),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            cnic=data.get('cnic', ''),
            address=data.get('address', ''),
            city=data.get('city', ''),
            province=data.get('province', ''),
            date_of_birth=self._parse_date(data.get('date_of_birth')),
            registration_date=self._parse_date(data.get('registration_date')),
            last_purchase_date=self._parse_date(data.get('last_purchase_date')),
            total_purchases=data.get('total_purchases', 0),
            total_spent=float(data.get('total_spent', 0)),
            customer_type=data.get('customer_type', 'Individual'),
            is_vip=bool(data.get('is_vip', False)),
            notes=data.get('notes', ''),
            created_date=self._parse_date(data.get('created_date'))
        )
    
    def to_dict(self, customer: Customer) -> Dict:
        """Convert Customer entity to database dictionary"""
        return {
            'customer_id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone': customer.phone,
            'cnic': customer.cnic,
            'address': customer.address,
            'city': customer.city,
            'province': customer.province,
            'date_of_birth': customer.date_of_birth,
            'registration_date': customer.registration_date,
            'last_purchase_date': customer.last_purchase_date,
            'total_purchases': customer.total_purchases,
            'total_spent': customer.total_spent,
            'customer_type': customer.customer_type,
            'is_vip': customer.is_vip,
            'notes': customer.notes,
            'created_date': customer.created_date
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
    
    def search_customers(self, search_term: str) -> List[Customer]:
        """Search customers by name, email, phone, or CNIC"""
        try:
            query = """
            SELECT * FROM Customers
            WHERE first_name LIKE ? OR
                  last_name LIKE ? OR
                  email LIKE ? OR
                  phone LIKE ? OR
                  cnic LIKE ? OR
                  address LIKE ?
            ORDER BY last_name, first_name
            """
            
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern,
                     search_pattern, search_pattern, search_pattern)
            
            results = db.execute_query(query, params)
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error searching customers: {e}")
            return []
    
    def get_vip_customers(self) -> List[Customer]:
        """Get all VIP customers"""
        return self.get_by_field('is_vip', True)
    
    def get_customers_by_type(self, customer_type: str) -> List[Customer]:
        """Get customers by type (Individual, Corporate, Government)"""
        return self.get_by_field('customer_type', customer_type)
    
    def get_top_customers(self, limit: int = 10) -> List[Customer]:
        """Get top customers by total spent"""
        try:
            query = """
            SELECT * FROM Customers
            WHERE total_spent > 0
            ORDER BY total_spent DESC
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            """
            
            results = db.execute_query(query, (limit,))
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error getting top customers: {e}")
            return []
    
    def get_recent_customers(self, days: int = 30) -> List[Customer]:
        """Get customers registered in recent days"""
        try:
            query = """
            SELECT * FROM Customers
            WHERE registration_date >= DATEADD(day, -?, GETDATE())
            ORDER BY registration_date DESC
            """
            
            results = db.execute_query(query, (days,))
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error getting recent customers: {e}")
            return []
    
    def get_customer_purchase_history(self, customer_id: int) -> List[Dict]:
        """Get purchase history for a customer"""
        try:
            query = """
            SELECT 
                s.sale_id,
                s.sale_date,
                s.sale_price,
                s.final_amount,
                s.payment_method,
                v.vehicle_id,
                v.color,
                v.manufacturing_year,
                v.vin,
                vm.model_name,
                m.name as manufacturer_name,
                e.first_name + ' ' + e.last_name as sales_person
            FROM Sales s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
            JOIN Employees e ON s.employee_id = e.employee_id
            WHERE s.customer_id = ?
            ORDER BY s.sale_date DESC
            """
            
            return db.execute_query(query, (customer_id,))
            
        except Exception as e:
            self.logger.error(f"Error getting purchase history for customer {customer_id}: {e}")
            return []
    
    def get_customer_statistics(self) -> Dict[str, Any]:
        """Get customer statistics"""
        try:
            # Total customers
            total_query = "SELECT COUNT(*) as count FROM Customers"
            total_result = db.execute_query(total_query)
            total_customers = total_result[0]['count'] if total_result else 0
            
            # Customers by type
            type_query = """
            SELECT 
                customer_type,
                COUNT(*) as count,
                AVG(total_spent) as avg_spent
            FROM Customers
            GROUP BY customer_type
            """
            type_results = db.execute_query(type_query)
            
            # VIP customers
            vip_query = "SELECT COUNT(*) as count FROM Customers WHERE is_vip = 1"
            vip_result = db.execute_query(vip_query)
            vip_count = vip_result[0]['count'] if vip_result else 0
            
            # Customers with purchases
            active_query = "SELECT COUNT(*) as count FROM Customers WHERE total_purchases > 0"
            active_result = db.execute_query(active_query)
            active_count = active_result[0]['count'] if active_result else 0
            
            # New customers this month
            new_query = """
            SELECT COUNT(*) as count 
            FROM Customers 
            WHERE registration_date >= DATEADD(month, -1, GETDATE())
            """
            new_result = db.execute_query(new_query)
            new_this_month = new_result[0]['count'] if new_result else 0
            
            return {
                'total_customers': total_customers,
                'vip_count': vip_count,
                'active_customers': active_count,
                'new_this_month': new_this_month,
                'by_type': [
                    {
                        'type': row['customer_type'],
                        'count': row['count'],
                        'avg_spent': row['avg_spent'] or 0
                    }
                    for row in type_results
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting customer statistics: {e}")
            return {
                'total_customers': 0,
                'vip_count': 0,
                'active_customers': 0,
                'new_this_month': 0,
                'by_type': []
            }
    
    def update_customer_stats(self, customer_id: int, 
                            purchase_amount: float = 0) -> bool:
        """Update customer statistics after purchase"""
        try:
            # Get current customer
            customer = self.get_by_id(customer_id)
            if not customer:
                return False
            
            # Update statistics
            if purchase_amount > 0:
                customer.total_purchases += 1
                customer.total_spent += purchase_amount
                customer.last_purchase_date = datetime.now()
                
                # Promote to VIP if threshold reached
                if customer.total_spent >= 10000000 and not customer.is_vip:
                    customer.is_vip = True
            
            return self.update(customer)
            
        except Exception as e:
            self.logger.error(f"Error updating customer stats: {e}")
            return False
    
    def get_customer_credit_score(self, customer_id: int) -> Optional[Dict]:
        """Get customer credit score"""
        try:
            query = """
            SELECT TOP 1 *
            FROM CreditScores
            WHERE customer_id = ?
            ORDER BY report_date DESC
            """
            
            results = db.execute_query(query, (customer_id,))
            return results[0] if results else None
            
        except Exception as e:
            self.logger.error(f"Error getting credit score for customer {customer_id}: {e}")
            return None
    
    def save_credit_score(self, customer_id: int, score: int, 
                         rating: str, provider: str) -> bool:
        """Save customer credit score"""
        try:
            query = """
            INSERT INTO CreditScores (customer_id, score, rating, provider)
            VALUES (?, ?, ?, ?)
            """
            
            db.execute_query(query, (customer_id, score, rating, provider))
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving credit score: {e}")
            return False


# Global repository instance
customer_repository = CustomerRepository()