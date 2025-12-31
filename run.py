import sys
import os
import tkinter as tk

# 1. Add 'src' to the System Path so Python finds our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from src.ui.main_window import VelocityNexusApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        # Set Icon if exists
        # root.iconbitmap('icon.ico') 
        app = VelocityNexusApp(root)
        root.mainloop()
    except ImportError as e:
        print("❌ CRITICAL ERROR: Python cannot find the 'src' directory.")
        print(f"Details: {e}")
        input("Press Enter to Exit...")
    except Exception as e:
        print(f"❌ Application Error: {e}")
        input("Press Enter to Exit...")