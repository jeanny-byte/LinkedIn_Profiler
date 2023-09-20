import time
import PySimpleGUI as sg
import pandas as pd
from bs4 import BeautifulSoup
import random
import requests
import os
import logging

# Define a list of user agents to rotate through
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/85.0',
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v15762694709 t4359033847046230594 athfa3c3975 altpub cvcv=2 smf=0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v4728014143579996337 t3426302838546509975 ath1fb31b7a altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 RuxitSynthetic/1.0 v8882666712577074484 t7527522693257895152 ath5ee645e0 altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v1950137287498130493 t2513504243886480416 ath5ee645e0 altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 RuxitSynthetic/1.0 v4975528860 t7896867101678076541 athfa3c3975 altpub cvcv=2 smf=0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v6183187319818126841 t3891685320802505868 ath1fb31b7a altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v15762718358 t4359033847046230594 athfa3c3975 altpub cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 RuxitSynthetic/1.0 v3308086730930119168 t3073221232537963778 ath259cea6f altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 RuxitSynthetic/1.0 v3594459638229758972 t3659150847447165606 athe94ac249 altpriv cvcv=2 smf=0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 RuxitSynthetic/1.0 v6766030086435051764 t4684696140914125110 ath93eb305d altpriv cvcv=2 smf=0"
    # Add more user agents as needed
]

# Define search engines and their URLs
search_engines = {
    "search.brave.com": "https://search.brave.com/search?q=",
    "www.bing.com": "https://www.bing.com/search?q=",
    "www.duckduckgo.com": "https://duckduckgo.com/?hps=1&q=",
    "www.google.com": "https://www.google.com/search?q=",
}

# Define a function to select a random user agent
def get_random_user_agent():
    return random.choice(user_agents)

# # Define a function to get a list of proxies from the API
# def get_proxies():
#     api_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=al"
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         return response.text.splitlines()
#     else:
#         return []

# Proxy lists
Local_Proxies = [
    '217.119.140.220:12324:14a46a7541d6b:10ab596399',
    '45.143.5.226:12324:14a46a7541d6b:10ab596399',
    '89.42.29.78:12324:14a46a7541d6b:10ab596399',
    '45.91.32.157:12324:14a46a7541d6b:10ab596399',
    '45.133.109.153:12324:14a46a7541d6b:10ab596399',
]
# Initialize the proxy list
proxy_list = Local_Proxies
current_proxy = None  # Variable to store the current proxy

# Define a function to rotate through the proxy list
def get_next_proxy():
    global proxy_list, current_proxy
    if not proxy_list:
        proxy_list = Local_Proxies
    current_proxy = proxy_list.pop(0)  # Get the next proxy from the list
    return current_proxy

# Define a function to split the proxy into components
def split_proxy(proxy_str):
    components = proxy_str.split(":")
    if len(components) == 4:
        ip, port, user, password = components
        return {
            "http": f"http://{user}:{password}@{ip}:{port}",
            "https": f"https://{user}:{password}@{ip}:{port}",
        }
    elif len(components) == 2:
        ip, port = components
        return {
            "http": f"http://{ip}:{port}",
            "https": f"https://{ip}:{port}",
        }
    else:
        return None

# Define a function to search the selected search engine and extract LinkedIn profiles
def search_linkedin_profiles(contact_name, company, selected_search_engine):
    if selected_search_engine not in search_engines:
        window["text_element"].update("Invalid search engine selected.")
        return []

    search_url = search_engines[selected_search_engine] + f'"{contact_name}" AND {company} LinkedIn profile'

    try:
        time.sleep(random.randint(5, 10))

        # Use the selected proxy to make the request
        if current_proxy:
            proxies = split_proxy(current_proxy)
        else:
            proxies = None

        headers = {
            'User-Agent': get_random_user_agent()
        }

        response = requests.get(search_url, headers=headers, proxies=proxies, timeout=30)

        time.sleep(3)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        linkedin_links = []  # Store the LinkedIn profile links
        link_count = 0

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'linkedin.com/in/' in href:
                text = link.text
                logging.info(text)
                linkedin_links.append(href)  # Append the LinkedIn profile link
                link_count += 1
                if link_count >= 3:
                    break  # Stop after collecting the first 3 links

        # Combine the first 3 links into a single cell, separated by commas
        links_combined = ', '.join(linkedin_links[:3])

        results.append({"LinkedIn Profiles": links_combined})

        return results

    except Exception as e:
        logging.error(f"Error: {e}")
        # If there was an error with the current proxy, switch to the next one
        if current_proxy:
            window["text_element"].update(f"Switching to the next proxy: {current_proxy}")
            get_next_proxy()
        return []

# Define the PySimpleGUI layout
layout = [
    [sg.Text("Select a .csv or .xlsx file:")],
    [sg.InputText(key="file_path"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")))],
    [sg.Text("Select a search engine:")],
    [sg.Radio("search.brave.com", "search_engine", default=True, key="search.brave.com"),
     sg.Radio("www.bing.com", "search_engine", key="www.bing.com"),
     sg.Radio("www.duckduckgo.com", "search_engine", key="www.duckduckgo.com"),
     sg.Radio("www.google.com", "search_engine", key="www.google.com")],
    [sg.Button("Start Search"), sg.Button("Exit")],
    [sg.Text("Progress Bar "),sg.ProgressBar(100, orientation="h", size=(20, 20), key="progress_bar")],
    [sg.Text("Status: "),sg.Text("", size=(50, 1), key="text_element")],
]

window = sg.Window("LinkedIn Search", layout, icon="linkedin-3-256.ico")

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Start Search":
        # Reset the request count before starting a new search
        request_count = 0

        file_path = values["file_path"]
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            sg.popup_error("Invalid file format. Please select a .csv or .xlsx file.")
            continue

        if "Contact Name" not in df.columns or "Company" not in df.columns:
            sg.popup_error("The file must contain columns named 'Contact Name' and 'Company'.")
            continue

        selected_search_engine = next(key for key, value in values.items() if value and key in search_engines)
        results = []

        for index, row in df.iterrows():
            contact_name = row["Contact Name"]
            company = row["Company"].replace("-", " ")
            window["text_element"].update(f'Searching... {contact_name} in {company}')
            search_results = search_linkedin_profiles(contact_name, company, selected_search_engine)
            results.extend(search_results)

            # Increment the request count
            request_count += 1

            # Check if the maximum number of requests has been reached
            max_requests = 10
            delay_duration = 1 * 60  # 1 minute

            # Update the progress bar
            progress = (index + 1) / len(df) * 100
            window["progress_bar"].update(progress)

            if request_count >= max_requests:
                window["text_element"].update(f"Reached {max_requests} requests. Waiting for {delay_duration / 60} minutes...")
                time.sleep(delay_duration)
                # Reset the request count after the delay
                request_count = 0



        if not results:
            window["text_element"].update("No matching results found.")
            continue

        else:
            # Create a new CSV file with the original file name plus "LinkedIn_Profiles"
            base_file_name = os.path.splitext(os.path.basename(file_path))[0]
            new_file_name = f"{base_file_name}_LinkedIn_Profiles.csv"
            window["text_element"].update(f'New file updated is stored as {new_file_name}')

            # Append the results to the original DataFrame and save to the new file
            df = pd.concat([df, pd.DataFrame(results)], axis=1)
            df.to_csv(new_file_name, index=False)

window.close()
