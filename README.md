# meteoblue Vacation Climate API

This project is a lightweight FastAPI application designed to support data-driven travel planning.  
Instead of relying on a static database, the system dynamically retrieves geographic information and long-term climate statistics using two external meteoblue APIs:

1. **Location Search API** – resolves user-provided city names into coordinates  
2. **modelclimate-day API** – provides ERA5-based climate normals (≈35-year averages)

The application processes these datasets to generate insights such as:
- annual climate profiles for any destination  
- the most suitable months to visit a location based on a simple comfort index  

This project is part of an academic assignment focusing on conceptual modeling, UML, and Python system implementation.

---

## Features

### **1. Location-based Climate Retrieval**
`GET /climate/{city_name}`  
Retrieves monthly climate normals for temperature, precipitation, and sunshine days.

### **2. Best Travel Month Recommendation**
`GET /recommendation/city/{city_name}`  
Computes a comfort score for each month and returns the top 3 months, including a human-readable summary.

### **3. Automatic City Resolution**
No predefined list of cities needed.  
The system uses meteoblue’s Location API to resolve any valid city worldwide.

---

## Technology Stack

- **FastAPI** – application framework  
- **Python 3.10+**  
- **meteoblue APIs**  
- **Requests** library for HTTP integration  
- **Uvicorn** for local development server  

No local database is required; all data is pulled on demand.

---

## Project Structure

app/
│── main.py # FastAPI endpoints
│── location_client.py # Calls meteoblue Location Search API
│── meteoblue_client.py # Retrieves climate normals
│── scoring.py # Comfort index & scoring logic
│── config.py # Loads API key from .env
│── init.py
requirements.txt
README.md

yaml
Code kopieren

---

##  Environment Variables

Create a `.env` file in the project root:

METEOBLUE_API_KEY=your_api_key_here

yaml
Code kopieren

The project will not run without this key.

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
Start the server:

bash
copy code
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Open Swagger documentation:

bash
copy code
http://localhost:8000/docs
Example Endpoints
Climate Data
bash
Code kopieren
GET /climate/Basel
Best Travel Months
bash
copy code
GET /recommendation/city/Berlin
Purpose of This Project
This project demonstrates:

conceptual data modeling (ER diagrams)

UML modeling (use case & class diagrams)

API-driven system implementation in Python

integration of external data sources instead of a local DB

a prototype for climate-based travel advisory logic

License
For educational use only.