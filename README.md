# LinkedIn Profile Search Tool

This is a Python project that allows you to search for LinkedIn profiles based on contact names and company names. It uses various web scraping techniques and user agents to extract LinkedIn profile links from popular search engines. The project also incorporates PySimpleGUI for a user-friendly interface.

## Features

- Search for LinkedIn profiles by providing a CSV or Excel file containing contact names and company names.
- Choose from multiple search engines, including search.brave.com, bing.com, duckduckgo.com, and google.com.
- Rotates user agents and proxies to avoid detection and bypass rate limiting.
- Handles errors gracefully, switching to the next proxy if necessary.

## Prerequisites

Before running this project, make sure you have the following dependencies installed:

- Python (>= 3.6)
- PySimpleGUI (install via pip: `pip install PySimpleGUI`)
- pandas (install via pip: `pip install pandas`)
- BeautifulSoup (install via pip: `pip install beautifulsoup4`)
- openpyxl (install via pip: `pip install openpyxl`)
- requests (install via pip: `pip install requests`)

## Usage

1. Clone or download this project to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the following command to start the LinkedIn profile search tool:

   ```
   python linkedin_profile_search.py
   ```

4. The PySimpleGUI interface will appear, allowing you to:

   - Select a CSV or Excel file containing contact names and company names.
   - Choose a search engine from the available options.
   - Click the "Start Search" button to initiate the LinkedIn profile search.

## Important Notes

- Ensure that the CSV or Excel file contains columns named "Contact Name" and "Company."
- The tool will automatically switch to the next proxy if it encounters any errors during the search process.
- It limits the number of requests to the search engines to avoid being blocked or rate-limited.
- Results will be saved in a new CSV file with "_LinkedIn_Profiles" appended to the original file name.

## Disclaimer

Please use this tool responsibly and ensure that your actions comply with LinkedIn's terms of service and web scraping guidelines. Web scraping may be subject to legal restrictions, and excessive use could lead to IP bans or other consequences.

**Note:** The list of user agents and proxies used in this project may need periodic updates to remain effective, as websites and services often change their policies and detection methods.