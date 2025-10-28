# SimpDL

A Python application built with [ttkbootstrap](https://pypi.org/project/ttkbootstrap) and Selenium to **scrape and organize content** from [SimpCity](https://simpcity.su) with comprehensive **HTML reporting**. The tool supports:

- **Config editing** for credentials and output directory.
- **URL management** (change/add/remove links).
- **Automated login** to SimpCity using Selenium.
- **Content scraping** to JSON format with multithreaded processing.
- **HTML report generation** from JSON data with Jinja2 templating.
- **Real-time progress tracking** and statistics during operations.

This README walks you through **requirements**, **installation**, and **usage** instructions.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [1. Configure Application](#1-configure-application)
  - [2. Manage URLs](#2-manage-urls)
  - [3. Generate Links](#3-generate-links)
  - [4. Generate Content](#4-generate-content)
  - [5. Generate Reports](#5-generate-reports)
- [Running the Program](#running-the-program)
- [Troubleshooting](#troubleshooting)
- [Terms and Conditions](#terms-and-conditions)

---

## Requirements

The project depends on the following Python packages:

```txt
requests
selenium
ttkbootstrap
jinja2
```

These can be installed via:

```bash
pip install -r requirements.txt
```

> **Note**: You must also have **Chrome** (and the appropriate [ChromeDriver](https://chromedriver.chromium.org/downloads)) installed. On most systems, Selenium can detect your existing Chrome and match driver versions automatically.



## Installation

1. **Clone** this repository:

   ```bash
   git clone https://github.com/michael-b-tt0/SimpDL_links
   cd SimpDL
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Virtual Environment**:\
   If you prefer, create and activate a [virtual environment](https://docs.python.org/3/tutorial/venv.html), then install dependencies.

4. **Check config folder**:

   - Ensure you have a `config/` folder with:
     - `config.json` (for login credentials, output directory, etc.)
     - `urls.txt` (list of SimpCity links)

---

## Project Structure

```bash
SimpDL/

├─ config/
│  ├─ config.json      # stores username/password/output_directory
│  └─ urls.txt         # stores links
├─ main.py             # main GUI entry point
├─ config_utils.py     # frames for editing config & URL list
├─ content_generator.py # content scraping to JSON with multithreaded GUI
├─ report_generator.py  # HTML report generation from JSON with Jinja2
├─ scraper_utils.py     # core scraping functions
├─ login_utils.py       # simpcity login automation
├─ link_utils.py        # link generation & management frames
├─ styles.py            # UI styling and themes
├─ template.html        # Jinja2 template for HTML reports
├─ requirements.txt     # required packages
└─ README.md            # this file
```

---

## Usage

Once installed, you can run the application and **use the GUI** to edit config, manage URLs, generate links, scrape content to JSON, and generate HTML reports.

### 1. Configure Application

- Click **“Modify Config”** in the sidebar.
- You’ll see all keys from `config.json`, such as `username`, `password`, `output_directory`.
- Edit them as needed, then **Save**.
- **username** / **password** should match your SimpCity account.
- **output** is where the finished json content will go


### 2. Manage URLs

- Click **“Change URL File”** in the sidebar.
- A list of URLs from `urls.txt` is displayed.
- **Add New URL** at the bottom by typing into the entry and pressing **Enter** or clicking **Add**.
- **Delete Link** next to any entry to remove it from the file.

### 3. Generate Links

- Click **“Generate Links”** in the sidebar.
- Enter the **Base Link** (e.g., `https://simpcity.su/threads/nottrebeca_.180370/`) and **Number of Pages** (e.g., 5).
- The tool writes all pages (`page-1`, `page-2`, etc.) into `urls.txt` automatically.
- **Note**: You can edit these again in **Change URL File** if needed.

### 4. Generate Content

- Click **"Content Generator"** in the sidebar.
- The interface shows statistics like total URLs to process, posts found, and processing progress.
- Click **"Start Generation"** to begin multithreaded content scraping:
  1. **Logs in** to SimpCity using credentials in `config.json`.
  2. Visits each URL in `urls.txt` and scrapes thread/post data.
  3. Saves all content as JSON in your `output_directory`.
- Real-time progress tracking shows completion percentage and posts found.
- **Activity log** displays detailed status messages and errors.
- You can switch to other pages while content generation runs (the GUI won’t freeze).
> **Note**: A JSON file named `{folder_name}_{date}.json` will be created in your output directory containing all scraped content data.

### 5. Generate Reports

- Click **"Report Generator"** in the sidebar.
- **Browse** and select a JSON file generated by the Content Generator.
- File preview shows total posts, file size, and modification date.
- Click **"Generate HTML Report"** to create a beautiful HTML report:
  1. Loads and validates the selected JSON file.
  2. Renders the content using Jinja2 template (`template.html`).
  3. Saves HTML report in the same directory as the JSON file.
  4. Automatically opens the report in your default web browser.
  5. All unique links from pixeldrain and gofile sources are located at the top for easy assessment 
- Status messages guide you through the generation process.
> **Note**: The HTML report provides an organized, searchable view of all scraped content with styling and navigation.

---

## Running the Program

```bash
cd SimpDL
python main.py
```

You should see the **SimpDL** window open:

1. **Sidebar** on the left with navigation buttons.
2. **Home** page (default) with a welcome message.
3. Other pages as described above.

---

## Troubleshooting

- **Credentials**: If login fails, confirm your `username` and `password` in `config/config.json` are correct.
- **ChromeDriver**: If Selenium fails to launch Chrome, check that your **Chrome** version matches your **ChromeDriver** version.
- **Content Generation Issues**:
  - Ensure you have valid links in `urls.txt`.
  - Verify `output_directory` exists and is writable.
  - Check the activity log for specific error messages.
- **Report Generation Issues**:
  - Ensure you have a valid JSON file generated by Content Generator.
  - Verify `template.html` exists in the application directory.
  - Check browser permissions if the report doesn't open automatically.
- **Template Missing**: If you get template errors, ensure `template.html` is in the application root directory and hasn't been moved.
- **Tkinter Issues**:
  - **Windows**: Tkinter is included by default with Python. If you encounter issues, ensure you installed Python with the **Add Python to PATH** option.
  - **Linux**: Install via `sudo pacman -S tk` (Arch) or `sudo apt-get install python3-tk` (Ubuntu).
  - **macOS**: Ensure you have XQuartz or the correct Tcl/Tk environment.

---
