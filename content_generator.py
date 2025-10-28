# Standard library imports
import os
import json
import threading
import tkinter as tk
import time
import datetime

# Third-party imports
import ttkbootstrap as tb
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Local imports
from login_utils import login_to_simpcity
from scraper_utils import scrape_page

def build_content_frame(parent, config_path, urls_file):
    """
    Returns an enhanced Frame for content generation with better UX and visual feedback
    """
    frame = tb.Frame(parent, bootstyle="dark")

    # Header section
    header_container = tb.Frame(frame, bootstyle="dark")
    header_container.pack(fill="x", pady=(0, 20))

    title = tb.Label(
        header_container,
        text="🚀 Content Generator",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(anchor="w")

    subtitle = tb.Label(
        header_container,
        text="Scrape content from configured URLs and generate JSON output",
        font=("Segoe UI", 11),
        foreground="#B3B3B3"
    )
    subtitle.pack(anchor="w", pady=(5, 0))

    # Stats card
    stats_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    stats_card.pack(fill="x", pady=(0, 15), padx=5)
    stats_card.configure(borderwidth=2)

    stats_content = tb.Frame(stats_card, bootstyle="secondary")
    stats_content.pack(fill="x", padx=20, pady=15)

    stats_title = tb.Label(
        stats_content,
        text="📊 Session Statistics",
        font=("Segoe UI", 11, "bold")
    )
    stats_title.pack(anchor="w", pady=(0, 10))

    # Stats row
    stats_row = tb.Frame(stats_content, bootstyle="secondary")
    stats_row.pack(fill="x")

    # Individual stat items
    def create_stat_item(parent, label, value="0"):
        container = tb.Frame(parent, bootstyle="secondary")
        container.pack(side="left", padx=15)
        
        val_label = tb.Label(
            container,
            text=value,
            font=("Segoe UI", 16, "bold"),
            foreground="#1DB954"
        )
        val_label.pack()
        
        desc_label = tb.Label(
            container,
            text=label,
            font=("Segoe UI", 9),
            foreground="#888888"
        )
        desc_label.pack()
        
        return val_label

    urls_stat = create_stat_item(stats_row, "URLs to Process")
    posts_stat = create_stat_item(stats_row, "Posts Found", "0")
    pages_stat = create_stat_item(stats_row, "Pages Processed", "0/0")

    # Progress section
    progress_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    progress_card.pack(fill="x", pady=(0, 15), padx=5)
    progress_card.configure(borderwidth=2)

    progress_content = tb.Frame(progress_card, bootstyle="secondary")
    progress_content.pack(fill="x", padx=20, pady=15)

    progress_title = tb.Label(
        progress_content,
        text="⏳ Progress",
        font=("Segoe UI", 11, "bold")
    )
    progress_title.pack(anchor="w", pady=(0, 10))

    progress_label = tb.Label(
        progress_content,
        text="Ready to start",
        font=("Segoe UI", 10),
        foreground="#B3B3B3"
    )
    progress_label.pack(anchor="w", pady=(0, 8))

    progress_bar = tb.Progressbar(
        progress_content,
        orient="horizontal",
        mode="determinate",
        bootstyle="success-striped"
    )
    progress_bar.pack(fill="x", ipady=5)

    # Log section
    log_frame = tb.Frame(frame, bootstyle="dark")
    log_frame.pack(fill="both", expand=True, pady=(15, 0))

    log_title = tb.Label(
        log_frame,
        text="📝 Activity Log",
        font=("Segoe UI", 11, "bold")
    )
    log_title.pack(anchor="w", pady=(0, 5))

    # Scrollable log text area
    log_container = tb.Frame(log_frame, bootstyle="secondary", relief="raised")
    log_container.pack(fill="both", expand=True)
    log_container.configure(borderwidth=2)

    log_text = tk.Text(
        log_container,
        height=12,
        bg="#1E1E1E",
        fg="#D4D4D4",
        wrap="word",
        font=("Consolas", 9),
        relief="flat",
        padx=15,
        pady=10
    )
    log_text.pack(side="left", fill="both", expand=True)

    scrollbar = tb.Scrollbar(log_container, command=log_text.yview)
    scrollbar.pack(side="right", fill="y")
    log_text.config(yscrollcommand=scrollbar.set)

    # Generation state
    generation_in_progress = [False]
    stats = {"urls": 0, "posts": 0, "current_page": 0, "total_pages": 0}

    def log_message(msg, level="INFO"):
        """Add timestamped message to log with color coding"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on level
        colors = {
            "INFO": "#B3B3B3",
            "SUCCESS": "#1DB954",
            "WARNING": "#FFA500",
            "ERROR": "#E22134"
        }
        
        log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        log_text.insert(tk.END, f"{msg}\n", level.lower())
        log_text.tag_config("timestamp", foreground="#888888")
        log_text.tag_config("info", foreground=colors["INFO"])
        log_text.tag_config("success", foreground=colors["SUCCESS"])
        log_text.tag_config("warning", foreground=colors["WARNING"])
        log_text.tag_config("error", foreground=colors["ERROR"])
        log_text.see(tk.END)

    def update_stats():
        """Update statistics display"""
        urls_stat.config(text=str(stats["urls"]))
        posts_stat.config(text=str(stats["posts"]))
        pages_stat.config(text=f"{stats['current_page']}/{stats['total_pages']}")

    def start_generation():
        """Triggered by the button. Spawns a background thread for the main generation."""
        if generation_in_progress[0]:
            return

        # Read URLs to get count
        try:
            with open(urls_file, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
            
            if not urls:
                log_message("No URLs found. Please add URLs first.", "ERROR")
                return
            
            stats["urls"] = len(urls)
            stats["total_pages"] = len(urls)
            update_stats()
            
        except Exception as e:
            log_message(f"Error reading URLs: {str(e)}", "ERROR")
            return

        generation_in_progress[0] = True
        start_button.config(state="disabled", text="⏳ Generating...")
        cancel_button.config(state="normal")
        log_text.delete(1.0, tk.END)
        log_message("Starting content generation...", "INFO")
        threading.Thread(target=run_generation, daemon=True).start()

    def cancel_generation():
        """Cancel the ongoing generation"""
        generation_in_progress[0] = False
        log_message("Cancellation requested...", "WARNING")

    def run_generation():
        """
        The main scraping logic, running in a background thread
        """
        all_posts_data = []
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            username = config.get("username", "")
            password = config.get("password", "")
            output_directory = config.get("output_directory", "")

            with open(urls_file, "r") as file:
                urls = [line.strip() for line in file if line.strip()]

            folder_name = get_folder_name(urls[0])
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
                log_message(f"Created output directory: {output_directory}", "INFO")

            log_message("Initializing browser...", "INFO")
            edge_options = Options()
            edge_options.add_argument("--disable-features=SmartScreen")
            edge_options.add_argument("--disable-popup-blocking")
            edge_options.add_argument("--log-level=3")
            edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

            service = Service(log_path="NUL")
            driver = webdriver.Edge(service=service, options=edge_options)

            try:
                log_message("Navigating to login page...", "INFO")
                driver.get("https://simpcity.cr/login/")
                time.sleep(3)
                
                log_message("Attempting login...", "INFO")
                login_to_simpcity(driver, username, password)
                log_message("✓ Login successful", "SUCCESS")

                total_pages = len(urls)
                for i, url in enumerate(urls):
                    if not generation_in_progress[0]:
                        log_message("Generation cancelled by user", "WARNING")
                        break

                    stats["current_page"] = i + 1
                    frame.after(0, update_stats)

                    log_message(f"Scraping page {i+1}/{total_pages}: {url}", "INFO")
                    frame.after(0, lambda: progress_label.config(
                        text=f"Processing page {i+1} of {total_pages}..."
                    ))

                    driver.get(url)
                    time.sleep(5)  # Wait for page to load

                    page_data = scrape_page(driver)
                    all_posts_data.extend(page_data)
                    
                    stats["posts"] = len(all_posts_data)
                    frame.after(0, update_stats)
                    
                    log_message(f"✓ Found {len(page_data)} posts on page {i+1}", "SUCCESS")

                    # Update progress bar
                    progress = ((i + 1) / total_pages) * 100
                    frame.after(0, lambda val=progress: progress_bar.configure(value=val))

                if generation_in_progress[0]:
                    # Save the final JSON file
                    output_filename = os.path.join(
                        output_directory,
                        f"{folder_name}_{datetime.date.today().strftime('%Y%m%d')}.json"
                    )
                    with open(output_filename, "w", encoding="utf-8") as f:
                        json.dump(all_posts_data, f, indent=2, ensure_ascii=False)

                    log_message("=" * 50, "INFO")
                    log_message(f"✓ Generation complete!", "SUCCESS")
                    log_message(f"Total posts: {len(all_posts_data)}", "SUCCESS")
                    log_message(f"Output file: {output_filename}", "SUCCESS")
                    
                    frame.after(0, lambda: progress_label.config(
                        text="✓ Generation completed successfully!",
                        foreground="#1DB954"
                    ))

            finally:
                driver.quit()
                log_message("Browser closed", "INFO")

        except Exception as e:
            log_message(f"✗ An error occurred: {str(e)}", "ERROR")
            frame.after(0, lambda: progress_label.config(
                text="✗ Generation failed. Check log for details.",
                foreground="#E22134"
            ))

        finally:
            generation_in_progress[0] = False
            frame.after(0, lambda: start_button.config(state="normal", text="🚀 Start Generation"))
            frame.after(0, lambda: cancel_button.config(state="disabled"))

    def get_folder_name(url):
        """Extract folder name from URL"""
        url = url.rstrip('/')
        parts = url.split('/')
        if 'threads' in parts:
            idx = parts.index('threads')
            if idx + 1 < len(parts):
                return parts[idx + 1].split('.')[0]
        return "default_content"

    # Control buttons
    button_container = tb.Frame(frame, bootstyle="dark")
    button_container.pack(fill="x", pady=15)

    start_button = tb.Button(
        button_container,
        text="🚀 Start Generation",
        bootstyle="success",
        command=start_generation,
        width=20
    )
    start_button.pack(side="left", padx=5, ipady=8)

    cancel_button = tb.Button(
        button_container,
        text="⏹️ Cancel",
        bootstyle="danger",
        command=cancel_generation,
        width=12,
        state="disabled"
    )
    cancel_button.pack(side="left", padx=5, ipady=8)

    # Load initial URL count
    try:
        with open(urls_file, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
        stats["urls"] = len(urls)
        stats["total_pages"] = len(urls)
        update_stats()
    except:
        pass

    return frame