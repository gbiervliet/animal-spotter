import requests
from bs4 import BeautifulSoup
import json
import argparse

BASE_URL = "https://waarneming.nl/fieldwork/observations/explore/"

def parse_arguments():
    parser = argparse.ArgumentParser(description='animal observation data fetcher')
    parser.add_argument('--end_date', default="2025-05-21", help='End date for observations (YYYY-MM-DD)')
    parser.add_argument('--point_coords', default="5.854682922363281%2051.842903707882684", help='Point coordinates (format: lon%2Clat)')
    parser.add_argument('--distance', default="5", help='Search radius distance in km')
    parser.add_argument('--species_id', default="54", help='Species ID to search for')
    return parser.parse_args()

def fetch_observation_data(url):
    print("[*] Fetching JSON data...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "table" not in data:
        raise ValueError("Expected 'table' field in response JSON.")

    return data["table"]

def html_table_to_json(html_table):
    print("[*] Parsing HTML table manually...")
    soup = BeautifulSoup(html_table, "html.parser")
    table = soup.find("table")
    if not table:
        raise ValueError("No <table> found.")

    headers = []
    for th in table.find("thead").find_all("th"):
        headers.append(th.get_text(strip=True))

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row_data = {}
        for i, cell in enumerate(cells):
            key = headers[i] if i < len(headers) else f"column_{i}"
            if key !="" and key != "Route":
                row_data[key] = cell.get_text(strip=True)    
        rows.append(row_data)

    return rows

def main():
    args = parse_arguments()
    
    url = f"{BASE_URL}?end_date={args.end_date}&json=species_observations&point=POINT({args.point_coords})&distance={args.distance}&species_id={args.species_id}"
    
    html_table = fetch_observation_data(url)
    json_data = html_table_to_json(html_table)
    print(json.dumps(json_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()