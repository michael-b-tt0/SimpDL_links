import os
import json
import webbrowser
from tkinter import filedialog
import ttkbootstrap as tb
from jinja2 import Environment, FileSystemLoader

def build_report_frame(parent):
    """
    Returns an enhanced Frame for generating HTML reports from JSON files
    """
    frame = tb.Frame(parent, bootstyle="dark")
    selected_file_path = ""
    file_info = {"posts": 0, "size": "0 KB"}

    # Header section
    header_container = tb.Frame(frame, bootstyle="dark")
    header_container.pack(fill="x", pady=(0, 20))

    title = tb.Label(
        header_container,
        text="📄 Report Generator",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(anchor="w")

    subtitle = tb.Label(
        header_container,
        text="Create beautiful HTML reports from your JSON data",
        font=("Segoe UI", 11),
        foreground="#B3B3B3"
    )
    subtitle.pack(anchor="w", pady=(5, 0))

    # File selection card
    selection_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    selection_card.pack(fill="x", pady=(0, 15), padx=5)
    selection_card.configure(borderwidth=2)

    selection_content = tb.Frame(selection_card, bootstyle="secondary")
    selection_content.pack(fill="x", padx=20, pady=20)

    selection_title = tb.Label(
        selection_content,
        text="📁 Select JSON File",
        font=("Segoe UI", 11, "bold")
    )
    selection_title.pack(anchor="w", pady=(0, 10))

    # File display area
    file_display = tb.Frame(selection_content, bootstyle="dark", relief="raised")
    file_display.pack(fill="x", pady=(0, 15))
    file_display.configure(borderwidth=1)

    file_icon_label = tb.Label(
        file_display,
        text="📋",
        font=("Segoe UI", 24),
        bootstyle="inverse-dark"
    )
    file_icon_label.pack(side="left", padx=15, pady=15)

    file_info_frame = tb.Frame(file_display, bootstyle="dark")
    file_info_frame.pack(side="left", fill="x", expand=True, pady=15)

    file_name_label = tb.Label(
        file_info_frame,
        text="No file selected",
        font=("Segoe UI", 12, "bold"),
        anchor="w"
    )
    file_name_label.pack(anchor="w")

    file_details_label = tb.Label(
        file_info_frame,
        text="Click 'Browse' to select a JSON file",
        font=("Segoe UI", 9),
        foreground="#888888",
        anchor="w"
    )
    file_details_label.pack(anchor="w", pady=(3, 0))

    # Browse button
    browse_button = tb.Button(
        selection_content,
        text="🔍 Browse for JSON File",
        bootstyle="info",
        width=25
    )
    browse_button.pack(ipady=8)

    # File preview card (initially hidden)
    preview_card = tb.Frame(frame, bootstyle="secondary", relief="raised")
    preview_card.configure(borderwidth=2)
    preview_info_shown = [False]

    preview_content = tb.Frame(preview_card, bootstyle="secondary")
    preview_content.pack(fill="x", padx=20, pady=20)

    preview_title = tb.Label(
        preview_content,
        text="📊 File Preview",
        font=("Segoe UI", 11, "bold")
    )
    preview_title.pack(anchor="w", pady=(0, 10))

    # Stats row
    stats_row = tb.Frame(preview_content, bootstyle="secondary")
    stats_row.pack(fill="x")

    def create_preview_stat(parent, icon, label, value_id):
        container = tb.Frame(parent, bootstyle="secondary")
        container.pack(side="left", padx=15, pady=5)

        icon_label = tb.Label(
            container,
            text=icon,
            font=("Segoe UI", 16)
        )
        icon_label.pack(side="left", padx=(0, 8))

        info_frame = tb.Frame(container, bootstyle="secondary")
        info_frame.pack(side="left")

        val_label = tb.Label(
            info_frame,
            text="0",
            font=("Segoe UI", 14, "bold"),
            foreground="#1DB954"
        )
        val_label.pack(anchor="w")

        desc_label = tb.Label(
            info_frame,
            text=label,
            font=("Segoe UI", 9),
            foreground="#888888"
        )
        desc_label.pack(anchor="w")

        return val_label

    posts_preview = create_preview_stat(stats_row, "📝", "Total Posts", "posts")
    size_preview = create_preview_stat(stats_row, "💾", "File Size", "size")
    date_preview = create_preview_stat(stats_row, "📅", "Modified", "date")

    # Status message area
    status_frame = tb.Frame(frame, bootstyle="dark")
    status_frame.pack(fill="x", pady=15)

    status_label = tb.Label(
        status_frame,
        text="",
        font=("Segoe UI", 10),
        bootstyle="inverse-dark",
        wraplength=600
    )
    status_label.pack()

    def show_preview():
        """Show the preview card"""
        if not preview_info_shown[0]:
            preview_card.pack(fill="x", pady=(0, 15), padx=5)
            preview_info_shown[0] = True

    def hide_preview():
        """Hide the preview card"""
        if preview_info_shown[0]:
            preview_card.pack_forget()
            preview_info_shown[0] = False

    def select_file():
        """Handle file selection"""
        nonlocal selected_file_path
        file_path = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if file_path:
            selected_file_path = file_path
            filename = os.path.basename(selected_file_path)
            
            # Update file display
            file_name_label.config(text=filename)
            file_icon_label.config(text="✅")
            
            # Try to load and analyze the file
            try:
                with open(selected_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Get file info
                file_size = os.path.getsize(selected_file_path)
                size_kb = file_size / 1024
                size_mb = size_kb / 1024
                
                if size_mb >= 1:
                    size_str = f"{size_mb:.2f} MB"
                else:
                    size_str = f"{size_kb:.2f} KB"
                
                # Get modification date
                mod_time = os.path.getmtime(selected_file_path)
                import datetime
                mod_date = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
                
                # Update preview
                posts_preview.config(text=str(len(data)))
                size_preview.config(text=size_str)
                date_preview.config(text=mod_date)
                
                file_details_label.config(
                    text=f"{len(data)} posts • {size_str}",
                    foreground="#1DB954"
                )
                
                show_preview()
                generate_button.config(state="normal")
                status_label.config(text="")
                
            except json.JSONDecodeError:
                file_details_label.config(
                    text="⚠️ Invalid JSON file",
                    foreground="#E22134"
                )
                hide_preview()
                generate_button.config(state="disabled")
                status_label.config(
                    text="❌ The selected file is not a valid JSON file",
                    foreground="#E22134"
                )
            except Exception as e:
                file_details_label.config(
                    text=f"⚠️ Error reading file",
                    foreground="#E22134"
                )
                hide_preview()
                generate_button.config(state="disabled")
                status_label.config(
                    text=f"❌ Error: {str(e)}",
                    foreground="#E22134"
                )

    def generate_report():
        """Generate HTML report with progress feedback"""
        if not selected_file_path:
            return

        # Update button state
        generate_button.config(state="disabled", text="⏳ Generating...")
        status_label.config(text="🔄 Loading JSON data...", foreground="#1DB954")
        frame.update()

        try:
            with open(selected_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            status_label.config(text="🔄 Rendering HTML template...")
            frame.update()

            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template("template.html")
            html_content = template.render(posts=data)

            status_label.config(text="🔄 Writing HTML file...")
            frame.update()

            output_filename = os.path.splitext(os.path.basename(selected_file_path))[0] + ".html"
            output_filepath = os.path.join(os.path.dirname(selected_file_path), output_filename)

            with open(output_filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            status_label.config(text="🔄 Opening report in browser...")
            frame.update()

            webbrowser.open('file://' + os.path.realpath(output_filepath))
            
            status_label.config(
                text=f"✅ Report generated successfully! Saved as: {output_filename}",
                foreground="#1DB954"
            )
            
            # Reset button after delay
            frame.after(2000, lambda: generate_button.config(text="📄 Generate HTML Report"))

        except FileNotFoundError:
            status_label.config(
                text="❌ Error: template.html not found. Ensure it exists in the application directory.",
                foreground="#E22134"
            )
        except Exception as e:
            status_label.config(
                text=f"❌ Error generating report: {str(e)}",
                foreground="#E22134"
            )
        finally:
            generate_button.config(state="normal", text="📄 Generate HTML Report")

    # Connect browse button
    browse_button.config(command=select_file)

    # Action buttons
    button_container = tb.Frame(frame, bootstyle="dark")
    button_container.pack(fill="x", pady=20)

    generate_button = tb.Button(
        button_container,
        text="📄 Generate HTML Report",
        bootstyle="success",
        command=generate_report,
        state="disabled",
        width=25
    )
    generate_button.pack(ipady=10)

    # Info section
    info_container = tb.Frame(frame, bootstyle="dark")
    info_container.pack(fill="x", pady=(20, 0))

    info_card = tb.Frame(info_container, bootstyle="secondary", relief="raised")
    info_card.pack(fill="x", padx=5)
    info_card.configure(borderwidth=2)

    info_content = tb.Frame(info_card, bootstyle="secondary")
    info_content.pack(fill="x", padx=20, pady=15)

    info_title = tb.Label(
        info_content,
        text="ℹ️ Requirements",
        font=("Segoe UI", 10, "bold")
    )
    info_title.pack(anchor="w", pady=(0, 8))

    requirements = [
        "• A valid JSON file generated by the Content Generator",
        "• template.html file must exist in the application directory",
        "• Generated report will open automatically in your browser"
    ]

    for req in requirements:
        req_label = tb.Label(
            info_content,
            text=req,
            font=("Segoe UI", 9),
            foreground="#B3B3B3",
            anchor="w"
        )
        req_label.pack(anchor="w", pady=2)

    return frame