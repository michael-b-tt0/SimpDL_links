import os
import json
import webbrowser
from tkinter import filedialog
import ttkbootstrap as tb
from jinja2 import Environment, FileSystemLoader

def build_report_frame(parent):
    """
    Returns a Frame for generating an HTML report from a JSON file.
    """
    frame = tb.Frame(parent, bootstyle="dark")
    selected_file_path = ""

    title = tb.Label(frame, text="Generate HTML Report", font=("Helvetica", 18, "bold"))
    title.pack(pady=10)

    # Label to show the selected file path
    file_label = tb.Label(frame, text="No JSON file selected.", font=("Helvetica", 12))
    file_label.pack(pady=10)

    def select_file():
        nonlocal selected_file_path
        file_path = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if file_path:
            selected_file_path = file_path
            file_label.config(text=os.path.basename(selected_file_path))
            generate_button.config(state="normal")

    def generate_report():
        if not selected_file_path:
            return

        try:
            with open(selected_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template("template.html")
            html_content = template.render(posts=data)

            output_filename = os.path.splitext(os.path.basename(selected_file_path))[0] + ".html"
            output_filepath = os.path.join(os.path.dirname(selected_file_path), output_filename)

            with open(output_filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            webbrowser.open('file://' + os.path.realpath(output_filepath))
            file_label.config(text=f"Successfully generated {output_filename}")

        except Exception as e:
            file_label.config(text=f"Error: {str(e)}")

    # Button to select a JSON file
    select_button = tb.Button(frame, text="Select JSON File", bootstyle="primary outline", command=select_file)
    select_button.pack(pady=10)

    # Button to generate the HTML report
    generate_button = tb.Button(frame, text="Generate HTML Report", bootstyle="success outline", command=generate_report, state="disabled")
    generate_button.pack(pady=10)

    return frame
