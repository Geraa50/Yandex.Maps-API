import requests
import folium

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'

def calculate_route_length(route_points):
    coords = ';'.join([f"{point[1]},{point[0]}" for point in route_points])
    url = f"https://routing.api.yandex.net/v2/router/buildRoute?apikey={API_KEY}&rll={coords}&mode=masstransit"
    
    response = requests.get(url)
    data = response.json()

    if 'errors' in data:
        raise ValueError(f"Ошибка при построении маршрута: {data['errors']}")

    length = sum([segment['distance'] for segment in data['route']['features']])
    return length

def display_route_on_map(route_points):
    map = folium.Map(location=[55.75, 37.61], zoom_start=10)

    folium.PolyLine(route_points, color='blue', weight=5).add_to(map)

    middle_point = len(route_points) // 2
    folium.Marker(route_points[middle_point]).add_to(map)

    map.save('route_map.html')

if __name__ == "__main__":
    route_points = [
        (55.7522, 37.6156),  # Красная площадь
        (55.7905, 37.6795),  # ВДНХ
        (55.7298, 37.6043)   # Горки парк
    ]

    route_length = calculate_route_length(route_points)
    print(f"Длина маршрута: {route_length / 1000:.2f} км")

    display_route_on_map(route_points)
