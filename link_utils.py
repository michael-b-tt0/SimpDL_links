import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from ttkbootstrap.tooltip import ToolTip

def generate_links(base_link, num_pages):
    """Generate paginated links from a base URL"""
    links = [base_link.rstrip("/")]
    for page_num in range(2, num_pages + 1):
        new_link = f"{base_link.rstrip('/')}/page-{page_num}"
        links.append(new_link)
    return links

def build_generate_links_frame(parent, urls_file, refresh_urls_func=None):
    """
    Creates an enhanced Frame for generating multiple paginated links
    """
    frame = tb.Frame(parent, bootstyle="dark")

    # Header section
    header_container = tb.Frame(frame, bootstyle="dark")
    header_container.pack(fill="x", pady=(0, 20))

    title_label = tb.Label(
        header_container,
        text="🔗 Link Generator",
        font=("Segoe UI", 20, "bold")
    )
    title_label.pack(anchor="w")

    subtitle_label = tb.Label(
        header_container,
        text="Automatically generate paginated URLs for bulk scraping",
        font=("Segoe UI", 11),
        foreground="#B3B3B3"
    )
    subtitle_label.pack(anchor="w", pady=(5, 0))

    # Info card with instructions
    info_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    info_card.pack(fill="x", pady=(0, 20), padx=5)
    info_card.configure(borderwidth=2)

    info_content = tb.Frame(info_card, bootstyle="secondary")
    info_content.pack(fill="x", padx=20, pady=15)

    info_icon = tb.Label(
        info_content,
        text="💡",
        font=("Segoe UI", 16)
    )
    info_icon.pack(side="left", padx=(0, 10))

    info_text = tb.Label(
        info_content,
        text="Enter the base thread URL and specify how many pages to scrape.\n"
             "The generator will create URLs for page-1, page-2, page-3, etc.",
        font=("Segoe UI", 10),
        justify="left",
        foreground="#B3B3B3"
    )
    info_text.pack(side="left", anchor="w")

    # Input card
    input_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    input_card.pack(fill="x", pady=(0, 15), padx=5)
    input_card.configure(borderwidth=2)

    input_content = tb.Frame(input_card, bootstyle="secondary")
    input_content.pack(fill="both", padx=20, pady=20)

    # Base link input
    base_link_frame = tb.Frame(input_content, bootstyle="secondary")
    base_link_frame.pack(fill="x", pady=(0, 15))

    base_link_label = tb.Label(
        base_link_frame,
        text="Base Thread URL",
        font=("Segoe UI", 10, "bold")
    )
    base_link_label.pack(anchor="w", pady=(0, 5))

    base_link_entry = tb.Entry(
        base_link_frame,
        font=("Segoe UI", 10),
        bootstyle="secondary"
    )
    base_link_entry.pack(fill="x", ipady=6)
    base_link_entry.insert(0, "https://simpcity.cr/threads/example-thread.12345/")

    # Add tooltip
    ToolTip(
        base_link_entry,
        text="Enter the full URL of the first page of the thread",
        bootstyle="info"
    )

    # Number of pages input
    pages_frame = tb.Frame(input_content, bootstyle="secondary")
    pages_frame.pack(fill="x", pady=(0, 10))

    pages_label = tb.Label(
        pages_frame,
        text="Number of Pages",
        font=("Segoe UI", 10, "bold")
    )
    pages_label.pack(anchor="w", pady=(0, 5))

    pages_input_frame = tb.Frame(pages_frame, bootstyle="secondary")
    pages_input_frame.pack(fill="x")

    pages_entry = tb.Entry(
        pages_input_frame,
        font=("Segoe UI", 10),
        bootstyle="secondary",
        width=15
    )
    pages_entry.pack(side="left", ipady=6)
    pages_entry.insert(0, "1")

    pages_hint = tb.Label(
        pages_input_frame,
        text="Must be at least 2 pages",
        font=("Segoe UI", 9),
        foreground="#888888"
    )
    pages_hint.pack(side="left", padx=10)

    # Preview section
    preview_card = tb.Frame(frame, bootstyle="secondary", relief="flat")
    preview_shown = [False]

    preview_content = tb.Frame(preview_card, bootstyle="secondary")
    preview_content.pack(fill="both", padx=20, pady=15)

    preview_title = tb.Label(
        preview_content,
        text="👁️ Link Preview",
        font=("Segoe UI", 11, "bold")
    )
    preview_title.pack(anchor="w", pady=(0, 10))

    preview_text = tk.Text(
        preview_content,
        height=8,
        bg="#1E1E1E",
        fg="#D4D4D4",
        wrap="word",
        font=("Consolas", 9),
        relief="flat",
        padx=10,
        pady=10,
        state="disabled"
    )
    preview_text.pack(fill="both", expand=True)

    preview_count_label = tb.Label(
        preview_content,
        text="",
        font=("Segoe UI", 9),
        foreground="#1DB954"
    )
    preview_count_label.pack(anchor="w", pady=(5, 0))

    # Status message
    status_frame = tb.Frame(frame, bootstyle="dark")
    status_frame.pack(fill="x", pady=15)

    status_label = tb.Label(
        status_frame,
        text="",
        font=("Segoe UI", 10),
        bootstyle="inverse-dark"
    )
    status_label.pack()

    def show_preview():
        """Show the preview card"""
        if not preview_shown[0]:
            preview_card.pack(fill="x", pady=(15, 0), padx=5)
            preview_shown[0] = True

    def update_preview():
        """Update the preview with generated links"""
        base_link = base_link_entry.get().strip()
        try:
            num_pages = int(pages_entry.get())
            
            if not base_link:
                return
            
            if num_pages < 2:
                return
            
            links = generate_links(base_link, num_pages)
            
            preview_text.config(state="normal")
            preview_text.delete(1.0, tk.END)
            
            for i, link in enumerate(links[:10], 1):  # Show first 10
                preview_text.insert(tk.END, f"{i}. {link}\n")
            
            if len(links) > 10:
                preview_text.insert(tk.END, f"\n... and {len(links) - 10} more links")
            
            preview_text.config(state="disabled")
            preview_count_label.config(text=f"Total: {len(links)} links will be generated")
            
            show_preview()
            generate_btn.config(state="normal")
            
        except ValueError:
            pass

    # Bind events for live preview
    base_link_entry.bind("<KeyRelease>", lambda e: update_preview())
    pages_entry.bind("<KeyRelease>", lambda e: update_preview())

    def validate_input():
        """Validate user input"""
        base_link = base_link_entry.get().strip()
        
        if not base_link:
            return False, "Please enter a base URL"
        
        if not base_link.startswith(("http://", "https://")):
            return False, "URL must start with http:// or https://"
        
        try:
            num_pages = int(pages_entry.get())
            if num_pages < 2:
                return False, "Number of pages must be at least 2"
            if num_pages > 1000:
                return False, "Number of pages cannot exceed 1000"
        except ValueError:
            return False, "Please enter a valid number of pages"
        
        return True, "Valid input"

    def generate():
        """Generate and save links"""
        is_valid, message = validate_input()
        
        if not is_valid:
            status_label.config(text=f"❌ {message}", foreground="#E22134")
            return
        
        base_link = base_link_entry.get().strip()
        num_pages = int(pages_entry.get())
        
        try:
            # Generate links
            links = generate_links(base_link, num_pages)
            
            # Save to file
            with open(urls_file, "w") as f:
                for link in links:
                    f.write(link + "\n")
            
            status_label.config(
                text=f"✅ Successfully generated {len(links)} links and saved to URLs file!",
                foreground="#1DB954"
            )
            
            # Refresh the URLs page if callback provided
            if refresh_urls_func:
                refresh_urls_func()
            
            # Clear status after 5 seconds
            frame.after(5000, lambda: status_label.config(text=""))
            
        except Exception as e:
            status_label.config(
                text=f"❌ Error: {str(e)}",
                foreground="#E22134"
            )

    # Button container
    button_container = tb.Frame(frame, bootstyle="dark")
    button_container.pack(fill="x", pady=10)

    generate_btn = tb.Button(
        button_container,
        text="🚀 Generate Links",
        bootstyle="success",
        command=generate,
        state="disabled",
        width=20
    )
    generate_btn.pack(ipady=10)

    # Example section
    example_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    example_card.pack(fill="x", pady=(20, 0), padx=5)
    example_card.configure(borderwidth=2)

    example_content = tb.Frame(example_card, bootstyle="secondary")
    example_content.pack(fill="x", padx=20, pady=15)

    example_title = tb.Label(
        example_content,
        text="📋 Example",
        font=("Segoe UI", 10, "bold")
    )
    example_title.pack(anchor="w", pady=(0, 8))

    example_text = tb.Label(
        example_content,
        text="Input: https://simpcity.cr/threads/example.12345/ with 3 pages\n"
             "Output:\n"
             "  1. https://simpcity.cr/threads/example.12345/\n"
             "  2. https://simpcity.cr/threads/example.12345/page-2\n"
             "  3. https://simpcity.cr/threads/example.12345/page-3",
        font=("Consolas", 9),
        justify="left",
        foreground="#B3B3B3"
    )
    example_text.pack(anchor="w")

    return frame