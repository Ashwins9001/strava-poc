import math
import json

def haversine(coord1, coord2):
    """Calculate the great-circle distance between two points (lat, lon) in km."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def split_coords_by_threshold(coords, threshold_km):
    """
    Splits list of coordinates into segments where consecutive points are within threshold_km.

    Args:
        coords (list of (lat, lon)): List of coordinate tuples.
        threshold_km (float): Distance threshold in kilometers.

    Returns:
        List of segments, where each segment is a list of coordinates.
    """
    if not coords:
        return []

    segments = []
    current_segment = [coords[0]]

    for i in range(1, len(coords)):
        dist = haversine(coords[i-1], coords[i])
        if dist <= threshold_km:
            current_segment.append(coords[i])
        else:
            # Distance exceeded threshold: start a new segment
            segments.append(current_segment)
            current_segment = [coords[i]]

    segments.append(current_segment)
    segments_js = json.dumps(segments)

    return segments_js


def generate_map(coordinates, threshold_km):

    segments = split_coords_by_threshold(coordinates, threshold_km)

    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

    # Create HTML with Leaflet map
    html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Leaflet Map with Multiple Segments</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet/dist/leaflet.css"
        />
        <style>
            html, body {{
                height: 100%;
                margin: 0;
                padding: 0;
            }}
            #map {{
                height: 100%;
                width: 100%;
            }}
        </style>
        </head>
        <body>

        <div id="map"></div>

        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

        <script>
        var segments = {segments};

        var colors = {colors};

        var map = L.map('map').setView([40, -80], 4);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);

        var layers = [];

        for (var i = 0; i < segments.length; i++) {{
            var color = colors[i % colors.length];
            var polyline = L.polyline(segments[i], {{ color: color }}).addTo(map);
            layers.push(polyline);
        }}

        var allPoints = [].concat.apply([], segments);
        var bounds = L.latLngBounds(allPoints);
        map.fitBounds(bounds);

        </script>

        </body>
        </html>
    """

    # Save the map to an HTML file
    with open("strava_leaflet_map.html", "w") as file:
        file.write(html_template)

    print("Leaflet map saved to 'strava_leaflet_map.html'. Open it in your browser.")