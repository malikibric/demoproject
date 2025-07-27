import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

url = "https://olx.ba/pretraga?attr=&attr_encoded=1&q=stan&category_id=23&page=1&canton=9&cities="

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
geolocator = Nominatim(user_agent="olx_scraper")

ads = soup.select(".article-content")  # može varirati ako OLX promijeni strukturu

for ad in ads:
    title = ad.select_one("a").get_text(strip=True)
    price = ad.select_one(".price").get_text(strip=True) if ad.select_one(".price") else "N/A"
    location = ad.select_one(".location").get_text(strip=True) if ad.select_one(".location") else "Sarajevo"

    try:
        location_data = geolocator.geocode(f"{location}, Sarajevo")
        if location_data:
            lat, lon = location_data.latitude, location_data.longitude
            print(f"L.marker([{lat}, {lon}]).addTo(map)\n  .bindPopup(createPopup('{title}', '{price}', 'OLX'));\n")
    except:
        continue

print(soup.prettify())  # da vidimo šta se zapravo učitalo
