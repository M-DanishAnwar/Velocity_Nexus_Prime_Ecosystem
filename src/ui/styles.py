"""
UI Styles and Themes for Velocity Nexus Prime
"""
import tkinter as tk
from tkinter import ttk
import colorsys

class VelocityStyles:
    """Modern UI styles for the application"""
    
    # Color palettes
    DARK_THEME = {
        'primary': '#1a1a2e',
        'secondary': '#16213e',
        'accent': '#0f3460',
        'success': '#4ecdc4',
        'warning': '#ff9a76',
        'danger': '#ff6b6b',
        'info': '#45aaf2',
        'text': '#e6e6e6',
        'text_secondary': '#a0a0a0',
        'card_bg': '#222831',
        'card_border': '#393e46',
        'hover': '#30475e',
        'input_bg': '#2d4059',
        'input_fg': '#ffffff',
        'input_border': '#405870',
        
        # Chart colors
        'chart1': '#00adb5',
        'chart2': '#ff9a76',
        'chart3': '#6a2c70',
        'chart4': '#08d9d6',
        'chart5': '#ff2e63',
        'chart6': '#f8b400',
        'chart7': '#95e1d3',
        'chart8': '#fce38a',
        
        # Status colors
        'available': '#00d26a',
        'sold': '#ff4757',
        'reserved': '#ffa502',
        'pending': '#3498db'
    }
    
    LIGHT_THEME = {
        'primary': '#ffffff',
        'secondary': '#f8f9fa',
        'accent': '#007bff',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'text': '#212529',
        'text_secondary': '#6c757d',
        'card_bg': '#ffffff',
        'card_border': '#dee2e6',
        'hover': '#e9ecef',
        'input_bg': '#ffffff',
        'input_fg': '#212529',
        'input_border': '#ced4da',
        
        # Chart colors
        'chart1': '#007bff',
        'chart2': '#28a745',
        'chart3': '#ffc107',
        'chart4': '#dc3545',
        'chart5': '#17a2b8',
        'chart6': '#6610f2',
        'chart7': '#fd7e14',
        'chart8': '#20c997',
        
        # Status colors
        'available': '#28a745',
        'sold': '#dc3545',
        'reserved': '#ffc107',
        'pending': '#17a2b8'
    }
    
    def __init__(self, root, theme='dark'):
        self.root = root
        self.theme = theme
        self.colors = self.DARK_THEME if theme == 'dark' else self.LIGHT_THEME
        self.setup_styles()
    
    def setup_styles(self):
        """Configure all ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure root background
        self.root.configure(bg=self.colors['primary'])
        
        # Configure main frames
        style.configure('Main.TFrame', background=self.colors['primary'])
        style.configure('Sidebar.TFrame', background=self.colors['secondary'])
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       borderwidth=1,
                       relief='solid')
        style.configure('Transparent.TFrame', background=self.colors['primary'])
        
        # Configure labels
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
        
        style.configure('Value.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['success'],
                       font=('Segoe UI', 28, 'bold'))
        
        style.configure('Label.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 10))
        
        style.configure('Success.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['success'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Error.TLabel',
                       background=self.colors['primary'],
                       foreground=self.colors['danger'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure buttons
        style.configure('Nav.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       padding=10)
        
        style.map('Nav.TButton',
                 background=[('active', self.colors['hover']),
                           ('disabled', self.colors['card_border'])])
        
        style.configure('Action.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        
        style.map('Action.TButton',
                 background=[('active', self._darken_color(self.colors['success'], 0.2)),
                           ('disabled', self.colors['card_border'])])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        
        style.map('Danger.TButton',
                 background=[('active', self._darken_color(self.colors['danger'], 0.2))])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        
        style.configure('Icon.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       padding=5)
        
        # Configure entries
        style.configure('Search.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       foreground=self.colors['input_fg'],
                       borderwidth=1,
                       relief='solid',
                       padding=5)
        
        style.map('Search.TEntry',
                 fieldbackground=[('focus', self.colors['input_bg']),
                                ('disabled', self.colors['card_border'])],
                 foreground=[('disabled', self.colors['text_secondary'])])
        
        style.configure('Form.TEntry',
                       fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='solid',
                       padding=5)
        
        # Configure combobox
        style.configure('TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       foreground=self.colors['input_fg'],
                       background=self.colors['input_bg'],
                       borderwidth=1,
                       relief='solid',
                       padding=5)
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.colors['input_bg']),
                                ('disabled', self.colors['card_border'])],
                 foreground=[('disabled', self.colors['text_secondary'])])
        
        # Configure notebook (tabs)
        style.configure('TNotebook',
                       background=self.colors['primary'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=self.colors['secondary'],
                       foreground=self.colors['text'],
                       padding=[20, 10],
                       font=('Segoe UI', 10))
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', 'white')])
        
        # Configure progressbar
        style.configure('TProgressbar',
                       background=self.colors['success'],
                       troughcolor=self.colors['card_border'],
                       borderwidth=0)
        
        # Configure treeview
        style.configure('Treeview',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['card_bg'],
                       rowheight=30,
                       font=('Segoe UI', 9))
        
        style.map('Treeview',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', 'white')])
        
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       padding=5)
        
        style.map('Treeview.Heading',
                 background=[('active', self.colors['hover'])])
        
        # Configure scrollbar
        style.configure('TScrollbar',
                       background=self.colors['secondary'],
                       troughcolor=self.colors['primary'],
                       borderwidth=0,
                       arrowsize=12)
        
        style.map('TScrollbar',
                 background=[('active', self.colors['accent'])])
        
        # Configure separator
        style.configure('TSeparator',
                       background=self.colors['card_border'])
        
        # Configure checkbutton
        style.configure('TCheckbutton',
                       background=self.colors['primary'],
                       foreground=self.colors['text'])
        
        # Configure radiobutton
        style.configure('TRadiobutton',
                       background=self.colors['primary'],
                       foreground=self.colors['text'])
        
        # Configure scale
        style.configure('TScale',
                       background=self.colors['primary'])
    
    def _darken_color(self, hex_color, factor=0.2):
        """Darken a hex color by a factor"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        # Darken
        l = max(0, l * (1 - factor))
        
        # Convert back to RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        # Convert back to hex
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    def _lighten_color(self, hex_color, factor=0.2):
        """Lighten a hex color by a factor"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        # Lighten
        l = min(1, l * (1 + factor))
        
        # Convert back to RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        # Convert back to hex
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    def get_color(self, color_name):
        """Get color by name"""
        return self.colors.get(color_name, '#000000')
    
    def get_chart_colors(self, n=5):
        """Get chart color palette"""
        chart_keys = ['chart1', 'chart2', 'chart3', 'chart4', 'chart5', 
                     'chart6', 'chart7', 'chart8']
        return [self.colors[key] for key in chart_keys[:n]]
    
    def get_status_color(self, status):
        """Get color for status"""
        status_colors = {
            'Available': self.colors['available'],
            'Sold': self.colors['sold'],
            'Reserved': self.colors['reserved'],
            'Pending': self.colors['pending'],
            'Completed': self.colors['success'],
            'Cancelled': self.colors['danger']
        }
        return status_colors.get(status, self.colors['text_secondary'])
    
    def create_gradient(self, color1, color2, steps=10):
        """Create gradient between two colors"""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to hex
        def rgb_to_hex(rgb):
            return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        
        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)
        
        gradient = []
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / (steps - 1))
            g = int(g1 + (g2 - g1) * i / (steps - 1))
            b = int(b1 + (b2 - b1) * i / (steps - 1))
            gradient.append(rgb_to_hex((r, g, b)))
        
        return gradient
    
    def create_shadow_effect(self, widget, color=None, offset=2):
        """Create shadow effect for widget"""
        if color is None:
            color = self._darken_color(self.colors['card_border'], 0.3)
        
        # This is a simplified shadow effect
        widget.config(highlightbackground=color, 
                     highlightcolor=color,
                     highlightthickness=1)
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=10, **kwargs):
        """Create rounded rectangle on canvas"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        
        return canvas.create_polygon(points, smooth=True, **kwargs)


# Theme switcher class
class ThemeManager:
    """Manage application themes"""
    
    THEMES = {
        'dark': VelocityStyles.DARK_THEME,
        'light': VelocityStyles.LIGHT_THEME,
        'blue': {
            'primary': '#0d1b2a',
            'secondary': '#1b263b',
            'accent': '#415a77',
            'success': '#4cc9f0',
            'warning': '#f8961e',
            'danger': '#f94144',
            'info': '#90e0ef',
            'text': '#e0e1dd',
            'text_secondary': '#778da9'
        },
        'green': {
            'primary': '#081c15',
            'secondary': '#1b4332',
            'accent': '#2d6a4f',
            'success': '#40916c',
            'warning': '#f48c06',
            'danger': '#d00000',
            'info': '#38b000',
            'text': '#d8f3dc',
            'text_secondary': '#95d5b2'
        }
    }
    
    def __init__(self, root):
        self.root = root
        self.current_theme = 'dark'
        self.styles = VelocityStyles(root, self.current_theme)
    
    def switch_theme(self, theme_name):
        """Switch to a different theme"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.styles = VelocityStyles(self.root, theme_name)
            self.styles.setup_styles()
            return True
        return False
    
    def get_available_themes(self):
        """Get list of available themes"""
        return list(self.THEMES.keys())
    
    def get_theme_colors(self, theme_name=None):
        """Get colors for a theme"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.THEMES.get(theme_name, self.THEMES['dark'])


# Custom widget styles
class ModernButton(ttk.Button):
    """Modern styled button"""
    
    def __init__(self, parent, text="", style="Nav.TButton", **kwargs):
        super().__init__(parent, text=text, style=style, **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        self.config(cursor="")


class IconButton(ttk.Button):
    """Button with icon"""
    
    def __init__(self, parent, icon="", text="", **kwargs):
        if icon:
            text = f"{icon} {text}"
        super().__init__(parent, text=text, style="Icon.TButton", **kwargs)


class Card(ttk.Frame):
    """Modern card widget"""
    
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        
        if title:
            title_label = ttk.Label(self, text=title, style="CardTitle.TLabel")
            title_label.pack(anchor='w', padx=15, pady=(15, 5))
        
        self.content = ttk.Frame(self, style="Card.TFrame")
        self.content.pack(fill='both', expand=True, padx=15, pady=5)


class StatCard(ttk.Frame):
    """Statistics card widget"""
    
    def __init__(self, parent, title="", value="", change="", icon="", color=None):
        super().__init__(parent, style="Card.TFrame")
        
        self.colors = VelocityStyles.DARK_THEME
        
        # Icon and title row
        top_frame = ttk.Frame(self, style="Card.TFrame")
        top_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        if icon:
            icon_label = ttk.Label(top_frame, text=icon, 
                                  font=('Segoe UI', 16),
                                  background=self.colors['card_bg'])
            icon_label.pack(side='left')
        
        title_label = ttk.Label(top_frame, text=title,
                               foreground=self.colors['text_secondary'],
                               background=self.colors['card_bg'],
                               font=('Segoe UI', 10))
        title_label.pack(side='right')
        
        # Value
        value_color = color if color else self.colors['success']
        value_label = ttk.Label(self, text=value,
                               foreground=value_color,
                               background=self.colors['card_bg'],
                               font=('Segoe UI', 28, 'bold'))
        value_label.pack(pady=(5, 10))
        
        # Change indicator
        if change:
            change_frame = ttk.Frame(self, style="Card.TFrame")
            change_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            change_color = self.colors['success'] if '+' in str(change) else self.colors['danger']
            change_label = ttk.Label(change_frame, text=str(change),
                                    foreground=change_color,
                                    background=self.colors['card_bg'],
                                    font=('Segoe UI', 10, 'bold'))
            change_label.pack(side='left')
            
            ttk.Label(change_frame, text="from last month",
                     foreground=self.colors['text_secondary'],
                     background=self.colors['card_bg'],
                     font=('Segoe UI', 8)).pack(side='right')