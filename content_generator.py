# Standard library imports
import os
import json
import threading
import tkinter as tk
import time

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
    Returns a Frame that scrapes content and generates a JSON file in a background thread.
    The output folder name is derived from the portion after 'threads/'
    in the first URL.
    """
    frame = tb.Frame(parent, bootstyle="dark")

    title = tb.Label(frame, text="Generate Content JSON", font=("Helvetica", 18, "bold"))
    title.pack(pady=10)

    progress_label = tb.Label(frame, text="Progress: Not started", font=("Helvetica", 12))
    progress_label.pack(pady=5)

    progress_bar = tb.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=5)

    log_text = tk.Text(frame, height=15, width=60, bg="#282828", fg="#1DB954", wrap="word")
    log_text.pack(pady=10, fill="both", expand=True)

    generation_in_progress = [False]

    def log_message(msg):
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)

    def start_generation():
        """Triggered by the button. Spawns a background thread for the main generation."""
        if generation_in_progress[0]:
            return

        generation_in_progress[0] = True
        start_button.config(state="disabled")
        log_message("Starting content generation...")
        threading.Thread(target=run_generation, daemon=True).start()

    def run_generation():
        """
        The main scraping logic, running in a background thread
        to keep the GUI responsive.
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

            if not urls:
                log_message("No URLs found. Please add URLs first.")
                return

            folder_name = get_folder_name(urls[0])
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            edge_options = Options()
            edge_options.add_argument("--disable-features=SmartScreen")
            edge_options.add_argument("--disable-popup-blocking")
            edge_options.add_argument("--log-level=3")
            edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

            service = Service(log_path="NUL")
            driver = webdriver.Edge(service=service, options=edge_options)

            try:
                driver.get("https://simpcity.cr/login/")
                time.sleep(3)
                login_to_simpcity(driver, username, password)
                log_message("Logged in successfully.")

                total_pages = len(urls)
                for i, url in enumerate(urls):
                    log_message(f"Scraping page {i+1}/{total_pages}: {url}")
                    driver.get(url)
                    time.sleep(5) # Wait for page to load

                    page_data = scrape_page(driver)
                    all_posts_data.extend(page_data)
                    log_message(f"Found {len(page_data)} posts on page {i+1}.")

                    # Update progress bar
                    progress = ((i + 1) / total_pages) * 100
                    frame.after(0, lambda val=progress: progress_bar.configure(value=val))
                    frame.after(0, lambda: progress_label.config(text=f"Scraped page {i+1}/{total_pages}"))

                # Save the final JSON file
                output_filename = os.path.join(output_directory, f"{folder_name}.json")
                with open(output_filename, "w", encoding="utf-8") as f:
                    json.dump(all_posts_data, f, indent=2, ensure_ascii=False)

                log_message(f"Successfully generated JSON file: {output_filename}")

            finally:
                driver.quit()

        except Exception as e:
            log_message(f"An error occurred: {str(e)}")

        finally:
            generation_in_progress[0] = False
            frame.after(0, lambda: start_button.config(state="normal"))

    def get_folder_name(url):
        url = url.rstrip('/')
        parts = url.split('/')
        if 'threads' in parts:
            idx = parts.index('threads')
            if idx + 1 < len(parts):
                return parts[idx + 1].split('.')[0] # Get name before any extension
        return "default_content"

    start_button = tb.Button(frame, text="Start Generation", bootstyle="success outline", command=start_generation)
    start_button.pack(pady=10)

    return frame
