"""
Custom Widgets for Velocity Nexus Prime
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from datetime import datetime
from src.ui.styles import VelocityStyles

class SearchBox(ttk.Frame):
    """Modern search box with icon"""
    
    def __init__(self, parent, placeholder="Search...", on_search=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_search = on_search
        self.styles = VelocityStyles(parent)
        
        # Search icon
        self.icon_label = ttk.Label(self, text="🔍", 
                                   font=('Segoe UI', 12),
                                   background=self.styles.colors['secondary'])
        self.icon_label.pack(side='left', padx=(10, 5))
        
        # Search entry
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var,
                              style='Search.TEntry',
                              font=('Segoe UI', 10))
        self.entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        
        # Placeholder
        self.placeholder = placeholder
        self.entry.insert(0, placeholder)
        self.entry.config(foreground=self.styles.colors['text_secondary'])
        
        # Bind events
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', self._on_search)
        self.var.trace('w', self._on_text_change)
        
        # Clear button
        self.clear_btn = ttk.Button(self, text="✕", 
                                   style='Icon.TButton',
                                   command=self.clear,
                                   width=3)
        self.clear_btn.pack(side='right', padx=(0, 5))
        self.clear_btn.pack_forget()  # Hidden initially
    
    def _on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground=self.styles.colors['text'])
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(foreground=self.styles.colors['text_secondary'])
            self.clear_btn.pack_forget()
    
    def _on_text_change(self, *args):
        text = self.var.get()
        if text and text != self.placeholder:
            self.clear_btn.pack(side='right', padx=(0, 5))
        else:
            self.clear_btn.pack_forget()
    
    def _on_search(self, event):
        if self.on_search:
            self.on_search(self.get_value())
    
    def get_value(self):
        """Get search value"""
        value = self.var.get()
        return value if value != self.placeholder else ""
    
    def clear(self):
        """Clear search box"""
        self.var.set("")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(foreground=self.styles.colors['text_secondary'])
        self.clear_btn.pack_forget()


class DatePicker(ttk.Frame):
    """Simple date picker widget"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.styles = VelocityStyles(parent)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
        # Day
        self.day_var = tk.StringVar(value=datetime.now().strftime('%d'))
        day_combo = ttk.Combobox(self, textvariable=self.day_var,
                                values=[f"{i:02d}" for i in range(1, 32)],
                                width=3, state='readonly')
        day_combo.pack(side='left', padx=2)
        
        ttk.Label(self, text="/", 
                 background=self.styles.colors['primary']).pack(side='left')
        
        # Month
        self.month_var = tk.StringVar(value=datetime.now().strftime('%m'))
        month_combo = ttk.Combobox(self, textvariable=self.month_var,
                                  values=[f"{i:02d}" for i in range(1, 13)],
                                  width=3, state='readonly')
        month_combo.pack(side='left', padx=2)
        
        ttk.Label(self, text="/", 
                 background=self.styles.colors['primary']).pack(side='left')
        
        # Year
        self.year_var = tk.StringVar(value=datetime.now().strftime('%Y'))
        current_year = datetime.now().year
        year_combo = ttk.Combobox(self, textvariable=self.year_var,
                                 values=[str(i) for i in range(current_year-10, current_year+11)],
                                 width=5, state='readonly')
        year_combo.pack(side='left', padx=2)
        
        # Bind changes
        self.day_var.trace('w', self._update_date)
        self.month_var.trace('w', self._update_date)
        self.year_var.trace('w', self._update_date)
    
    def _update_date(self, *args):
        """Update date string when components change"""
        try:
            date_str = f"{self.year_var.get()}-{self.month_var.get()}-{self.day_var.get()}"
            datetime.strptime(date_str, '%Y-%m-%d')  # Validate
            self.date_var.set(date_str)
        except ValueError:
            pass
    
    def get_date(self):
        """Get selected date"""
        return self.date_var.get()
    
    def set_date(self, date_str):
        """Set date from string"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            self.day_var.set(date.strftime('%d'))
            self.month_var.set(date.strftime('%m'))
            self.year_var.set(date.strftime('%Y'))
            self.date_var.set(date_str)
        except ValueError:
            pass


class StatusIndicator(ttk.Frame):
    """Status indicator with colored circle"""
    
    def __init__(self, parent, status="Available", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.styles = VelocityStyles(parent)
        self.status = status
        
        # Colored circle
        self.canvas = tk.Canvas(self, width=12, height=12, 
                               highlightthickness=0, bg=self.styles.colors['primary'])
        self.canvas.pack(side='left', padx=(0, 5))
        
        # Status label
        self.label = ttk.Label(self, text=status,
                              foreground=self.styles.get_status_color(status),
                              background=self.styles.colors['primary'],
                              font=('Segoe UI', 9))
        self.label.pack(side='left')
        
        self._draw_circle()
    
    def _draw_circle(self):
        """Draw colored circle"""
        color = self.styles.get_status_color(self.status)
        self.canvas.create_oval(2, 2, 10, 10, fill=color, outline=color)
    
    def set_status(self, status):
        """Update status"""
        self.status = status
        self.label.config(text=status, 
                         foreground=self.styles.get_status_color(status))
        self._draw_circle()


class ProgressCard(ttk.Frame):
    """Progress card with label and progress bar"""
    
    def __init__(self, parent, title="", value=0, max_value=100, unit="%", **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        
        self.styles = VelocityStyles(parent)
        
        # Title and value
        top_frame = ttk.Frame(self, style="Card.TFrame")
        top_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        ttk.Label(top_frame, text=title,
                 foreground=self.styles.colors['text_secondary'],
                 background=self.styles.colors['card_bg'],
                 font=('Segoe UI', 10)).pack(side='left')
        
        self.value_label = ttk.Label(top_frame, 
                                    text=f"{value}{unit}",
                                    foreground=self.styles.colors['text'],
                                    background=self.styles.colors['card_bg'],
                                    font=('Segoe UI', 10, 'bold'))
        self.value_label.pack(side='right')
        
        # Progress bar
        self.progress = ttk.Progressbar(self, maximum=max_value,
                                       value=value, mode='determinate')
        self.progress.pack(fill='x', padx=15, pady=(0, 15))
        
        self.value = value
        self.max_value = max_value
        self.unit = unit
    
    def set_value(self, value):
        """Update progress value"""
        self.value = min(value, self.max_value)
        self.progress['value'] = self.value
        self.value_label.config(text=f"{self.value}{self.unit}")


class ImageViewer(ttk.Frame):
    """Image viewer widget"""
    
    def __init__(self, parent, image_path=None, width=200, height=150, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.width = width
        self.height = height
        self.image = None
        self.photo = None
        
        # Canvas for image
        self.canvas = tk.Canvas(self, width=width, height=height,
                               highlightthickness=0, bg='#2d4059')
        self.canvas.pack()
        
        # Placeholder text
        self.canvas.create_text(width//2, height//2,
                               text="No Image",
                               fill='#778da9',
                               font=('Segoe UI', 10))
        
        if image_path:
            self.load_image(image_path)
    
    def load_image(self, image_path):
        """Load and display image"""
        try:
            # Load image
            image = Image.open(image_path)
            image.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
            
            # Convert for tkinter
            self.photo = ImageTk.PhotoImage(image)
            
            # Display on canvas
            self.canvas.delete("all")
            self.canvas.create_image(self.width//2, self.height//2,
                                    image=self.photo)
            
            self.image = image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.canvas.delete("all")
            self.canvas.create_text(self.width//2, self.height//2,
                                   text="Image Error",
                                   fill='#ff6b6b',
                                   font=('Segoe UI', 10))


class DataTable(ttk.Frame):
    """Enhanced data table with sorting and filtering"""
    
    def __init__(self, parent, columns, data=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.columns = columns
        self.data = data or []
        self.styles = VelocityStyles(parent)
        self.sort_column = None
        self.sort_reverse = False
        
        # Create frame for table and scrollbar
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True)
        
        # Create treeview
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, 
                            command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical',
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data
        self.load_data(data)
        
        # Double-click event
        self.tree.bind('<Double-Button-1>', self.on_double_click)
    
    def load_data(self, data):
        """Load data into table"""
        self.data = data or []
        self.tree.delete(*self.tree.get_children())
        
        for row in self.data:
            self.tree.insert('', 'end', values=row)
    
    def sort_by_column(self, column):
        """Sort table by column"""
        # Get column index
        col_index = self.columns.index(column)
        
        # Sort data
        self.data.sort(key=lambda x: x[col_index], 
                      reverse=self.sort_reverse)
        
        # Reload table
        self.load_data(self.data)
        
        # Update sort indicator
        self.update_sort_indicator(column)
        
        # Toggle sort direction
        self.sort_reverse = not self.sort_reverse
    
    def update_sort_indicator(self, column):
        """Update sort indicator in header"""
        for col in self.columns:
            current_text = self.tree.heading(col, 'text')
            if col == column:
                indicator = " ↓" if self.sort_reverse else " ↑"
                if not current_text.endswith(indicator):
                    self.tree.heading(col, text=f"{current_text.rstrip(' ↑↓')}{indicator}")
            else:
                # Remove indicator from other columns
                self.tree.heading(col, text=current_text.rstrip(' ↑↓'))
    
    def on_double_click(self, event):
        """Handle double-click event"""
        item = self.tree.selection()
        if item:
            values = self.tree.item(item, 'values')
            print(f"Selected: {values}")
    
    def get_selected(self):
        """Get selected row"""
        item = self.tree.selection()
        if item:
            return self.tree.item(item, 'values')
        return None
    
    def clear_selection(self):
        """Clear selection"""
        self.tree.selection_remove(self.tree.selection())


class NotificationBadge(ttk.Label):
    """Notification badge with count"""
    
    def __init__(self, parent, count=0, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.styles = VelocityStyles(parent)
        self.count = count
        
        self.config(
            text=str(count) if count > 0 else "",
            foreground='white',
            background=self.styles.colors['danger'],
            font=('Segoe UI', 8, 'bold'),
            padding=(3, 1) if count < 10 else (2, 1)
        )
        
        if count <= 0:
            self.config(text="")
    
    def set_count(self, count):
        """Update badge count"""
        self.count = count
        if count > 0:
            self.config(text=str(count),
                       padding=(3, 1) if count < 10 else (2, 1))
        else:
            self.config(text="")


class ToolTip:
    """Tooltip for widgets"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.show)
        self.widget.bind('<Leave>', self.hide)
    
    def show(self, event=None):
        """Show tooltip"""
        if self.tooltip or not self.text:
            return
        
        # Get widget position
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create label
        label = ttk.Label(self.tooltip, text=self.text,
                         background="#ffffe0",
                         relief='solid', borderwidth=1,
                         padding=(5, 2))
        label.pack()
    
    def hide(self, event=None):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None