import tkinter as tk
from tkinter import ttk, messagebox
from src.services.vehicle_service import VehicleService # Ensure you have this file from previous step
# If you don't have service, change import to: from src.repositories.vehicle_repo import VehicleRepository

class VelocityNexusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Velocity Nexus Prime Ecosystem - Enterprise Edition")
        self.root.geometry("1280x800")
        self.root.state('zoomed')
        
        # Initialize Logic
        # NOTE: If you haven't made the Service layer yet, strictly use Repo directly for now to make it work
        from src.repositories.vehicle_repo import VehicleRepository
        self.repo = VehicleRepository()

        # COLOR PALETTE (Cyberpunk/Dark Theme)
        self.colors = {
            'bg_dark': '#121212',
            'bg_panel': '#1E1E1E',
            'text_light': '#E0E0E0',
            'accent_blue': '#00ADB5',
            'accent_green': '#00C853',
            'accent_red': '#D32F2F',
            'border': '#333333'
        }
        
        self.configure_styles()
        self.build_ui()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Global Styles
        style.configure('App.TFrame', background=self.colors['bg_dark'])
        style.configure('Panel.TFrame', background=self.colors['bg_panel'], relief='flat')
        
        # Label Styles
        style.configure('Header.TLabel', background=self.colors['bg_dark'], foreground=self.colors['accent_blue'], font=('Segoe UI', 24, 'bold'))
        style.configure('SubHeader.TLabel', background=self.colors['bg_panel'], foreground=self.colors['text_light'], font=('Segoe UI', 14))
        style.configure('Body.TLabel', background=self.colors['bg_panel'], foreground='#AAAAAA', font=('Segoe UI', 10))
        
        # Button Styles
        style.configure('Action.TButton', background=self.colors['accent_blue'], foreground='white', font=('Segoe UI', 10, 'bold'), padding=10)
        style.map('Action.TButton', background=[('active', '#007A80')])
        
        # Treeview (The Table)
        style.configure('Treeview', 
                        background=self.colors['bg_panel'], 
                        foreground=self.colors['text_light'], 
                        fieldbackground=self.colors['bg_panel'],
                        font=('Consolas', 10),
                        rowheight=35)
        style.configure('Treeview.Heading', background='#252526', foreground=self.colors['accent_blue'], font=('Segoe UI', 11, 'bold'))

    def build_ui(self):
        # 1. Sidebar (Navigation)
        sidebar = ttk.Frame(self.root, style='Panel.TFrame', width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        ttk.Label(sidebar, text="VELOCITY\nNEXUS", style='Header.TLabel', font=('Segoe UI', 18, 'bold')).pack(pady=30)
        
        nav_buttons = ["📊 Dashboard", "🚗 Inventory", "👥 Customers", "📝 Sales History", "⚙️ Settings"]
        for btn in nav_buttons:
            b = tk.Button(sidebar, text=btn, bg=self.colors['bg_panel'], fg='white', bd=0, font=('Segoe UI', 12), anchor='w', padx=20)
            b.pack(fill='x', pady=5)

        # 2. Main Content Area
        main_area = ttk.Frame(self.root, style='App.TFrame')
        main_area.pack(side='right', fill='both', expand=True)

        # Header
        header = ttk.Frame(main_area, style='App.TFrame')
        header.pack(fill='x', padx=30, pady=30)
        ttk.Label(header, text="Inventory Management", style='Header.TLabel').pack(side='left')
        ttk.Button(header, text="Refresh Data", style='Action.TButton', command=self.load_inventory).pack(side='right')

        # 3. Data Table (Treeview)
        table_frame = ttk.Frame(main_area, style='Panel.TFrame')
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        cols = ('ID', 'Make', 'Model', 'Color', 'Price (PKR)', 'Dealership', 'City', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        
        # Configure Columns
        for col in cols:
            self.tree.heading(col, text=col)
            width = 100 if col == 'ID' else 150
            self.tree.column(col, width=width, anchor='center')

        # Scrollbar
        sb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        # 4. Action Bar
        action_bar = ttk.Frame(main_area, style='App.TFrame')
        action_bar.pack(fill='x', padx=30, pady=20)
        ttk.Button(action_bar, text="Sell Selected Vehicle", style='Action.TButton', command=self.sell_action).pack(side='right')

        # Initial Load
        self.load_inventory()

    def load_inventory(self):
        # Clear Table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            data = self.repo.get_detailed_inventory()
            for row in data:
                # row structure comes from SQL query in repo
                v_id, make, model, color, price, dealer, city, status, import_stat = row
                
                # Format Price
                price_fmt = f"{price:,.0f}"
                if import_stat == 'Imported':
                    model = f"{model} (IMP)"

                self.tree.insert('', 'end', values=(v_id, make, model, color, price_fmt, dealer, city, status))
        except Exception as e:
            messagebox.showerror("Database Error", f"Is SQL Server Running?\n\nDetails: {e}")

    def sell_action(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a car to sell.")
            return
        
        # Get data
        item = self.tree.item(selected[0])
        val = item['values']
        v_id = val[0]
        price_raw = float(val[4].replace(',', ''))
        
        # Simple Input Dialog (In real app, make a custom window)
        top = tk.Toplevel(self.root)
        top.title("Sale Processing")
        top.geometry("300x200")
        
        tk.Label(top, text="Customer CNIC:").pack()
        e_cnic = tk.Entry(top)
        e_cnic.pack()
        
        tk.Label(top, text="Name:").pack()
        e_name = tk.Entry(top)
        e_name.pack()
        
        def confirm():
            # Tax Logic (Tax is 17% standard)
            tax = price_raw * 0.17
            success = self.repo.execute_sale(v_id, e_cnic.get(), e_name.get(), 1, price_raw, tax)
            if success:
                messagebox.showinfo("Success", "Car Sold!")
                top.destroy()
                self.load_inventory()
            else:
                messagebox.showerror("Failed", "Sale failed. Check logs.")

        tk.Button(top, text="Confirm Sale", command=confirm).pack(pady=10)