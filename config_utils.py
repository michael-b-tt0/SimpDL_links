import json
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip

def create_section_header(parent, text):
    """Create a styled section header"""
    header_frame = tb.Frame(parent, bootstyle="dark")
    
    label = tb.Label(
        header_frame,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bootstyle="inverse-dark"
    )
    label.pack(side="left", pady=10)
    
    return header_frame

def create_input_row(parent, label_text, value, tooltip_text=""):
    """Create a styled input row with label, entry, and optional tooltip"""
    row = tb.Frame(parent, bootstyle="secondary")
    row.pack(fill="x", pady=8, padx=5)
    
    # Label with tooltip icon if tooltip provided
    label_frame = tb.Frame(row, bootstyle="secondary")
    label_frame.pack(side="left", fill="y", padx=(10, 5))
    
    lbl = tb.Label(
        label_frame,
        text=label_text,
        width=20,
        anchor="w",
        font=("Segoe UI", 10)
    )
    lbl.pack(side="left")
    
    if tooltip_text:
        info_label = tb.Label(
            label_frame,
            text="ℹ️",
            cursor="hand2",
            font=("Segoe UI", 9)
        )
        info_label.pack(side="left", padx=2)
        ToolTip(info_label, text=tooltip_text, bootstyle="info")
    
    # Entry field with styling
    entry = tb.Entry(
        row,
        font=("Segoe UI", 10),
        bootstyle="secondary"
    )
    entry.insert(0, str(value))
    entry.pack(side="left", fill="x", expand=True, padx=(5, 10), ipady=5)
    
    return entry

def build_config_frame(parent, config_path):
    """
    Creates an enhanced Frame for modifying the config with better UX
    """
    frame = tb.Frame(parent, bootstyle="dark")

    # Header section
    header_container = tb.Frame(frame, bootstyle="dark")
    header_container.pack(fill="x", pady=(0, 20))

    title_label = tb.Label(
        header_container,
        text="⚙️ Configuration Settings",
        font=("Segoe UI", 20, "bold")
    )
    title_label.pack(anchor="w")

    subtitle_label = tb.Label(
        header_container,
        text="Configure your credentials and output preferences",
        font=("Segoe UI", 11),
        foreground="#B3B3B3"
    )
    subtitle_label.pack(anchor="w", pady=(5, 0))

    # Load configuration
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "username": "",
            "password": "",
            "output_directory": "./output"
        }

    # Scrollable container for config fields
    container = ScrolledFrame(frame, autohide=True, bootstyle="secondary")
    container.pack(fill="both", expand=True, padx=0, pady=(0, 15))

    # Card-like container for settings
    settings_card = tb.Frame(container, bootstyle="secondary", relief="raised")
    settings_card.pack(fill="both", expand=True, padx=10, pady=10)
    settings_card.configure(borderwidth=2)

    # Tooltips for each field
    tooltips = {
        "username": "Your SimpCity account username",
        "password": "Your SimpCity account password (stored locally)",
        "output_directory": "Directory where JSON files will be saved"
    }

    entries = {}
    
    # Create input fields for each config item
    for key, val in config.items():
        tooltip = tooltips.get(key, f"Configuration value for {key}")
        entry = create_input_row(settings_card, f"{key.replace('_', ' ').title()}:", val, tooltip)
        entries[key] = entry

    # Status message area
    status_frame = tb.Frame(frame, bootstyle="dark")
    status_frame.pack(fill="x", pady=(10, 0))

    status_label = tb.Label(
        status_frame,
        text="",
        font=("Segoe UI", 10),
        bootstyle="inverse-dark"
    )
    status_label.pack()

    def validate_config():
        """Validate configuration fields"""
        username = entries.get("username", None)
        password = entries.get("password", None)
        
        if username and not username.get().strip():
            return False, "Username cannot be empty"
        if password and not password.get().strip():
            return False, "Password cannot be empty"
        
        return True, "Configuration is valid"

    def save_config():
        """Save configuration with validation"""
        is_valid, message = validate_config()
        
        if not is_valid:
            status_label.config(text=f"❌ {message}", foreground="#E22134")
            return
        
        try:
            for key, entry in entries.items():
                config[key] = entry.get()
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)
            
            status_label.config(text="✅ Configuration saved successfully!", foreground="#1DB954")
            
            # Clear status after 3 seconds
            frame.after(3000, lambda: status_label.config(text=""))
        
        except Exception as e:
            status_label.config(text=f"❌ Error saving: {str(e)}", foreground="#E22134")

    # Button container
    button_container = tb.Frame(frame, bootstyle="dark")
    button_container.pack(fill="x", pady=10)

    save_button = tb.Button(
        button_container,
        text="💾 Save Configuration",
        bootstyle="success",
        command=save_config,
        width=20
    )
    save_button.pack(pady=5, ipady=8)

    return frame


def build_urls_frame(parent, urls_file):
    """
    Creates an enhanced Frame for managing URLs with better visual design
    """
    frame = tb.Frame(parent, bootstyle="dark")

    # Header section
    header_container = tb.Frame(frame, bootstyle="dark")
    header_container.pack(fill="x", pady=(0, 20))

    title_label = tb.Label(
        header_container,
        text="📋 URL Management",
        font=("Segoe UI", 20, "bold")
    )
    title_label.pack(anchor="w")

    subtitle_label = tb.Label(
        header_container,
        text="Add, remove, and organize your scraping URLs",
        font=("Segoe UI", 11),
        foreground="#B3B3B3"
    )
    subtitle_label.pack(anchor="w", pady=(5, 0))

    # URL count display
    count_frame = tb.Frame(frame, bootstyle="dark")
    count_frame.pack(fill="x", pady=(0, 10))

    count_label = tb.Label(
        count_frame,
        text="Total URLs: 0",
        font=("Segoe UI", 10, "bold"),
        foreground="#1DB954"
    )
    count_label.pack(side="left")

    # Add URL section (moved to top)
    add_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    add_card.pack(fill="x", pady=(0, 15), padx=5)
    add_card.configure(borderwidth=2)

    add_content = tb.Frame(add_card, bootstyle="secondary")
    add_content.pack(fill="x", padx=15, pady=15)

    add_title = tb.Label(
        add_content,
        text="Add New URL",
        font=("Segoe UI", 11, "bold")
    )
    add_title.pack(anchor="w", pady=(0, 8))

    add_row = tb.Frame(add_content, bootstyle="secondary")
    add_row.pack(fill="x")

    new_url_entry = tb.Entry(add_row, font=("Segoe UI", 10))
    new_url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)
    new_url_entry.insert(0, "https://")

    add_button = tb.Button(
        add_row,
        text="➕ Add",
        bootstyle="success",
        width=12
    )
    add_button.pack(side="right", ipady=4)

    # Scrollable container for URL list
    list_label = tb.Label(
        frame,
        text="Current URLs",
        font=("Segoe UI", 11, "bold")
    )
    list_label.pack(anchor="w", pady=(10, 5))

    container = ScrolledFrame(frame, autohide=True, bootstyle="secondary", height=300)
    container.pack(fill="both", expand=True, padx=5, pady=(0, 10))

    row_frames = []

    def get_urls_from_file():
        """Read the current URLs from disk, stripping empty lines."""
        try:
            with open(urls_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def update_count():
        """Update the URL count display"""
        urls = get_urls_from_file()
        count_label.config(text=f"Total URLs: {len(urls)}")

    def refresh_list():
        """Refresh the URL list display"""
        # Clear existing rows
        for rf in row_frames:
            rf.destroy()
        row_frames.clear()

        loaded_urls = get_urls_from_file()

        # Create URL rows
        for i, url in enumerate(loaded_urls):
            # Alternating row colors for better readability
            bg_style = "secondary" if i % 2 == 0 else "dark"
            
            row = tb.Frame(container, bootstyle=bg_style, relief="flat")
            row.pack(fill="x", pady=2, padx=5)
            row_frames.append(row)

            # URL index
            index_label = tb.Label(
                row,
                text=f"{i+1}.",
                width=4,
                anchor="w",
                font=("Segoe UI", 9)
            )
            index_label.pack(side="left", padx=(10, 5))

            # URL text (truncated if too long)
            display_url = url if len(url) <= 80 else url[:77] + "..."
            url_label = tb.Label(
                row,
                text=display_url,
                anchor="w",
                font=("Consolas", 9)
            )
            url_label.pack(side="left", padx=5, fill="x", expand=True)
            
            # Add tooltip with full URL if truncated
            if len(url) > 80:
                ToolTip(url_label, text=url, bootstyle="info")

            # Delete button
            delete_btn = tb.Button(
                row,
                text="🗑️",
                bootstyle="danger",
                width=4,
                command=lambda idx=i: remove_url(idx)
            )
            delete_btn.pack(side="right", padx=10, pady=5)

        update_count()

        # Show empty state if no URLs
        if not loaded_urls:
            empty_label = tb.Label(
                container,
                text="No URLs added yet. Add your first URL above!",
                font=("Segoe UI", 11),
                foreground="#888888"
            )
            empty_label.pack(pady=40)
            row_frames.append(empty_label)

    def remove_url(index):
        """Remove URL at specified index"""
        loaded_urls = get_urls_from_file()
        if 0 <= index < len(loaded_urls):
            loaded_urls.pop(index)
            with open(urls_file, "w") as f:
                for u in loaded_urls:
                    f.write(u + "\n")
        refresh_list()

    def add_url():
        """Add new URL to the list"""
        new_url = new_url_entry.get().strip()
        if new_url and new_url != "https://":
            # Simple URL validation
            if not new_url.startswith(("http://", "https://")):
                new_url = "https://" + new_url
            
            loaded_urls = get_urls_from_file()
            
            # Check for duplicates
            if new_url in loaded_urls:
                new_url_entry.delete(0, "end")
                new_url_entry.insert(0, "⚠️ URL already exists!")
                frame.after(2000, lambda: new_url_entry.delete(0, "end") or new_url_entry.insert(0, "https://"))
                return
            
            loaded_urls.append(new_url)
            with open(urls_file, "w") as f:
                for u in loaded_urls:
                    f.write(u + "\n")
            new_url_entry.delete(0, "end")
            new_url_entry.insert(0, "https://")
        refresh_list()

    # Bind Enter key to add URL
    new_url_entry.bind("<Return>", lambda event: add_url())
    
    # Connect add button
    add_button.config(command=add_url)

    # Action buttons at bottom
    action_frame = tb.Frame(frame, bootstyle="dark")
    action_frame.pack(fill="x", pady=10)

    clear_all_btn = tb.Button(
        action_frame,
        text="🗑️ Clear All URLs",
        bootstyle="danger",
        command=lambda: clear_all_urls()
    )
    clear_all_btn.pack(side="left", padx=5)

    def clear_all_urls():
        """Clear all URLs with confirmation"""
        if get_urls_from_file():
            # Simple confirmation by requiring button press twice
            if clear_all_btn.cget("text") == "🗑️ Clear All URLs":
                clear_all_btn.config(text="⚠️ Click Again to Confirm")
                frame.after(3000, lambda: clear_all_btn.config(text="🗑️ Clear All URLs"))
            else:
                with open(urls_file, "w") as f:
                    f.write("")
                refresh_list()
                clear_all_btn.config(text="🗑️ Clear All URLs")

    # Initial list load
    refresh_list()

    # Store refresh function for external access
    frame.refresh_list = refresh_list

    return frame