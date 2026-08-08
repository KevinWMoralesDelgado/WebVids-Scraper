import json
import requests
from bs4 import BeautifulSoup


def connect_and_scrape():
    # Full endpoint URL (retaining all null parameters to avoid HTTP 500 server errors)
    url = "https://webvids.miami-airport.com/webfids/webfids_internal?action=turnsFrame&direction=D&serviceType=null&display=null&pageNo=1&flightsPerScreen=null&actSortType=asc&actSortCol=CXR&newSortCol=&pax=null"

    output_file = "data_dump.json"

    try:
        print("Getting all the data, standby...")
        response = requests.get(url, timeout=6)
        print(f"Server response code: {response.status_code}")

        if response.status_code == 200:
            print("Connected to the website.")

            # Parse the HTML response body into a BeautifulSoup object
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Locate all table rows in the HTML DOM
            rows = soup.find_all("tr")
            all_flights = []

            print(f"Found an estimated total of {len(rows)} rows.")

            for row in rows:
                # Extract text from each table cell (td), trimming whitespace and stripping non-breaking space characters (\xa0) upfront
                cells = [
                    cell.text.strip().replace("\xa0", "")
                    for cell in row.find_all("td")
                ]

                # Ensure the row contains expected flight data columns and is not an empty header
                if len(cells) >= 11 and cells[0] != "":
                    gate_raw = cells[10]
                    
                    # Validate gate value: truthy guard checks for None/empty strings, while startswith('&') filters raw HTML entities
                    gate_found = (
                        gate_raw
                        if gate_raw and not gate_raw.startswith("&")
                        else "Unassigned"
                    )

                    # Only process and record flights with an assigned gate
                    if gate_found != "Unassigned":
                        # Concourse is derived from the first character of the assigned gate (e.g., 'D12' -> 'D')
                        concourse_found = gate_found[0].upper()
                        
                        # Parse passenger count into an integer safely
                        pax_data = int(cells[9]) if cells[9].isdigit() else 0

                        # Map cleansed table cell indices directly to standard JSON keys
                        flight_entry = {
                            "Airline": cells[0],
                            "Flight #": cells[1],
                            "Aircraft": cells[2],
                            "Tail #": cells[3],
                            "Sched Time": cells[4],
                            "Actual Time": cells[5],
                            "Type": "International"
                            if cells[7] == "I"
                            else "Domestic",
                            "Destination": cells[8],
                            "Pax": pax_data,
                            "Gate": gate_found,
                            "Concourse": concourse_found,
                        }
                        
                        all_flights.append(flight_entry)

            print("Info processed. Saving everything to a JSON file...")

            # Write the collected list of dictionaries to disk formatted with 4-space indentation
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_flights, f, indent=4)

    except Exception as e:
        print(f"Something went wrong: {e}")
        return False

def get_international_flights():
    input_file = "data_dump.json"
    output_file = "international_flights.json"

    international_count  = 0
    international_flights = []

    try:
        with open(input_file, "r", encoding ="utf-8") as f:
            data = json.load(f)

            for flight in data:
                if flight.get("Type") ==  "International":
                    international_count += 1
                    international_flights.append(flight)

        print(f"Found {international_count} international flights.")

        with open(output_file, "w", encoding="utf-8") as f_:
            json.dump(international_flights, f_, indent=4)

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"💥 Error: {e}")

def get_domestic_flights():
    input_file = "data_dump.json"
    output_file = "domestic_flights.json"
    domestic_count = 0
    domestic_flights = []

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            for flight in data:
                if flight.get("Type") == "Domestic":
                    domestic_count += 1
                    domestic_flights.append(flight)

        print(f"Found {domestic_count} domestic flights.")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(domestic_flights, f, indent=4)

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"💥 Error: {e}")


if __name__ == "__main__":
    connect_and_scrape()
    get_international_flights()
    get_domestic_flights()