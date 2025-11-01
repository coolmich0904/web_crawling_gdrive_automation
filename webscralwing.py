import time
import pandas as pd
import os
import json


try:
    from bs4 import BeautifulSoup
    import requests

    print("✓ BeautifulSoup & requests import successful\n")
except ImportError as e:
    print(f"❌ Import failed: {e}\n")
    print("Install: pip install beautifulsoup4 requests")
    exit()

# --- 1. Configuration Variables ---
EXCEL_FILE_PATH = r'C:\Users\irene\PycharmProjects\sample_web_crawling\interview_links.xlsx'
LINK_COLUMN_NAME = 'Web Links'
OUTPUT_FOLDER = r'C:\Users\irene\PycharmProjects\sample_web_crawling\transcripts'
JSON_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'interview_data.json')

print(f"📁 Current Directory: {os.getcwd()}")

# Generate Output Folder
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"✓ Created Folder: {OUTPUT_FOLDER}")
else:
    print(f"✓ Confirmed Folder: {OUTPUT_FOLDER}")

print()


# --- 2. Function to extract text from GeeksforGeeks ---
def scrape_websites(url):
    """Extract text from GeeksforGeeks page using BeautifulSoup"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        print(f"    Requesting webpage...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        text_lines = []

        # Method 1: Extract from article tag (recommended)
        article = soup.find('article')
        if article:
            for element in article.find_all(['p', 'h1', 'h2', 'h3', 'li', 'pre']):
                text = element.get_text(strip=True)
                if text:
                    text_lines.append(text)
        else:
            # Method 2: Extract from main tag (alternative)
            main = soup.find('main')
            if main:
                for element in main.find_all(['p', 'h1', 'h2', 'h3', 'li', 'pre']):
                    text = element.get_text(strip=True)
                    if text:
                        text_lines.append(text)

        extracted_text = '\n'.join(text_lines)

        return extracted_text if extracted_text else None

    except requests.exceptions.RequestException as e:
        print(f"    ❌ Request error: {str(e)[:100]}")
        return None
    except Exception as e:
        print(f"    ❌ Extraction error: {str(e)[:100]}")
        return None


# --- 3. Function to generate key from URL ---
def get_key_from_url(url):
    """Generate unique key from URL"""
    filename = url.split('/')[-1].split('?')[0]
    if not filename:
        filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
    return filename[:50]


# --- 4. Main scraping function ---
def scrape_all_websites(excel_path, column_name, output_folder, json_file):
    print(f"Reading {excel_path} File....")
    print(f"   File exists: {os.path.exists(excel_path)}\n")

    # Initialize JSON data dictionary
    json_data = {}

    # Load existing JSON if it exists
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print(f"✓ Loaded existing JSON: {len(json_data)} entries\n")
        except:
            json_data = {}

    try:
        print("  Trying: pandas.read_excel()...")
        df = pd.read_excel(excel_path)
        print(f"Read {len(df)} lines\n")

        success_count = 0
        for index, row in df.iterrows():
            website_url = row[column_name]
            print(f"[{index + 1}] URL: {website_url}")

            try:
                # Check URL validity
                if not str(website_url).startswith(('http://', 'https://')):
                    print(f"    ⚠️ Warning: Invalid URL format\n")
                    continue

                # Extract text from website
                extracted_text = scrape_websites(str(website_url))

                if extracted_text and len(extracted_text) > 0:
                    # Generate key
                    key = get_key_from_url(str(website_url))

                    # Add to JSON data
                    json_data[key] = {
                        "url": str(website_url),
                        "title": key,
                        "content": extracted_text,
                        "length": len(extracted_text)
                    }

                    print(f"    ✓ Added: {key}")
                    print(f"    Length: {len(extracted_text)} characters\n")
                    success_count += 1
                else:
                    print(f"    ❌ Text not found\n")

            except Exception as e:
                print(f"    ❌ Error occurred: {str(e)[:100]}\n")

        # Save JSON file
        if json_data:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

        print("=" * 60)
        print(f"✓ Completed! {success_count} websites added")
        print(f"✓ Total entries in JSON: {len(json_data)}")
        print(f"📂 Saved to: {json_file}")
        print("=" * 60)

    except FileNotFoundError:
        print(f"🚨 Error: Can't find file. Check path: {excel_path}")
    except KeyError:
        print(f"🚨 Error: No '{column_name}'. Check column name")


# --- 5. Run the function ---
print("\nStarting scraping...\n")
scrape_all_websites(EXCEL_FILE_PATH, LINK_COLUMN_NAME, OUTPUT_FOLDER, JSON_OUTPUT_FILE)

print("\n=== Final Check ===")
print(f"Excel file path: {EXCEL_FILE_PATH}")
print(f"Excel file exists: {os.path.exists(EXCEL_FILE_PATH)}")
if os.path.exists(JSON_OUTPUT_FILE):
    with open(JSON_OUTPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Total entries in JSON: {len(data)}")
    if data:
        keys = list(data.keys())[:3]
        print(f"Sample keys: {keys}")