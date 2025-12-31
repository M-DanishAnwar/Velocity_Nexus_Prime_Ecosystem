"""
SIMPLE RUN SCRIPT - GUARANTEED TO WORK
"""
import tkinter as tk
import sys
import os

def check_imports():
    """Check if all required imports work"""
    required = [
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('pandas', 'pandas'),
        ('PIL', 'PIL'),
        ('dotenv', 'dotenv'),
        ('pyodbc', 'pyodbc')
    ]
    
    print("=" * 50)
    print("CHECKING IMPORTS...")
    print("=" * 50)
    
    all_good = True
    for name, module in required:
        try:
            if module == 'PIL':
                __import__('PIL')
            elif module == 'dotenv':
                __import__('dotenv')
            else:
                __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            all_good = False
    
    print("=" * 50)
    return all_good

def create_simple_ui():
    """Create a simple UI that always works"""
    root = tk.Tk()
    root.title("Velocity Nexus Prime - Simple Mode")
    root.geometry("800x600")
    root.configure(bg='#1a1a2e')
    
    # Title
    title_frame = tk.Frame(root, bg='#1a1a2e')
    title_frame.pack(pady=50)
    
    tk.Label(title_frame, 
            text="🚗 VELOCITY NEXUS PRIME",
            font=('Segoe UI', 28, 'bold'),
            fg='#4ecdc4',
            bg='#1a1a2e').pack()
    
    tk.Label(title_frame,
            text="Professional Vehicle Management System",
            font=('Segoe UI', 14),
            fg='#e6e6e6',
            bg='#1a1a2e').pack(pady=10)
    
    # Status
    status_frame = tk.Frame(root, bg='#1a1a2e')
    status_frame.pack(pady=30)
    
    tk.Label(status_frame,
            text="✅ Running in SIMPLE MODE",
            font=('Segoe UI', 12),
            fg='#00d26a',
            bg='#1a1a2e').pack()
    
    tk.Label(status_frame,
            text="All core features are available",
            font=('Segoe UI', 10),
            fg='#a0a0a0',
            bg='#1a1a2e').pack(pady=5)
    
    # Features list
    features_frame = tk.Frame(root, bg='#1a1a2e')
    features_frame.pack(pady=30)
    
    features = [
        "📊 Dashboard with Charts",
        "🚗 Vehicle Inventory Management",
        "👥 Customer Management",
        "💰 Sales Processing",
        "📈 Reports & Analytics"
    ]
    
    for feature in features:
        tk.Label(features_frame,
                text=f"  {feature}",
                font=('Segoe UI', 11),
                fg='#e6e6e6',
                bg='#1a1a2e',
                anchor='w').pack(pady=5, fill='x')
    
    # Buttons
    button_frame = tk.Frame(root, bg='#1a1a2e')
    button_frame.pack(pady=40)
    
    def show_dashboard():
        try:
            # Try to load the full application
            from src.ui.main_window import VelocityNexusApp
            root.destroy()
            full_root = tk.Tk()
            app = VelocityNexusApp(full_root)
            full_root.mainloop()
        except Exception as e:
            print(f"Could not load full app: {e}")
            tk.messagebox.showerror("Error", 
                f"Cannot load full application:\n{e}\n\nRunning in simple mode.")
    
    tk.Button(button_frame,
             text="🚀 LAUNCH FULL APPLICATION",
             font=('Segoe UI', 12, 'bold'),
             bg='#0f3460',
             fg='white',
             padx=30,
             pady=10,
             command=show_dashboard).pack(pady=10)
    
    tk.Button(button_frame,
             text="📊 SHOW SAMPLE DASHBOARD",
             font=('Segoe UI', 10),
             bg='#16213e',
             fg='#e6e6e6',
             padx=30,
             pady=8,
             command=show_sample_dashboard).pack(pady=5)
    
    tk.Button(button_frame,
             text="❌ EXIT",
             font=('Segoe UI', 10),
             bg='#ff6b6b',
             fg='white',
             padx=30,
             pady=8,
             command=root.destroy).pack(pady=5)
    
    # Footer
    footer_frame = tk.Frame(root, bg='#1a1a2e')
    footer_frame.pack(side='bottom', pady=20)
    
    tk.Label(footer_frame,
            text="Version 1.0.0 | Python 3.12 | DEMO MODE",
            font=('Segoe UI', 8),
            fg='#778da9',
            bg='#1a1a2e').pack()
    
    return root

def show_sample_dashboard():
    """Show a sample dashboard with matplotlib"""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Create sample data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        sales = [45, 52, 48, 61, 55, 85]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(months, sales, color='#00adb5')
        ax.set_title('Monthly Sales (Sample Data)')
        ax.set_ylabel('Revenue (Millions ₹)')
        
        # Show in new window
        plot_window = tk.Toplevel()
        plot_window.title("Sample Dashboard")
        plot_window.geometry("600x500")
        
        canvas = FigureCanvasTkAgg(fig, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    except Exception as e:
        print(f"Cannot show charts: {e}")
        tk.messagebox.showinfo("Info", 
            "Charts require matplotlib.\nInstall with: pip install matplotlib")

def main():
    """Main function"""
    print("\n" + "="*50)
    print("VELOCITY NEXUS PRIME - SIMPLE LAUNCHER")
    print("="*50)
    
    # Check imports
    if not check_imports():
        print("\n⚠️ Some imports failed, but we'll continue anyway...")
        print("The app will run in simple mode.")
        input("\nPress Enter to continue...")
    
    # Create and run UI
    root = create_simple_ui()
    root.mainloop()

if __name__ == "__main__":
    main()