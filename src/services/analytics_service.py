"""
Analytics Service for Charts and Reports
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import logging
from src.database.connection import db
from src.database.config import config

class AnalyticsService:
    """Service for generating analytics and reports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.demo_data = self._create_demo_data()
    
    def _create_demo_data(self) -> Dict:
        """Create demo data for demo mode"""
        # Months for the last year
        months = [(datetime.now() - timedelta(days=30*i)).strftime('%b') for i in range(11, -1, -1)]
        
        return {
            'monthly_sales': {
                'months': months,
                'revenue': [45, 52, 48, 61, 55, 65, 70, 75, 80, 78, 82, 85],  # in millions
                'units': [12, 15, 14, 18, 16, 20, 22, 24, 25, 23, 26, 28]
            },
            'sales_by_category': {
                'categories': ['Sedan', 'SUV', 'Hatchback', 'Luxury', 'Electric', 'Commercial'],
                'values': [35, 28, 20, 12, 5, 10],
                'colors': ['#00adb5', '#ff9a76', '#6a2c70', '#08d9d6', '#ff2e63', '#f8b400']
            },
            'inventory_stats': {
                'total': 48,
                'available': 32,
                'sold': 12,
                'reserved': 4,
                'by_status': {'Available': 32, 'Sold': 12, 'Reserved': 4},
                'by_type': {'Sedan': 18, 'SUV': 15, 'Hatchback': 8, 'Luxury': 4, 'Electric': 3}
            },
            'top_performers': [
                {'name': 'Toyota Corolla', 'sales': 45, 'revenue': 202.5},
                {'name': 'Honda Civic', 'sales': 32, 'revenue': 208},
                {'name': 'Suzuki Alto', 'sales': 28, 'revenue': 61.6},
                {'name': 'Toyota Fortuner', 'sales': 18, 'revenue': 225},
                {'name': 'MG ZS EV', 'sales': 12, 'revenue': 102}
            ],
            'customer_metrics': {
                'total': 128,
                'new_this_month': 15,
                'vip_count': 8,
                'avg_purchase': 5.2,  # in millions
                'repeat_rate': 0.35  # 35% repeat customers
            }
        }
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get all dashboard statistics"""
        if config.is_demo_mode():
            return self._get_demo_dashboard_stats()
        
        try:
            stats = {}
            
            # Vehicle statistics
            stats['vehicle_stats'] = self.get_vehicle_statistics()
            
            # Sales statistics
            stats['sales_stats'] = self.get_sales_statistics()
            
            # Customer statistics
            stats['customer_stats'] = self.get_customer_statistics()
            
            # Revenue statistics
            stats['revenue_stats'] = self.get_revenue_statistics()
            
            # Monthly trends
            stats['monthly_trends'] = self.get_monthly_trends()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard stats: {e}")
            return self._get_demo_dashboard_stats()
    
    def get_vehicle_statistics(self) -> Dict[str, Any]:
        """Get vehicle-related statistics"""
        if config.is_demo_mode():
            return self.demo_data['inventory_stats']
        
        try:
            query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available,
                SUM(CASE WHEN status = 'Sold' THEN 1 ELSE 0 END) as sold,
                SUM(CASE WHEN status = 'Reserved' THEN 1 ELSE 0 END) as reserved,
                AVG(current_price) as avg_price,
                MIN(current_price) as min_price,
                MAX(current_price) as max_price
            FROM Vehicles
            """
            
            result = db.execute_query(query)
            if result:
                stats = result[0]
                
                # Get vehicles by type
                type_query = """
                SELECT 
                    vt.type_name,
                    COUNT(v.vehicle_id) as count
                FROM Vehicles v
                JOIN VehicleModels vm ON v.model_id = vm.model_id
                JOIN VehicleTypes vt ON vm.type_id = vt.type_id
                GROUP BY vt.type_name
                """
                types_result = db.execute_query(type_query)
                types_dict = {item['type_name']: item['count'] for item in types_result}
                
                # Get vehicles by status
                status_query = """
                SELECT 
                    status,
                    COUNT(*) as count
                FROM Vehicles
                GROUP BY status
                """
                status_result = db.execute_query(status_query)
                status_dict = {item['status']: item['count'] for item in status_result}
                
                return {
                    'total': stats['total'],
                    'available': stats['available'],
                    'sold': stats['sold'],
                    'reserved': stats['reserved'],
                    'avg_price': stats['avg_price'] or 0,
                    'min_price': stats['min_price'] or 0,
                    'max_price': stats['max_price'] or 0,
                    'by_type': types_dict,
                    'by_status': status_dict
                }
            
            return self.demo_data['inventory_stats']
            
        except Exception as e:
            self.logger.error(f"Error getting vehicle stats: {e}")
            return self.demo_data['inventory_stats']
    
    def get_sales_statistics(self) -> Dict[str, Any]:
        """Get sales-related statistics"""
        if config.is_demo_mode():
            return {
                'total_sales': 128,
                'monthly_sales': 28,
                'monthly_revenue': 85.2,  # in millions
                'avg_sale_value': 6.65,  # in millions
                'best_selling': 'Toyota Corolla'
            }
        
        try:
            # Get current month sales
            current_month = datetime.now().strftime('%Y-%m')
            
            query = """
            SELECT 
                COUNT(*) as total_sales,
                SUM(final_amount) as total_revenue,
                AVG(final_amount) as avg_sale_value
            FROM Sales
            WHERE sale_status = 'Completed'
            """
            
            result = db.execute_query(query)
            if result:
                stats = result[0]
                
                # Get current month stats
                monthly_query = f"""
                SELECT 
                    COUNT(*) as monthly_sales,
                    SUM(final_amount) as monthly_revenue
                FROM Sales
                WHERE sale_status = 'Completed'
                    AND FORMAT(sale_date, 'yyyy-MM') = '{current_month}'
                """
                monthly_result = db.execute_query(monthly_query)
                monthly_stats = monthly_result[0] if monthly_result else {'monthly_sales': 0, 'monthly_revenue': 0}
                
                # Get best selling model
                best_query = """
                SELECT TOP 1
                    vm.model_name
                FROM Sales s
                JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
                JOIN VehicleModels vm ON v.model_id = vm.model_id
                GROUP BY vm.model_name
                ORDER BY COUNT(s.sale_id) DESC
                """
                best_result = db.execute_query(best_query)
                best_selling = best_result[0]['model_name'] if best_result else 'N/A'
                
                return {
                    'total_sales': stats['total_sales'] or 0,
                    'monthly_sales': monthly_stats['monthly_sales'] or 0,
                    'monthly_revenue': (monthly_stats['monthly_revenue'] or 0) / 1000000,  # Convert to millions
                    'avg_sale_value': (stats['avg_sale_value'] or 0) / 1000000,
                    'best_selling': best_selling,
                    'total_revenue': (stats['total_revenue'] or 0) / 1000000
                }
            
            return self.demo_data['sales_stats']
            
        except Exception as e:
            self.logger.error(f"Error getting sales stats: {e}")
            return self.demo_data['sales_stats']
    
    def get_monthly_trends(self) -> Dict[str, List]:
        """Get monthly sales trends"""
        if config.is_demo_mode():
            return self.demo_data['monthly_sales']
        
        try:
            query = """
            SELECT 
                FORMAT(sale_date, 'yyyy-MM') as month,
                COUNT(*) as units_sold,
                SUM(final_amount) as revenue
            FROM Sales
            WHERE sale_status = 'Completed'
                AND sale_date >= DATEADD(month, -12, GETDATE())
            GROUP BY FORMAT(sale_date, 'yyyy-MM')
            ORDER BY month
            """
            
            result = db.execute_query(query)
            
            if result:
                months = [datetime.strptime(item['month'], '%Y-%m').strftime('%b') for item in result]
                units = [item['units_sold'] for item in result]
                revenue = [(item['revenue'] or 0) / 1000000 for item in result]  # Convert to millions
                
                return {
                    'months': months,
                    'units': units,
                    'revenue': revenue
                }
            
            return self.demo_data['monthly_sales']
            
        except Exception as e:
            self.logger.error(f"Error getting monthly trends: {e}")
            return self.demo_data['monthly_sales']
    
    def get_sales_by_category(self) -> Dict[str, List]:
        """Get sales distribution by vehicle category"""
        if config.is_demo_mode():
            return self.demo_data['sales_by_category']
        
        try:
            query = """
            SELECT 
                vt.type_name as category,
                COUNT(s.sale_id) as sales_count,
                SUM(s.final_amount) as revenue
            FROM Sales s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN VehicleTypes vt ON vm.type_id = vt.type_id
            WHERE s.sale_status = 'Completed'
            GROUP BY vt.type_name
            ORDER BY sales_count DESC
            """
            
            result = db.execute_query(query)
            
            if result:
                categories = [item['category'] for item in result]
                values = [item['sales_count'] for item in result]
                
                # Color palette
                colors = ['#00adb5', '#ff9a76', '#6a2c70', '#08d9d6', 
                         '#ff2e63', '#f8b400', '#95e1d3', '#fce38a']
                
                return {
                    'categories': categories,
                    'values': values,
                    'colors': colors[:len(categories)]
                }
            
            return self.demo_data['sales_by_category']
            
        except Exception as e:
            self.logger.error(f"Error getting sales by category: {e}")
            return self.demo_data['sales_by_category']
    
    def get_top_performing_models(self, limit: int = 5) -> List[Dict]:
        """Get top performing vehicle models"""
        if config.is_demo_mode():
            return self.demo_data['top_performers'][:limit]
        
        try:
            query = f"""
            SELECT TOP {limit}
                m.name + ' ' + vm.model_name as name,
                COUNT(s.sale_id) as sales,
                SUM(s.final_amount) as revenue
            FROM Sales s
            JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN VehicleModels vm ON v.model_id = vm.model_id
            JOIN Manufacturers m ON vm.manufacturer_id = m.manufacturer_id
            WHERE s.sale_status = 'Completed'
            GROUP BY m.name, vm.model_name
            ORDER BY sales DESC
            """
            
            result = db.execute_query(query)
            
            if result:
                return [
                    {
                        'name': item['name'],
                        'sales': item['sales'],
                        'revenue': (item['revenue'] or 0) / 1000000  # Convert to millions
                    }
                    for item in result
                ]
            
            return self.demo_data['top_performers'][:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting top performers: {e}")
            return self.demo_data['top_performers'][:limit]
    
    def get_revenue_statistics(self) -> Dict[str, Any]:
        """Get revenue-related statistics"""
        if config.is_demo_mode():
            return {
                'total_revenue': 156.8,  # in millions
                'monthly_revenue': 85.2,
                'growth_rate': 0.23,  # 23%
                'avg_monthly': 65.3
            }
        
        try:
            query = """
            SELECT 
                SUM(final_amount) as total_revenue,
                AVG(final_amount) as avg_revenue
            FROM Sales
            WHERE sale_status = 'Completed'
            """
            
            result = db.execute_query(query)
            
            if result:
                total = (result[0]['total_revenue'] or 0) / 1000000
                avg = (result[0]['avg_revenue'] or 0) / 1000000
                
                # Get growth rate
                growth_query = """
                SELECT 
                    (SUM(CASE WHEN sale_date >= DATEADD(month, -1, GETDATE()) THEN final_amount ELSE 0 END) -
                     SUM(CASE WHEN sale_date >= DATEADD(month, -2, GETDATE()) 
                               AND sale_date < DATEADD(month, -1, GETDATE()) 
                               THEN final_amount ELSE 0 END)) /
                    NULLIF(SUM(CASE WHEN sale_date >= DATEADD(month, -2, GETDATE()) 
                                     AND sale_date < DATEADD(month, -1, GETDATE()) 
                                     THEN final_amount ELSE 0 END), 0) as growth_rate
                FROM Sales
                WHERE sale_status = 'Completed'
                """
                
                growth_result = db.execute_query(growth_query)
                growth_rate = growth_result[0]['growth_rate'] if growth_result and growth_result[0]['growth_rate'] else 0
                
                return {
                    'total_revenue': total,
                    'avg_revenue': avg,
                    'growth_rate': growth_rate,
                    'monthly_revenue': self._get_current_month_revenue()
                }
            
            return self.demo_data['revenue_stats']
            
        except Exception as e:
            self.logger.error(f"Error getting revenue stats: {e}")
            return self.demo_data['revenue_stats']
    
    def _get_current_month_revenue(self) -> float:
        """Get current month revenue"""
        try:
            current_month = datetime.now().strftime('%Y-%m')
            query = f"""
            SELECT SUM(final_amount) as revenue
            FROM Sales
            WHERE sale_status = 'Completed'
                AND FORMAT(sale_date, 'yyyy-MM') = '{current_month}'
            """
            
            result = db.execute_query(query)
            return (result[0]['revenue'] or 0) / 1000000 if result else 0
            
        except Exception as e:
            self.logger.error(f"Error getting current month revenue: {e}")
            return 0
    
    def get_customer_statistics(self) -> Dict[str, Any]:
        """Get customer-related statistics"""
        if config.is_demo_mode():
            return self.demo_data['customer_metrics']
        
        try:
            query = """
            SELECT 
                COUNT(*) as total_customers,
                SUM(CASE WHEN is_vip = 1 THEN 1 ELSE 0 END) as vip_count,
                AVG(total_spent) as avg_spent,
                AVG(total_purchases) as avg_purchases
            FROM Customers
            """
            
            result = db.execute_query(query)
            
            if result:
                stats = result[0]
                
                # Get new customers this month
                new_customers_query = """
                SELECT COUNT(*) as new_customers
                FROM Customers
                WHERE registration_date >= DATEADD(month, -1, GETDATE())
                """
                new_result = db.execute_query(new_customers_query)
                new_customers = new_result[0]['new_customers'] if new_result else 0
                
                # Get repeat customer rate
                repeat_query = """
                SELECT 
                    COUNT(CASE WHEN total_purchases > 1 THEN 1 END) * 1.0 / 
                    NULLIF(COUNT(*), 0) as repeat_rate
                FROM Customers
                WHERE total_purchases > 0
                """
                repeat_result = db.execute_query(repeat_query)
                repeat_rate = repeat_result[0]['repeat_rate'] if repeat_result else 0
                
                return {
                    'total': stats['total_customers'] or 0,
                    'vip_count': stats['vip_count'] or 0,
                    'avg_spent': (stats['avg_spent'] or 0) / 1000000,
                    'avg_purchases': stats['avg_purchases'] or 0,
                    'new_this_month': new_customers,
                    'repeat_rate': repeat_rate
                }
            
            return self.demo_data['customer_metrics']
            
        except Exception as e:
            self.logger.error(f"Error getting customer stats: {e}")
            return self.demo_data['customer_metrics']
    
    def _get_demo_dashboard_stats(self) -> Dict[str, Any]:
        """Get demo dashboard statistics"""
        return {
            'vehicle_stats': self.demo_data['inventory_stats'],
            'sales_stats': {
                'total_sales': 128,
                'monthly_sales': 28,
                'monthly_revenue': 85.2,
                'avg_sale_value': 6.65,
                'best_selling': 'Toyota Corolla',
                'total_revenue': 156.8
            },
            'customer_stats': self.demo_data['customer_metrics'],
            'revenue_stats': {
                'total_revenue': 156.8,
                'monthly_revenue': 85.2,
                'growth_rate': 0.23,
                'avg_monthly': 65.3
            },
            'monthly_trends': self.demo_data['monthly_sales'],
            'sales_by_category': self.demo_data['sales_by_category'],
            'top_performers': self.demo_data['top_performers'][:5]
        }
    
    def generate_sales_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate comprehensive sales report"""
        report = {
            'summary': {},
            'by_category': [],
            'by_manufacturer': [],
            'by_salesperson': [],
            'top_vehicles': []
        }
        
        if config.is_demo_mode():
            # Generate demo report
            report['summary'] = {
                'total_sales': 28,
                'total_revenue': 85.2,
                'avg_sale_value': 6.65,
                'total_commission': 4.26,
                'total_tax': 14.48
            }
            
            report['by_category'] = [
                {'category': 'Sedan', 'sales': 12, 'revenue': 42.3},
                {'category': 'SUV', 'sales': 8, 'revenue': 24.8},
                {'category': 'Hatchback', 'sales': 5, 'revenue': 11.5},
                {'category': 'Luxury', 'sales': 2, 'revenue': 6.1},
                {'category': 'Electric', 'sales': 1, 'revenue': 0.5}
            ]
            
            report['top_vehicles'] = self.demo_data['top_performers'][:5]
            
        return report


# Global analytics service instance
analytics_service = AnalyticsService()