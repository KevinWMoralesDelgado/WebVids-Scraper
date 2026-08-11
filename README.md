# MIA WebVIDS Scraper & Categorizer

A lightweight Python utility that extracts live flight data from Miami International Airport's (MIA) internal WebFIDS display system and organizes departures into clean, structured JSON feeds.

---

## 📌 Description

This script automates the retrieval of flight information directly from the WebVIDS portal at Miami International Airport. 
It captures active departure details, parses raw HTML table structures, determines concourse locations based on assigned gates, 
and categorizes flights by destination type (**Domestic** vs. **International**).

---

## 🚀 Features

* **Automated Data Extraction:** Connects to the internal WebFIDS endpoint to fetch real-time flight records.
* **Gate & Concourse Parsing:** Identifies assigned departure gates and extracts concourse designations automatically.
* **Flight Categorization:** Organizes departure data into separate **Domestic** and **International** flight streams.
* **Data Sanitization:** Cleans whitespace, handles HTML entities, and exports formatted JSON outputs.

---

## 🛠️ Tech Stack & Dependencies

* **Python 3.x**
* **[Requests](https://requests.readthedocs.io/):** Handles HTTP connections to the airport endpoint.
* **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/):** Parses and navigates the raw HTML structure.
* **`json` (Standard Library):** Formats and writes flight records to structured JSON files.

---

## 👤 Author

* **Author:** Kevin M
