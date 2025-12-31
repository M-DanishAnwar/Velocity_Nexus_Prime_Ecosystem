"""
Base Repository Class with CRUD Operations
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic
from src.database.connection import db
import logging

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """Abstract base repository with CRUD operations"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.logger = logging.getLogger(f"Repository.{table_name}")
    
    @abstractmethod
    def to_entity(self, data: Dict) -> T:
        """Convert database row to entity"""
        pass
    
    @abstractmethod
    def to_dict(self, entity: T) -> Dict:
        """Convert entity to database dictionary"""
        pass
    
    def get_all(self, where_clause: str = None, params: tuple = None) -> List[T]:
        """Get all records with optional filter"""
        try:
            query = f"SELECT * FROM {self.table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            
            results = db.execute_query(query, params)
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error getting all {self.table_name}: {e}")
            return []
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get record by ID"""
        try:
            query = f"SELECT * FROM {self.table_name} WHERE {self.table_name[:-1]}_id = ?"
            results = db.execute_query(query, (id,))
            
            if results:
                return self.to_entity(results[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting {self.table_name} by id {id}: {e}")
            return None
    
    def get_by_field(self, field: str, value: Any) -> List[T]:
        """Get records by field value"""
        try:
            query = f"SELECT * FROM {self.table_name} WHERE {field} = ?"
            results = db.execute_query(query, (value,))
            return [self.to_entity(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"Error getting {self.table_name} by {field}={value}: {e}")
            return []
    
    def add(self, entity: T) -> int:
        """Add new record and return ID"""
        try:
            data = self.to_dict(entity)
            
            # Remove ID if present (for auto-increment)
            id_field = f"{self.table_name[:-1]}_id"
            if id_field in data:
                del data[id_field]
            
            inserted_id = db.insert_data(self.table_name, data)
            
            if inserted_id > 0:
                self.logger.info(f"Added {self.table_name} with ID: {inserted_id}")
                return inserted_id
            else:
                self.logger.error(f"Failed to add {self.table_name}")
                return -1
                
        except Exception as e:
            self.logger.error(f"Error adding {self.table_name}: {e}")
            return -1
    
    def update(self, entity: T) -> bool:
        """Update existing record"""
        try:
            data = self.to_dict(entity)
            id_field = f"{self.table_name[:-1]}_id"
            
            if id_field not in data:
                raise ValueError(f"{id_field} is required for update")
            
            entity_id = data[id_field]
            del data[id_field]  # Remove ID from update data
            
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            condition = f"{id_field} = ?"
            
            success = db.update_data(
                self.table_name,
                data,
                condition,
                (entity_id,)
            )
            
            if success:
                self.logger.info(f"Updated {self.table_name} with ID: {entity_id}")
            else:
                self.logger.warning(f"No {self.table_name} found with ID: {entity_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating {self.table_name}: {e}")
            return False
    
    def delete(self, id: int) -> bool:
        """Delete record by ID"""
        try:
            id_field = f"{self.table_name[:-1]}_id"
            query = f"DELETE FROM {self.table_name} WHERE {id_field} = ?"
            
            # For audit purposes, get record before deletion
            record = self.get_by_id(id)
            
            with db.get_connection() as cursor:
                cursor.execute(query, (id,))
                success = cursor.rowcount > 0
            
            if success:
                self.logger.info(f"Deleted {self.table_name} with ID: {id}")
                # Log to audit table if needed
                self._log_deletion(id, record)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error deleting {self.table_name} with ID {id}: {e}")
            return False
    
    def _log_deletion(self, id: int, record: Optional[T]):
        """Log deletion to audit table (override if needed)"""
        pass
    
    def exists(self, id: int) -> bool:
        """Check if record exists by ID"""
        try:
            return self.get_by_id(id) is not None
        except Exception as e:
            self.logger.error(f"Error checking existence of {self.table_name} ID {id}: {e}")
            return False
    
    def count(self, where_clause: str = None, params: tuple = None) -> int:
        """Count records with optional filter"""
        try:
            query = f"SELECT COUNT(*) as count FROM {self.table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            
            results = db.execute_query(query, params)
            return results[0]['count'] if results else 0
            
        except Exception as e:
            self.logger.error(f"Error counting {self.table_name}: {e}")
            return 0
    
    def get_paginated(self, page: int = 1, page_size: int = 50, 
                     order_by: str = None, descending: bool = False) -> Dict[str, Any]:
        """Get paginated results"""
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Build order clause
            order_clause = ""
            if order_by:
                order_clause = f" ORDER BY {order_by}"
                if descending:
                    order_clause += " DESC"
            else:
                id_field = f"{self.table_name[:-1]}_id"
                order_clause = f" ORDER BY {id_field}"
            
            # Get data
            query = f"""
            SELECT * FROM {self.table_name}
            {order_clause}
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """
            
            results = db.execute_query(query, (offset, page_size))
            entities = [self.to_entity(row) for row in results]
            
            # Get total count
            total_count = self.count()
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'data': entities,
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_previous': page > 1,
                'has_next': page < total_pages
            }
            
        except Exception as e:
            self.logger.error(f"Error getting paginated {self.table_name}: {e}")
            return {
                'data': [],
                'page': page,
                'page_size': page_size,
                'total_count': 0,
                'total_pages': 0,
                'has_previous': False,
                'has_next': False
            }
    
    def search(self, search_term: str, search_fields: List[str]) -> List[T]:
        """Search across multiple fields"""
        try:
            if not search_term or not search_fields:
                return []
            
            # Build OR conditions for each field
            conditions = []
            params = []
            
            for field in search_fields:
                conditions.append(f"{field} LIKE ?")
                params.append(f"%{search_term}%")
            
            where_clause = " OR ".join(conditions)
            return self.get_all(where_clause, tuple(params))
            
        except Exception as e:
            self.logger.error(f"Error searching {self.table_name}: {e}")
            return []
    
    def execute_custom_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute custom query"""
        try:
            return db.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"Error executing custom query: {e}")
            return []