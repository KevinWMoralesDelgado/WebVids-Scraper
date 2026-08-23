import json
import requests
from bs4 import BeautifulSoup

# The names of the files where we will save our data
DATA_DUMP_FILE = "data_dump.json"
INTERNATIONAL_FILE = "international_flights.json"
DOMESTIC_FILE = "domestic_flights.json"


def connect_and_scrape():
    """Downloads flight information from the airport website and saves it."""
    # The website link to pull flight data from
    url = (
        "https://webvids.miami-airport.com/webfids/webfids_internal"
        "?action=turnsFrame&direction=D&serviceType=null&display=null"
        "&pageNo=1&flightsPerScreen=null&actSortType=asc&actSortCol=CXR"
        "&newSortCol=&pax=null"
    )

    try:
        print("Fetching data from Miami Airport...")
        # Reach out to the website (times out if the website takes longer than 6 seconds to answer)
        response = requests.get(url, timeout=6)
        print(f"Server response code: {response.status_code}")

        # Code 200 means "OK". If we get anything else, stop the program.
        if response.status_code != 200:
            print(f"Failed to connect. HTTP Status: {response.status_code}")
            return False

        print("Connected successfully. Parsing HTML...")
        # Load the raw website page into BeautifulSoup so we can search through it
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find every table row on the page
        rows = soup.find_all("tr")
        print(f"Found {len(rows)} table rows.")

        all_flights = []

        for row in rows:
            # Get the text from each cell in the row and clean up extra spaces
            cells = [
                cell.text.strip().replace("\xa0", "")
                for cell in row.find_all("td")
            ]

            # Skip empty rows or rows that don't have enough columns
            if len(cells) < 11 or not cells[0]:
                continue

            gate_raw = cells[10]

            # Skip rows where the gate is missing or broken
            if not gate_raw or gate_raw.startswith("&"):
                continue

            gate_found = gate_raw
            # Grab the first letter of the gate for the Concourse (e.g., 'D' from 'D12')
            concourse_found = gate_found[0].upper()

            # Make sure passenger count is a number, default to 0 if empty
            pax_data = int(cells[9]) if cells[9].isdigit() else 0

            # Organize all details into a clean dictionary
            flight_entry = {
                "Airline": cells[0],
                "Flight #": cells[1],
                "Aircraft": cells[2],
                "Tail #": cells[3],
                "Sched Time": cells[4],
                "Actual Time": cells[5],
                "Type": "International" if cells[7] == "I" else "Domestic",
                "Destination": cells[8],
                "Pax": pax_data,
                "Gate": gate_found,
                "Concourse": concourse_found,
            }

            all_flights.append(flight_entry)

        print(f"Processed {len(all_flights)} valid flights. Saving to file...")

        # Save all collected flights into our main JSON file
        with open(DATA_DUMP_FILE, "w", encoding="utf-8") as f:
            json.dump(all_flights, f, indent=4)

        return True

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return False


def process_flight_categories():
    """Separates saved flights into two new files: International and Domestic."""
    international_flights = []
    domestic_flights = []

    try:
        # Open and read the main flight file we saved earlier
        with open(DATA_DUMP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Sort each flight into the right list
        for flight in data:
            flight_type = flight.get("Type")
            if flight_type == "International":
                international_flights.append(flight)
            elif flight_type == "Domestic":
                domestic_flights.append(flight)

        print(f"International flights: {len(international_flights)}")
        print(f"Domestic flights: {len(domestic_flights)}")

        # Save the sorted lists into two separate JSON files
        with open(INTERNATIONAL_FILE, "w", encoding="utf-8") as inter_f, \
             open(DOMESTIC_FILE, "w", encoding="utf-8") as dom_f:
            json.dump(international_flights, inter_f, indent=4)
            json.dump(domestic_flights, dom_f, indent=4)

        print("Successfully exported categorized flight files!")

    except FileNotFoundError:
        print(f"❌ Error: The input file '{DATA_DUMP_FILE}' was not found.")
    except Exception as e:
        print(f"💥 Error processing flight data: {e}")


# Run the code
if __name__ == "__main__":
    if connect_and_scrape():
        process_flight_categories()