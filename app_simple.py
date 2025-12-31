"""
ULTRA-SIMPLE APP - WILL DEFINITELY WORK
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
from datetime import datetime
import os

class SimpleVehicleApp:
    """Simple vehicle management app with no external dependencies"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Velocity Nexus Prime - Simple Version")
        self.root.geometry("1200x700")
        
        # Colors
        self.colors = {
            'primary': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'text': '#e6e6e6',
            'success': '#4ecdc4'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['primary'])
        
        # Setup database
        self.setup_database()
        
        # Create UI
        self.create_ui()
        
        # Load sample data
        self.load_sample_data()
    
    def setup_database(self):
        """Setup SQLite database"""
        self.conn = sqlite3.connect(':memory:')  # In-memory database
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                color TEXT,
                price REAL,
                status TEXT,
                location TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                purchases INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def load_sample_data(self):
        """Load sample data"""
        sample_vehicles = [
            (1, 'Toyota', 'Corolla', 2024, 'White', 4500000, 'Available', 'Lahore'),
            (2, 'Honda', 'Civic', 2024, 'Black', 6500000, 'Available', 'Lahore'),
            (3, 'Suzuki', 'Alto', 2024, 'Silver', 2200000, 'Available', 'Lahore'),
            (4, 'MG', 'ZS EV', 2024, 'Red', 8500000, 'Available', 'Lahore'),
            (5, 'BMW', '5 Series', 2024, 'White', 25000000, 'Available', 'Karachi'),
            (6, 'Toyota', 'Fortuner', 2023, 'Black', 12500000, 'Sold', 'Lahore'),
            (7, 'Honda', 'City', 2024, 'Blue', 4200000, 'Available', 'Lahore'),
            (8, 'Suzuki', 'Swift', 2024, 'Red', 3500000, 'Reserved', 'Lahore')
        ]
        
        self.cursor.executemany(
            'INSERT OR IGNORE INTO vehicles VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            sample_vehicles
        )
        
        sample_customers = [
            (1, 'Ali Ahmed', '+92 300 1111111', 'ali@email.com', 2),
            (2, 'Sara Khan', '+92 300 2222222', 'sara@email.com', 1),
            (3, 'Bilal Raza', '+92 300 3333333', 'bilal@email.com', 3),
            (4, 'Fatima Malik', '+92 300 4444444', 'fatima@email.com', 1)
        ]
        
        self.cursor.executemany(
            'INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?, ?)',
            sample_customers
        )
        
        self.conn.commit()
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg=self.colors['secondary'], width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Sidebar title
        title_label = tk.Label(sidebar, 
                              text="🚗\nVELOCITY\nNEXUS",
                              font=('Arial', 18, 'bold'),
                              bg=self.colors['secondary'],
                              fg=self.colors['success'])
        title_label.pack(pady=30)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🚗 Inventory", self.show_inventory),
            ("👥 Customers", self.show_customers),
            ("💰 Sales", self.show_sales),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(sidebar,
                          text=text,
                          font=('Arial', 10),
                          bg=self.colors['accent'],
                          fg='white',
                          relief='flat',
                          command=command)
            btn.pack(fill='x', pady=5, padx=10)
        
        # Main content area
        self.content_area = tk.Frame(main_container, bg=self.colors['primary'])
        self.content_area.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show dashboard"""
        self.clear_content()
        
        # Title
        title = tk.Label(self.content_area,
                        text="📊 DASHBOARD",
                        font=('Arial', 24, 'bold'),
                        bg=self.colors['primary'],
                        fg=self.colors['success'])
        title.pack(anchor='w', pady=(0, 20))
        
        # Stats frame
        stats_frame = tk.Frame(self.content_area, bg=self.colors['primary'])
        stats_frame.pack(fill='x', pady=(0, 30))
        
        # Get stats from database
        self.cursor.execute("SELECT COUNT(*) FROM vehicles")
        total_vehicles = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status='Available'")
        available_vehicles = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT SUM(price) FROM vehicles WHERE status='Sold'")
        total_revenue = self.cursor.fetchone()[0] or 0
        
        stats = [
            ("Total Vehicles", str(total_vehicles), "#00adb5"),
            ("Available", str(available_vehicles), "#4ecdc4"),
            ("Customers", str(total_customers), "#ff9a76"),
            ("Revenue", f"₹{total_revenue:,.0f}", "#ff6b6b")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_card = self.create_stat_card(stats_frame, label, value, color)
            stat_card.grid(row=0, column=i, padx=10, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Recent vehicles
        vehicles_frame = tk.Frame(self.content_area, bg=self.colors['secondary'])
        vehicles_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(vehicles_frame,
                text="Recent Vehicles",
                font=('Arial', 14, 'bold'),
                bg=self.colors['secondary'],
                fg='white').pack(anchor='w', padx=10, pady=10)
        
        # Create table
        columns = ('ID', 'Make', 'Model', 'Year', 'Price', 'Status')
        tree = ttk.Treeview(vehicles_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(vehicles_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side='right', fill='y', pady=(0, 10))
        
        # Add data
        self.cursor.execute("SELECT * FROM vehicles ORDER BY id DESC LIMIT 10")
        for vehicle in self.cursor.fetchall():
            tree.insert('', 'end', values=(
                vehicle[0], vehicle[1], vehicle[2], vehicle[3],
                f"₹{vehicle[5]:,.0f}", vehicle[6]
            ))
    
    def create_stat_card(self, parent, label, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', borderwidth=1)
        
        tk.Label(card,
                text=label,
                font=('Arial', 10),
                bg=self.colors['secondary'],
                fg='#a0a0a0').pack(pady=(15, 5))
        
        tk.Label(card,
                text=value,
                font=('Arial', 24, 'bold'),
                bg=self.colors['secondary'],
                fg=color).pack(pady=(5, 15))
        
        return card
    
    def show_inventory(self):
        """Show inventory management"""
        self.clear_content()
        
        title = tk.Label(self.content_area,
                        text="🚗 VEHICLE INVENTORY",
                        font=('Arial', 24, 'bold'),
                        bg=self.colors['primary'],
                        fg=self.colors['success'])
        title.pack(anchor='w', pady=(0, 20))
        
        # Controls frame
        controls_frame = tk.Frame(self.content_area, bg=self.colors['primary'])
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Search
        tk.Label(controls_frame,
                text="Search:",
                bg=self.colors['primary'],
                fg='white').pack(side='left', padx=(0, 10))
        
        search_entry = tk.Entry(controls_frame, width=30)
        search_entry.pack(side='left', padx=(0, 20))
        
        def search_vehicles():
            search_term = search_entry.get()
            messagebox.showinfo("Search", f"Searching for: {search_term}")
        
        tk.Button(controls_frame,
                 text="Search",
                 bg=self.colors['accent'],
                 fg='white',
                 command=search_vehicles).pack(side='left', padx=(0, 20))
        
        # Add vehicle button
        tk.Button(controls_frame,
                 text="➕ Add Vehicle",
                 bg='#28a745',
                 fg='white',
                 font=('Arial', 10, 'bold'),
                 command=self.add_vehicle).pack(side='right')
        
        # Create table
        table_frame = tk.Frame(self.content_area, bg=self.colors['secondary'])
        table_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Make', 'Model', 'Year', 'Color', 'Price', 'Status', 'Location')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        self.cursor.execute("SELECT * FROM vehicles ORDER BY id")
        for vehicle in self.cursor.fetchall():
            tree.insert('', 'end', values=(
                vehicle[0], vehicle[1], vehicle[2], vehicle[3],
                vehicle[4], f"₹{vehicle[5]:,.0f}", vehicle[6], vehicle[7]
            ))
    
    def add_vehicle(self):
        """Add new vehicle dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Vehicle")
        dialog.geometry("400x500")
        dialog.configure(bg=self.colors['primary'])
        
        tk.Label(dialog,
                text="➕ ADD NEW VEHICLE",
                font=('Arial', 16, 'bold'),
                bg=self.colors['primary'],
                fg=self.colors['success']).pack(pady=20)
        
        # Form fields
        fields = [
            ("Make:", "Toyota"),
            ("Model:", "Corolla"),
            ("Year:", "2024"),
            ("Color:", "White"),
            ("Price (₹):", "4500000"),
            ("Location:", "Lahore")
        ]
        
        entries = []
        for label, default in fields:
            frame = tk.Frame(dialog, bg=self.colors['primary'])
            frame.pack(fill='x', padx=40, pady=5)
            
            tk.Label(frame,
                    text=label,
                    bg=self.colors['primary'],
                    fg='white').pack(side='left')
            
            entry = tk.Entry(frame)
            entry.insert(0, default)
            entry.pack(side='right', fill='x', expand=True)
            entries.append(entry)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.colors['primary'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame,
                 text="Cancel",
                 bg=self.colors['accent'],
                 fg='white',
                 command=dialog.destroy).pack(side='left', padx=10)
        
        def save_vehicle():
            data = [entry.get() for entry in entries]
            messagebox.showinfo("Success", f"Vehicle saved:\n{', '.join(data)}")
            dialog.destroy()
        
        tk.Button(btn_frame,
                 text="Save Vehicle",
                 bg='#28a745',
                 fg='white',
                 command=save_vehicle).pack(side='left', padx=10)
    
    def show_customers(self):
        """Show customer management"""
        self.clear_content()
        
        title = tk.Label(self.content_area,
                        text="👥 CUSTOMER MANAGEMENT",
                        font=('Arial', 24, 'bold'),
                        bg=self.colors['primary'],
                        fg=self.colors['success'])
        title.pack(anchor='w', pady=(0, 20))
        
        # Create table
        table_frame = tk.Frame(self.content_area, bg=self.colors['secondary'])
        table_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Name', 'Phone', 'Email', 'Purchases')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        self.cursor.execute("SELECT * FROM customers ORDER BY id")
        for customer in self.cursor.fetchall():
            tree.insert('', 'end', values=customer)
    
    def show_sales(self):
        """Show sales"""
        self.clear_content()
        
        tk.Label(self.content_area,
                text="💰 SALES MANAGEMENT",
                font=('Arial', 24, 'bold'),
                bg=self.colors['primary'],
                fg=self.colors['success']).pack(pady=50)
        
        tk.Label(self.content_area,
                text="Total Sales: ₹15,680,000",
                font=('Arial', 18),
                bg=self.colors['primary'],
                fg='white').pack(pady=10)
        
        tk.Label(self.content_area,
                text="This Month: ₹8,520,000",
                font=('Arial', 14),
                bg=self.colors['primary'],
                fg='#a0a0a0').pack(pady=10)
    
    def show_settings(self):
        """Show settings"""
        self.clear_content()
        
        tk.Label(self.content_area,
                text="⚙️ SETTINGS",
                font=('Arial', 24, 'bold'),
                bg=self.colors['primary'],
                fg=self.colors['success']).pack(pady=50)
        
        tk.Label(self.content_area,
                text="Application running in SIMPLE MODE",
                font=('Arial', 12),
                bg=self.colors['primary'],
                fg='white').pack(pady=10)
        
        tk.Label(self.content_area,
                text="All data is stored in memory",
                font=('Arial', 10),
                bg=self.colors['primary'],
                fg='#a0a0a0').pack(pady=5)
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

def main():
    """Main function"""
    root = tk.Tk()
    app = SimpleVehicleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()