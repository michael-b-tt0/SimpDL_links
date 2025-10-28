import os
import webbrowser
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
import sys

from config_utils import build_config_frame, build_urls_frame
from content_generator import build_content_frame
from link_utils import build_generate_links_frame
from login_utils import login_to_simpcity
from report_generator import build_report_frame

# Import styles if available, otherwise use defaults
try:
    from styles import COLORS, FONTS, SPACING, SIZES
except ImportError:
    COLORS = {"primary": "#1DB954"}
    FONTS = {"heading_large": ("Segoe UI", 24, "bold")}
    SPACING = {"md": 15, "lg": 20}
    SIZES = {"sidebar_width": 220}

def create_styled_button(parent, text, command, icon=None, style="success"):
    """Create a consistently styled sidebar button with optional icon"""
    btn_frame = tb.Frame(parent, bootstyle="dark")
    
    btn = tb.Button(
        btn_frame, 
        text=f"  {text}" if icon else text,
        bootstyle=style,
        command=command,
        width=18
    )
    btn.pack(fill="x", ipady=8)
    
    return btn_frame

def create_separator(parent):
    """Create a visual separator line"""
    sep = tb.Separator(parent, orient="horizontal", bootstyle="secondary")
    return sep

def main_gui():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config", "config.json")
    urls_file = os.path.join(script_dir, "config", "urls.txt")

    # Create main window with modern theme
    app = tb.Window(themename="darkly")
    app.title("SimpDL - Content Manager")
    
    # Set minimum window size
    app.minsize(1000, 650)

    def center_window(window, width=1100, height=700):
        """Center window on screen with enhanced dimensions"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")

    center_window(app, 1100, 700)

   

    # ===== HEADER BAR =====
    header_frame = tb.Frame(app, bootstyle="primary")
    header_frame.pack(side="top", fill="x")

    # Logo and title in header
    header_content = tb.Frame(header_frame, bootstyle="primary")
    header_content.pack(side="left", padx=25, pady=18)

    app_title = tb.Label(
        header_content,
        text="🎯 SimpDL",
        font=("Segoe UI", 24, "bold"),
        bootstyle="inverse-primary"
    )
    app_title.pack(side="left")

    version_label = tb.Label(
        header_content,
        text="v1.0",
        font=("Segoe UI", 12),
        bootstyle="inverse-secondary"
    )
    version_label.pack(side="left", padx=20)

    # ===== MAIN CONTAINER =====
    main_container = tb.Frame(app, bootstyle="dark")
    main_container.pack(fill="both", expand=True)

    # ===== SIDEBAR =====
    sidebar_frame = tb.Frame(main_container, bootstyle="secondary", width=240)
    sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
    sidebar_frame.pack_propagate(False)

    # Sidebar content with padding
    sidebar_content = tb.Frame(sidebar_frame, bootstyle="secondary")
    sidebar_content.pack(fill="both", expand=True, padx=15, pady=20)

    # Navigation label
    nav_label = tb.Label(
        sidebar_content,
        text="NAVIGATION",
        font=("Segoe UI", 9, "bold"),
        bootstyle="secondary",
        foreground="#888888"
    )
    nav_label.pack(anchor="w", pady=(0, 10))

    # ===== CONTENT AREA =====
    content_container = tb.Frame(main_container, bootstyle="dark")
    content_container.pack(side="left", fill="both", expand=True)

    # Add padding around content
    content_frame = tb.Frame(content_container, bootstyle="dark")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    pages = {}
    current_page = ["home"]

    def show_page(page_name):
        """Show selected page"""
        for page in pages.values():
            page.pack_forget()
        pages[page_name].pack(fill="both", expand=True)
        current_page[0] = page_name

    # ===== HOME PAGE (Enhanced) =====
    home_page = tb.Frame(content_frame, bootstyle="dark")
    
    # Welcome section
    welcome_container = tb.Frame(home_page, bootstyle="dark")
    welcome_container.pack(pady=40)

    home_title = tb.Label(
        welcome_container,
        text="Welcome to SimpDL",
        font=("Segoe UI", 32, "bold"),
        bootstyle="inverse-dark"
    )
    home_title.pack()

    subtitle = tb.Label(
        welcome_container,
        text="Content Manager & Report Generator",
        font=("Segoe UI", 14),
        foreground="#1DB954"
    )
    subtitle.pack(pady=(5, 0))

    # Info card
    info_card = tb.Frame(home_page, bootstyle="secondary", relief="raised")
    info_card.pack(pady=30, padx=100, fill="x")
    info_card.configure(borderwidth=2)

    card_content = tb.Frame(info_card, bootstyle="secondary")
    card_content.pack(padx=30, pady=30)

    info_text = tb.Label(
        card_content,
        text="This application helps you manage and generate content from SimpCity.\n\n"
             "Get started by configuring your settings in the sidebar,\n"
             "then generate links and scrape content.",
        font=("Segoe UI", 12),
        bootstyle="inverse-secondary",
        justify="center"
    )
    info_text.pack(pady=10)

    

    

    

    # Quick start guide
    guide_frame = tb.Frame(home_page, bootstyle="dark")
    guide_frame.pack(pady=20)

    guide_title = tb.Label(
        guide_frame,
        text="Quick Start Guide",
        font=("Segoe UI", 14, "bold"),
        bootstyle="inverse-dark"
    )
    guide_title.pack(pady=10)

    steps = [
        "1. Configure your credentials in 'Modify Config'",
        "2. Add URLs manually or use 'Generate Links'",
        "3. Run 'Generate Content JSON' to scrape data",
        "4. Create an HTML report from your JSON file"
    ]

    for step in steps:
        step_label = tb.Label(
            guide_frame,
            text=step,
            font=("Segoe UI", 11),
            bootstyle="inverse-dark"
        )
        step_label.pack(anchor="w", padx=50, pady=3)

    pages["home"] = home_page

    # ===== CREATE OTHER PAGES =====
    config_page = build_config_frame(content_frame, config_path)
    pages["config"] = config_page

    urls_page = build_urls_frame(content_frame, urls_file)
    pages["urls"] = urls_page

    def refresh_urls_list():
        urls_page.refresh_list()

    generate_page = build_generate_links_frame(content_frame, urls_file, refresh_urls_list)
    pages["generate"] = generate_page

    content_page = build_content_frame(content_frame, config_path, urls_file)
    pages["content"] = content_page

    report_page = build_report_frame(content_frame)
    pages["report"] = report_page

    # ===== SIDEBAR NAVIGATION BUTTONS =====
    nav_buttons = [
        ("🏠 Home", "home", "info"),
        ("⚙️ Modify Config", "config", "primary"),
        ("📋 Manage URLs", "urls", "primary"),
        ("🔗 Generate Links", "generate", "primary"),
    ]

    for text, page, btn_style in nav_buttons:
        btn = create_styled_button(
            sidebar_content, 
            text, 
            lambda p=page: show_page(p),
            style=btn_style
        )
        btn.pack(fill="x", pady=3)

    # Separator
    sep1 = create_separator(sidebar_content)
    sep1.pack(fill="x", pady=15)

    # Actions section
    actions_label = tb.Label(
        sidebar_content,
        text="ACTIONS",
        font=("Segoe UI", 9, "bold"),
        bootstyle="secondary",
        foreground="#888888"
    )
    actions_label.pack(anchor="w", pady=(0, 10))

    action_buttons = [
        ("🚀 Generate Content", "content", "success"),
        ("📄 Generate Report", "report", "success"),
    ]

    for text, page, btn_style in action_buttons:
        btn = create_styled_button(
            sidebar_content,
            text,
            lambda p=page: show_page(p),
            style=btn_style
        )
        btn.pack(fill="x", pady=3)

    # Spacer
    spacer = tb.Frame(sidebar_content, bootstyle="secondary")
    spacer.pack(fill="both", expand=True)

    # Exit button at bottom
    sep2 = create_separator(sidebar_content)
    sep2.pack(fill="x", pady=10)

    exit_btn = create_styled_button(
        sidebar_content,
        "❌ Exit",
        app.quit,
        style="danger"
    )
    exit_btn.pack(fill="x", pady=5)

    # Show home page initially
    show_page("home")
    
    # Start the application
    app.mainloop()

if __name__ == "__main__":
    main_gui()
