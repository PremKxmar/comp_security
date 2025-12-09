import geoip2.database
import os

def get_location(ip_address):
    try:
        # Path to the GeoLite2-City.mmdb file
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'GeoLite2-City.mmdb')
        
        if not os.path.exists(db_path):
            return "Unknown", "Unknown"

        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip_address)
            country = response.country.name
            city = response.city.name
            return country, city
    except Exception as e:
        # print(f"GeoIP Error: {e}")
        return "Unknown", "Unknown"
