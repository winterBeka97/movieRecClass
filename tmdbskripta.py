import requests
import json
import os  

API_KEY = "aad1178b228bb829e6922aacfbdb4717"
MOVIE_ID = "791373"
OUTPUT_FILE = f"reviews_{MOVIE_ID}.json"

DATA_FOLDER = "Data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

OUTPUT_PATH = os.path.join(DATA_FOLDER, OUTPUT_FILE)


url = f"https://api.themoviedb.org/3/movie/{MOVIE_ID}/reviews"
params = {
    "api_key": API_KEY,
    "language": "en-US",
    "page": 1
}

reviews = []
current_page = 1
total_pages = 1

try:
    while current_page <= total_pages:
        params["page"] = current_page
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        reviews.extend(data["results"])
        total_pages = data["total_pages"]
        current_page += 1

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {len(reviews)} reviews to {OUTPUT_PATH}")

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except KeyError:
    print("Error parsing API response - check your API key and movie ID")
except IOError as e:
    print(f"Error writing to file: {e}")
