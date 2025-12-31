"""
Main Window - Professional Modern UI with Dashboard
"""
import tkinter as tk
from tkinter import ttk, messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os
from datetime import datetime
import threading

class VelocityNexusApp:
    """Main Application Window with Modern UI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Velocity Nexus Prime - Professional Edition")
        self.root.geometry("1400x800")
        self.root.state('zoomed')  # Start maximized
        
        # Modern color palette
        self.colors = {
            # Dark theme - Professional
            'primary': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'text': '#e6e6e6',
            'text_secondary': '#a0a0a0',
            'success': '#4ecdc4',
            'warning': '#ff9a76',
            'danger': '#ff6b6b',
            'info': '#45aaf2',
            'card_bg': '#222831',
            'card_border': '#393e46',
            'hover': '#30475e',
            
            # Chart colors
            'chart1': '#00adb5',
            'chart2': '#ff9a76',
            'chart3': '#6a2c70',
            'chart4': '#08d9d6',
            'chart5': '#ff2e63'
        }
        
        # Setup styles
        self.setup_styles()
        
        # Create UI
        self.create_ui()
        
        # Load data
        self.load_sample_data()  # Demo mode
        
        # Center window
        self.center_window()
        
        # Bind events
        self.bind_events()
        
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Main.TFrame', background=self.colors['primary'])
        style.configure('Sidebar.TFrame', background=self.colors['secondary'])
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       borderwidth=1,
                       relief='solid')
        
        # Label styles
        style.configure('Title.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['success'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 14))
        
        style.configure('CardTitle.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 12, 'bold'))
        
        # Button styles
        style.configure('Nav.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       padding=10)
        
        style.map('Nav.TButton',
                 background=[('active', self.colors['hover'])])
        
        style.configure('Action.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        
        # Entry styles
        style.configure('Search.TEntry',
                       fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='solid')
        
    def create_ui(self):
        """Create the main UI structure"""
        # Main container
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill='both', expand=True)
        
        # ==================== SIDEBAR ====================
        sidebar = ttk.Frame(main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        title_frame.pack(fill='x', pady=(30, 20))
        
        ttk.Label(title_frame, 
                 text="⚡ VELOCITY\nNEXUS PRIME",
                 style='Title.TLabel',
                 justify='center').pack(pady=10)
        
        ttk.Label(title_frame,
                 text="Professional Vehicle Management",
                 foreground=self.colors['text_secondary'],
                 background=self.colors['secondary'],
                 font=('Segoe UI', 9)).pack()
        
        # Navigation buttons
        nav_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        nav_frame.pack(fill='x', padx=20)
        
        nav_buttons = [
            ("📊 DASHBOARD", self.show_dashboard),
            ("🚗 INVENTORY", self.show_inventory),
            ("💰 SALES", self.show_sales),
            ("👥 CUSTOMERS", self.show_customers),
            ("📈 REPORTS", self.show_reports),
            ("⚙️ SETTINGS", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(nav_frame, 
                           text=text,
                           style='Nav.TButton',
                           command=command)
            btn.pack(fill='x', pady=5)
        
        # Status at bottom
        status_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        status_frame.pack(side='bottom', fill='x', pady=20)
        
        self.status_label = ttk.Label(status_frame,
                                     text="🟢 DEMO MODE",
                                     foreground=self.colors['success'],
                                     background=self.colors['secondary'],
                                     font=('Segoe UI', 9))
        self.status_label.pack(pady=5)
        
        ttk.Label(status_frame,
                 text=f"User: Admin | {datetime.now().strftime('%Y-%m-%d')}",
                 foreground=self.colors['text_secondary'],
                 background=self.colors['secondary'],
                 font=('Segoe UI', 8)).pack()
        
        # ==================== MAIN CONTENT ====================
        self.content_area = ttk.Frame(main_container, style='Main.TFrame')
        self.content_area.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Header with search
        self.create_header()
        
        # Main content frame
        self.main_content = ttk.Frame(self.content_area, style='Main.TFrame')
        self.main_content.pack(fill='both', expand=True, pady=(20, 0))
        
        # Show dashboard by default
        self.show_dashboard()
        
    def create_header(self):
        """Create header with search and actions"""
        header = ttk.Frame(self.content_area, style='Main.TFrame')
        header.pack(fill='x')
        
        # Welcome message
        welcome_label = ttk.Label(header,
                                text="Welcome back, Admin 👋",
                                style='Subtitle.TLabel')
        welcome_label.pack(side='left')
        
        # Search frame
        search_frame = ttk.Frame(header, style='Main.TFrame')
        search_frame.pack(side='right')
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame,
                               textvariable=self.search_var,
                               width=40,
                               style='Search.TEntry',
                               font=('Segoe UI', 10))
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.insert(0, "Search vehicles, customers...")
        
        # Search button
        search_btn = ttk.Button(search_frame,
                              text="🔍 Search",
                              style='Action.TButton',
                              command=self.perform_search)
        search_btn.pack(side='left')
        
        # Quick actions
        actions_frame = ttk.Frame(header, style='Main.TFrame')
        actions_frame.pack(side='right', padx=20)
        
        ttk.Button(actions_frame,
                  text="🔄 Refresh",
                  style='Nav.TButton',
                  command=self.refresh_all).pack(side='left', padx=5)
        
        ttk.Button(actions_frame,
                  text="➕ Add Vehicle",
                  style='Action.TButton',
                  command=self.add_vehicle).pack(side='left', padx=5)
        
    def show_dashboard(self):
        """Show dashboard with charts and stats"""
        self.clear_content()
        
        # Dashboard title
        title_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame,
                 text="📊 DASHBOARD OVERVIEW",
                 style='Title.TLabel').pack(side='left')
        
        ttk.Label(title_frame,
                 text="Real-time business insights",
                 foreground=self.colors['text_secondary'],
                 background=self.colors['primary'],
                 font=('Segoe UI', 11)).pack(side='left', padx=10)
        
        # Stats cards row
        stats_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        stats_frame.pack(fill='x', pady=(0, 30))
        
        stats_data = [
            {"title": "Total Inventory", "value": "48", "change": "+12%", "icon": "🚗", "color": self.colors['chart1']},
            {"title": "Available Vehicles", "value": "32", "change": "+8%", "icon": "✅", "color": self.colors['success']},
            {"title": "Monthly Sales", "value": "₹85.2M", "change": "+23%", "icon": "💰", "color": self.colors['chart2']},
            {"title": "New Customers", "value": "128", "change": "+15%", "icon": "👥", "color": self.colors['chart3']},
            {"title": "Pending Orders", "value": "7", "change": "-2%", "icon": "⏳", "color": self.colors['warning']}
        ]
        
        for i, stat in enumerate(stats_data):
            card = self.create_stat_card(stats_frame, stat)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Charts row
        charts_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        charts_frame.pack(fill='both', expand=True)
        
        # Left chart - Sales by category
        left_chart_frame = ttk.Frame(charts_frame, style='Card.TFrame')
        left_chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(left_chart_frame,
                 text="Sales by Vehicle Type",
                 style='CardTitle.TLabel').pack(pady=15)
        
        self.create_pie_chart(left_chart_frame)
        
        # Right chart - Monthly revenue
        right_chart_frame = ttk.Frame(charts_frame, style='Card.TFrame')
        right_chart_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        ttk.Label(right_chart_frame,
                 text="Monthly Revenue Trend",
                 style='CardTitle.TLabel').pack(pady=15)
        
        self.create_bar_chart(right_chart_frame)
        
        # Recent activity
        activity_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        activity_frame.pack(fill='x', pady=(30, 0))
        
        ttk.Label(activity_frame,
                 text="📋 RECENT ACTIVITY",
                 style='CardTitle.TLabel').pack(anchor='w', pady=(0, 10))
        
        self.create_activity_table(activity_frame)
        
    def create_stat_card(self, parent, stat):
        """Create a beautiful statistics card"""
        card = ttk.Frame(parent, style='Card.TFrame')
        
        # Icon and title
        icon_frame = ttk.Frame(card, style='Card.TFrame')
        icon_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        ttk.Label(icon_frame,
                 text=stat['icon'],
                 font=('Segoe UI', 20),
                 background=self.colors['card_bg']).pack(side='left')
        
        ttk.Label(icon_frame,
                 text=stat['title'],
                 foreground=self.colors['text_secondary'],
                 background=self.colors['card_bg'],
                 font=('Segoe UI', 10)).pack(side='right')
        
        # Value
        ttk.Label(card,
                 text=stat['value'],
                 foreground=stat['color'],
                 background=self.colors['card_bg'],
                 font=('Segoe UI', 28, 'bold')).pack(pady=(5, 10))
        
        # Change indicator
        change_frame = ttk.Frame(card, style='Card.TFrame')
        change_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        change_color = self.colors['success'] if '+' in stat['change'] else self.colors['danger']
        ttk.Label(change_frame,
                 text=stat['change'],
                 foreground=change_color,
                 background=self.colors['card_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(side='left')
        
        ttk.Label(change_frame,
                 text="from last month",
                 foreground=self.colors['text_secondary'],
                 background=self.colors['card_bg'],
                 font=('Segoe UI', 8)).pack(side='right')
        
        return card
        
    def create_pie_chart(self, parent):
        """Create pie chart for sales by category"""
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor(self.colors['card_bg'])
        ax.set_facecolor(self.colors['card_bg'])
        
        # Sample data
        categories = ['Sedan', 'SUV', 'Hatchback', 'Luxury', 'Electric']
        sales = [35, 28, 20, 12, 5]
        colors = [self.colors['chart1'], self.colors['chart2'], 
                 self.colors['chart3'], self.colors['chart4'], self.colors['chart5']]
        
        wedges, texts, autotexts = ax.pie(sales, labels=categories, colors=colors,
                                         autopct='%1.1f%%', startangle=90)
        
        # Style the text
        for text in texts:
            text.set_color(self.colors['text'])
            text.set_fontsize(9)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_weight('bold')
        
        ax.set_title('Sales Distribution', color=self.colors['text'], fontsize=12)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_bar_chart(self, parent):
        """Create bar chart for monthly revenue"""
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor(self.colors['card_bg'])
        ax.set_facecolor(self.colors['card_bg'])
        
        # Sample data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [45, 52, 48, 61, 55, 85]  # In millions
        
        bars = ax.bar(months, revenue, color=self.colors['chart1'])
        
        # Style the bars
        for bar in bars:
            bar.set_edgecolor(self.colors['card_border'])
        
        # Style the axes
        ax.set_ylabel('Revenue (Millions ₹)', color=self.colors['text'], fontsize=10)
        ax.set_xlabel('Month', color=self.colors['text'], fontsize=10)
        ax.tick_params(axis='x', colors=self.colors['text'])
        ax.tick_params(axis='y', colors=self.colors['text'])
        
        # Grid
        ax.grid(True, alpha=0.3, color=self.colors['text_secondary'])
        
        # Title
        ax.set_title('Monthly Revenue Trend', color=self.colors['text'], fontsize=12)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_activity_table(self, parent):
        """Create recent activity table"""
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(parent, style='Card.TFrame')
        tree_frame.pack(fill='both', expand=True)
        
        # Define columns
        columns = ('Time', 'Activity', 'User', 'Status')
        
        # Create treeview
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=5)
        
        # Define headings
        tree.heading('Time', text='Time')
        tree.heading('Activity', text='Activity')
        tree.heading('User', text='User')
        tree.heading('Status', text='Status')
        
        # Define column widths
        tree.column('Time', width=120)
        tree.column('Activity', width=300)
        tree.column('User', width=150)
        tree.column('Status', width=100)
        
        # Style the treeview
        style = ttk.Style()
        style.configure('Treeview', 
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['card_bg'],
                       rowheight=30,
                       font=('Segoe UI', 9))
        
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Sample data
        activities = [
            ('10:30 AM', 'New vehicle added: Toyota Corolla 2024', 'Admin', '✅ Completed'),
            ('09:45 AM', 'Sale processed: Honda Civic to Ali Khan', 'Sales Rep', '💰 ₹6.5M'),
            ('09:15 AM', 'Test drive scheduled: BMW 5 Series', 'Customer Service', '📅 Scheduled'),
            ('Yesterday', 'Monthly report generated', 'System', '📊 Generated'),
            ('Dec 14', 'Price updated: Suzuki Alto increased by 5%', 'Manager', '📈 Updated')
        ]
        
        # Insert data
        for activity in activities:
            tree.insert('', 'end', values=activity)
            
    def show_inventory(self):
        """Show inventory management tab"""
        self.clear_content()
        
        title_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame,
                 text="🚗 VEHICLE INVENTORY",
                 style='Title.TLabel').pack(side='left')
        
        # Inventory controls
        controls_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Filters
        filter_frame = ttk.Frame(controls_frame, style='Main.TFrame')
        filter_frame.pack(side='left')
        
        ttk.Label(filter_frame,
                 text="Filter by:",
                 foreground=self.colors['text'],
                 background=self.colors['primary']).pack(side='left', padx=5)
        
        # Category filter
        categories = ['All', 'Sedan', 'SUV', 'Hatchback', 'Luxury', 'Electric']
        self.category_var = tk.StringVar(value='All')
        category_combo = ttk.Combobox(filter_frame,
                                    textvariable=self.category_var,
                                    values=categories,
                                    width=15,
                                    state='readonly')
        category_combo.pack(side='left', padx=5)
        
        # Status filter
        statuses = ['All', 'Available', 'Sold', 'Reserved']
        self.status_var = tk.StringVar(value='Available')
        status_combo = ttk.Combobox(filter_frame,
                                  textvariable=self.status_var,
                                  values=statuses,
                                  width=15,
                                  state='readonly')
        status_combo.pack(side='left', padx=5)
        
        # Apply filters button
        ttk.Button(filter_frame,
                  text="Apply Filters",
                  style='Action.TButton',
                  command=self.apply_inventory_filters).pack(side='left', padx=10)
        
        # Action buttons
        action_frame = ttk.Frame(controls_frame, style='Main.TFrame')
        action_frame.pack(side='right')
        
        ttk.Button(action_frame,
                  text="➕ Add New Vehicle",
                  style='Action.TButton',
                  command=self.add_vehicle).pack(side='left', padx=5)
        
        ttk.Button(action_frame,
                  text="📊 Export to Excel",
                  style='Nav.TButton').pack(side='left', padx=5)
        
        # Inventory table
        self.create_inventory_table()
        
    def create_inventory_table(self):
        """Create inventory table with sample data"""
        table_frame = ttk.Frame(self.main_content, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Define columns
        columns = ('ID', 'Manufacturer', 'Model', 'Year', 'Color', 'Price', 'Status', 'Location')
        
        # Create treeview
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Sample inventory data
        inventory = [
            (101, 'Toyota', 'Corolla', 2024, 'White', '₹4.5M', 'Available', 'Lahore'),
            (102, 'Honda', 'Civic', 2024, 'Black', '₹6.5M', 'Available', 'Lahore'),
            (103, 'Suzuki', 'Alto', 2024, 'Silver', '₹2.2M', 'Available', 'Lahore'),
            (104, 'MG', 'ZS EV', 2024, 'Red', '₹8.5M', 'Available', 'Lahore'),
            (105, 'BMW', '5 Series', 2024, 'White', '₹25M', 'Available', 'Karachi'),
            (106, 'Mercedes', 'S-Class', 2024, 'Black', '₹45M', 'Available', 'Karachi'),
            (107, 'Tesla', 'Model 3', 2024, 'Silver', '₹22M', 'Test Drive', 'Islamabad'),
            (108, 'Toyota', 'Fortuner', 2023, 'Black', '₹12.5M', 'Sold', 'Lahore'),
            (109, 'Honda', 'City', 2024, 'Blue', '₹4.2M', 'Available', 'Lahore'),
            (110, 'Suzuki', 'Swift', 2024, 'Red', '₹3.5M', 'Reserved', 'Lahore')
        ]
        
        # Insert data
        for item in inventory:
            tree.insert('', 'end', values=item)
            
        # Bind double-click event
        tree.bind('<Double-Button-1>', self.view_vehicle_details)
        
    def show_sales(self):
        """Show sales management tab"""
        self.clear_content()
        ttk.Label(self.main_content,
                 text="💰 SALES MANAGEMENT - Coming Soon",
                 style='Title.TLabel').pack(pady=50)
        
    def show_customers(self):
        """Show customer management tab"""
        self.clear_content()
        ttk.Label(self.main_content,
                 text="👥 CUSTOMER MANAGEMENT - Coming Soon",
                 style='Title.TLabel').pack(pady=50)
        
    def show_reports(self):
        """Show reports tab"""
        self.clear_content()
        ttk.Label(self.main_content,
                 text="📈 REPORTS & ANALYTICS - Coming Soon",
                 style='Title.TLabel').pack(pady=50)
        
    def show_settings(self):
        """Show settings tab"""
        self.clear_content()
        ttk.Label(self.main_content,
                 text="⚙️ SYSTEM SETTINGS - Coming Soon",
                 style='Title.TLabel').pack(pady=50)
        
    def clear_content(self):
        """Clear the main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def perform_search(self):
        """Perform search operation"""
        search_term = self.search_var.get()
        if search_term and search_term != "Search vehicles, customers...":
            messagebox.showinfo("Search", f"Searching for: {search_term}")
            # In real app, implement search logic here
            
    def refresh_all(self):
        """Refresh all data"""
        messagebox.showinfo("Refresh", "Refreshing data...")
        # In real app, refresh data from database
        
    def add_vehicle(self):
        """Add new vehicle dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Vehicle")
        dialog.geometry("400x500")
        dialog.configure(bg=self.colors['primary'])
        
        ttk.Label(dialog,
                 text="➕ ADD NEW VEHICLE",
                 style='Title.TLabel').pack(pady=20)
        
        # Form fields
        fields = [
            ("Manufacturer:", "Toyota"),
            ("Model:", "Corolla"),
            ("Year:", "2024"),
            ("Color:", "White"),
            ("Price (₹):", "4500000"),
            ("VIN:", "JTNK4MEB8L1012345"),
            ("Dealership:", "Toyota Lahore Central")
        ]
        
        entries = []
        for label, default in fields:
            frame = ttk.Frame(dialog)
            frame.pack(fill='x', padx=40, pady=5)
            
            ttk.Label(frame,
                     text=label,
                     foreground=self.colors['text'],
                     background=self.colors['primary']).pack(side='left')
            
            entry = ttk.Entry(frame)
            entry.insert(0, default)
            entry.pack(side='right', fill='x', expand=True)
            entries.append(entry)
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame,
                  text="Cancel",
                  style='Nav.TButton',
                  command=dialog.destroy).pack(side='left', padx=10)
        
        ttk.Button(btn_frame,
                  text="Save Vehicle",
                  style='Action.TButton',
                  command=lambda: self.save_vehicle(entries, dialog)).pack(side='left', padx=10)
        
    def save_vehicle(self, entries, dialog):
        """Save vehicle data"""
        data = [entry.get() for entry in entries]
        messagebox.showinfo("Success", f"Vehicle saved:\n{', '.join(data)}")
        dialog.destroy()
        
    def apply_inventory_filters(self):
        """Apply inventory filters"""
        category = self.category_var.get()
        status = self.status_var.get()
        messagebox.showinfo("Filters", f"Applied: Category={category}, Status={status}")
        
    def view_vehicle_details(self, event):
        """View vehicle details on double-click"""
        messagebox.showinfo("Vehicle Details", "Viewing vehicle details...")
        
    def load_sample_data(self):
        """Load sample data for demo mode"""
        # In real app, load from database
        pass
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def bind_events(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<F5>', lambda e: self.refresh_all())
        self.root.bind('<Control-n>', lambda e: self.add_vehicle())
        self.root.bind('<Control-f>', lambda e: self.search_var.focus())
        
# For direct testing
if __name__ == "__main__":
    root = tk.Tk()
    app = VelocityNexusApp(root)
    root.mainloop()