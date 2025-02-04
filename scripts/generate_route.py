import os
import gpxpy
import numpy as np
import folium
import sys
from geopy.distance import geodesic
import matplotlib.cm as cm
import matplotlib.colors as colors
from functools import lru_cache

SIMPLIFICATION_FACTOR = 10

# Fonction pour calculer la distance entre des points GPS
@lru_cache(maxsize=None)
def calculate_distance(points):
    if len(points) < 2:
        return 0.0
    return round(sum(geodesic(points[i], points[i + 1]).km for i in range(len(points) - 1)), 2)

# Extraction des données d'élévation à partir d'un fichier GPX
def extract_elevation_data(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        elevations = [point.elevation for track in gpx.tracks for segment in track.segments for point in segment.points]
    return np.array(elevations)

# Découpage des segments en sous-segments avec une vérification plus rapide
def split_segments(points, max_segment_length_km=1.0):
    sub_segments = []
    current_segment = [points[0]]
    segment_distance = 0.0

    for i in range(1, len(points)):
        segment_distance += geodesic((points[i - 1][0], points[i - 1][1]), (points[i][0], points[i][1])).km
        current_segment.append(points[i])
        if segment_distance >= max_segment_length_km:
            sub_segments.append(current_segment)
            current_segment = [points[i]]
            segment_distance = 0.0

    if len(current_segment) > 1:
        sub_segments.append(current_segment)

    return sub_segments

# Analyse du dénivelé positif optimisée
def analyze_elevation(elevations):
    if len(elevations) < 2:
        return 0
    diffs = np.diff(elevations)
    return np.sum(diffs[diffs > 0])

# Extraction et découpe des segments de chaque GPX
def extract_segments(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        segments = []
        for track in gpx.tracks:
            for segment in track.segments:
                points = [[point.latitude, point.longitude, point.elevation] for point in segment.points]
                if len(points) > 1:
                    segments.extend(split_segments(points))
        return segments

# Recherche de la meilleure connexion entre segments
def find_best_connection(segment_a, segment_b):
    end_a = segment_a[-1]
    start_b = segment_b[0]
    return geodesic((end_a[0], end_a[1]), (start_b[0], start_b[1])).km

# Construction du trajet raccordé respectant les critères optimisée
# Construction du trajet raccordé respectant les critères optimisée
def create_connected_route(segments, target_distance, max_elevation):
    current_distance = 0
    current_elevation = 0
    route_segments = []

    if not segments:
        print("Aucun segment valide disponible.")
        return []

    # Trie initial pour prioriser les segments les plus longs
    segments.sort(key=lambda seg: -len(seg))
    route_segments.append(segments.pop(0))

    print("\nConstruction du trajet...")
    while current_distance < target_distance and segments:
        best_segment = None
        best_distance = float('inf')

        last_point = route_segments[-1][-1]
        for segment in segments:
            connection_distance = geodesic((last_point[0], last_point[1]), (segment[0][0], segment[0][1])).km
            if connection_distance < best_distance and connection_distance < 1.0:
                best_distance = connection_distance
                best_segment = segment

        if best_segment:
            # Ajouter la distance de connexion entre les segments
            connection_distance = geodesic((last_point[0], last_point[1]), (best_segment[0][0], best_segment[0][1])).km
            current_distance += connection_distance

            route_segments.append(best_segment)
            coords = [(p[0], p[1]) for p in best_segment]
            current_distance += calculate_distance(tuple(coords))
            current_elevation += analyze_elevation([p[2] for p in best_segment])
            segments.remove(best_segment)
            print(f"  ✓ Segment ajouté : Distance cumulée {current_distance:.2f} km, Dénivelé cumulé {current_elevation:.1f} m")
        else:
            print("  ✗ Aucun segment raccord trouvé, arrêt de la construction.")
            break

    print("\nTrajet construit avec succès.")
    print(f"Distance totale : {current_distance:.2f} km, Dénivelé positif : {current_elevation:.1f} m")
    return route_segments


# Affichage sur une carte Folium
def display_route_on_map(route_segments):
    map_center = [46.603354, 1.888334]
    map_object = folium.Map(location=map_center, zoom_start=6)

    if route_segments:
        # Ajouter les segments
        for segment in route_segments:
            coords = [(p[0], p[1]) for p in segment]
            folium.PolyLine(locations=coords, color='blue', weight=4, opacity=0.5).add_to(map_object)

        # Ajouter les marqueurs pour le début et la fin du trajet
        start_point = route_segments[0][0]
        end_point = route_segments[-1][-1]
        total_distance = calculate_distance(tuple([(p[0], p[1]) for segment in route_segments for p in segment]))
        total_elevation = sum(analyze_elevation([p[2] for p in segment]) for segment in route_segments)

        folium.Marker(
            location=[start_point[0], start_point[1]],
            popup=f"Départ du trajet\nDistance totale : {total_distance:.2f} km\nDénivelé positif : {total_elevation:.1f} m",
            icon=folium.Icon(color='green', icon='flag')
        ).add_to(map_object)

        folium.Marker(
            location=[end_point[0], end_point[1]],
            popup=f"Arrivée du trajet\nDistance totale : {total_distance:.2f} km\nDénivelé positif : {total_elevation:.1f} m",
            icon=folium.Icon(color='red', icon='flag')
        ).add_to(map_object)

    folium.LayerControl().add_to(map_object)
    map_object.save("templates/optimized_route.html")
    print("\nCarte générée dans templates/optimized_route.html.")

# Exemple d'utilisation
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python generate_route.py <distance> <elevation>")
        sys.exit(1)
    
    target_distance = float(sys.argv[1])
    max_elevation = float(sys.argv[2])
    
    # Code existant pour charger les fichiers GPX et générer le trajet optimal
    gpx_files = [os.path.join("data", f) for f in os.listdir("data") if f.endswith('.gpx')]
    all_segments = []

    for gpx_file_path in gpx_files:
        print(f"Chargement du fichier GPX : {gpx_file_path}")
        segments = extract_segments(gpx_file_path)
        all_segments.extend(segments)
        print(f"Segments extraits : {len(segments)}")

    # Création du trajet optimal
    route_segments = create_connected_route(all_segments, target_distance, max_elevation)

    # Affichage sur la carte
    display_route_on_map(route_segments)