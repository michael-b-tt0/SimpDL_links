# styles.py - Centralized styling constants for the application

# Color Palette
COLORS = {
    "primary": "#1DB954",        # Spotify green
    "primary_dark": "#148A3C",
    "primary_light": "#1ED760",
    "secondary": "#191414",      # Dark background
    "surface": "#282828",        # Card/container background
    "surface_light": "#3E3E3E",
    "background": "#121212",     # Main background
    "text_primary": "#FFFFFF",
    "text_secondary": "#B3B3B3",
    "success": "#1DB954",
    "warning": "#FFA500",
    "danger": "#E22134",
    "info": "#3B82F6",
    "border": "#404040",
    "hover": "#333333",
}

# Typography
FONTS = {
    "heading_large": ("Segoe UI", 24, "bold"),
    "heading_medium": ("Segoe UI", 18, "bold"),
    "heading_small": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 11),
    "body_large": ("Segoe UI", 12),
    "caption": ("Segoe UI", 10),
    "monospace": ("Consolas", 10),
    "button": ("Segoe UI", 10, "bold"),
}

# Spacing
SPACING = {
    "xs": 5,
    "sm": 10,
    "md": 15,
    "lg": 20,
    "xl": 30,
    "xxl": 40,
}

# Border Radius - Updated for rounded corners
RADIUS = {
    "small": 6,
    "medium": 10,
    "large": 15,
    "xlarge": 20,
}

# Component Sizes
SIZES = {
    "sidebar_width": 220,
    "button_height": 40,
    "input_height": 35,
    "icon_size": 20,
    "window_min_width": 1000,
    "window_min_height": 650,
}

# Shadows (for future ttk styling)
SHADOWS = {
    "small": "0 2px 4px rgba(0,0,0,0.2)",
    "medium": "0 4px 8px rgba(0,0,0,0.3)",
    "large": "0 8px 16px rgba(0,0,0,0.4)",
}

# Button Styles
BUTTON_STYLES = {
    "primary": {
        "bg": COLORS["primary"],
        "fg": COLORS["text_primary"],
        "hover_bg": COLORS["primary_light"],
    },
    "secondary": {
        "bg": COLORS["surface"],
        "fg": COLORS["text_primary"],
        "hover_bg": COLORS["surface_light"],
    },
    "danger": {
        "bg": COLORS["danger"],
        "fg": COLORS["text_primary"],
        "hover_bg": "#C41E2D",
    },
}

# Animation durations (in milliseconds)
ANIMATION = {
    "fast": 150,
    "normal": 300,
    "slow": 500,
}

# TTKBootstrap style configurations for rounded elements
ROUNDED_BUTTON_STYLE = "rounded"  # Will be applied to buttons
ROUNDED_FRAME_STYLE = "rounded"   # Will be applied to frames/cards