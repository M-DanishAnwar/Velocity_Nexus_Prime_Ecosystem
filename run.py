"""
Velocity Nexus Prime - Robust Entry Point
"""
import sys
import os
import logging
import tkinter as tk
from tkinter import messagebox

# Configure Logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('VelocityNexus')

def check_imports():
    """Verify critical dependencies are installed"""
    missing = []
    try:
        import numpy
        import pandas
        import matplotlib
        import PIL
        import dotenv
        import pyodbc
    except ImportError as e:
        logger.error(f"Dependency Error: {e}")
        return False, str(e)
    return True, ""

def main():
    logger.info("🚀 Starting Application...")
    
    # 1. Load Environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not found. Environment variables may not load.")

    # 2. Check Dependencies
    valid, error_msg = check_imports()
    if not valid:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Setup Error", 
            f"Missing dependencies.\nPlease run FIX_PROJECT.bat\n\nError: {error_msg}")
        return

    # 3. Launch App
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.ui.main_window import VelocityNexusApp
        
        root = tk.Tk()
        app = VelocityNexusApp(root)
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Crash: {e}", exc_info=True)
        # Fallback UI for crash
        root = tk.Tk()
        root.title("Crash Report")
        tk.Label(root, text=f"Application Crashed:\n{e}", padx=20, pady=20, fg="red").pack()
        root.mainloop()

if __name__ == "__main__":
    main()