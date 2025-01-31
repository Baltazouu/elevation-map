import os
import gpxpy
import gpxpy.gpx
import numpy as np
import folium
from branca.element import Template, MacroElement
import matplotlib.cm as cm
import matplotlib.colors as colors
from geopy.distance import geodesic

SIMPLIFICATION_FACTOR = 10

def calculate_distance(points):
    if len(points) < 2:
        return 0.0
    return round(sum(geodesic(points[i], points[i + 1]).km for i in range(len(points) - 1)), 2)

def extract_elevation_data(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    elevations = [point.elevation for track in gpx.tracks for segment in track.segments for point in segment.points]
    return np.array(elevations)

def analyze_elevation(elevations):
    if len(elevations) < 2:
        return 0, 0
    diffs = np.diff(elevations)
    return np.sum(diffs[diffs > 0]), abs(np.sum(diffs[diffs < 0]))

def simplify_points(points, factor=SIMPLIFICATION_FACTOR):
    return points[::factor]

def get_gradient_colors(elevations):
    norm = colors.Normalize(vmin=min(elevations), vmax=max(elevations))
    cmap = cm.get_cmap('RdYlGn_r')
    return [colors.to_hex(cmap(norm(e))) for e in elevations]

def get_advanced_gradient_colors(elevations):
    norm = colors.Normalize(vmin=min(elevations), vmax=max(elevations))
    cmap = colors.LinearSegmentedColormap.from_list("custom_cmap", [(0.0, "blue"), (0.25, "green"), (0.5, "yellow"), (0.75, "red"), (1.0, "black")])
    return [colors.to_hex(cmap(norm(e))) for e in elevations]

def plot_gpx_on_map(gpx_file_path, map_object):
    """
    Trace un itinéraire GPX avec des couleurs selon l'altitude, ajoute un marqueur de départ/arrivée,
    et permet d'afficher/cacher les tracés avec un contrôle interactif.
    """
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            points = [[point.latitude, point.longitude, point.elevation] for point in segment.points]

            # Simplification des points pour alléger la carte
            points = simplify_points(points)

            if points:
                lats_lons = [(p[0], p[1]) for p in points]
                elevations = [p[2] for p in points]

                # Analyse des altitudes
                min_elev, max_elev = min(elevations), max(elevations)
                positive_elev, negative_elev = analyze_elevation(elevations)
                distance = calculate_distance(lats_lons)

                # Génération des couleurs améliorées 🔥
                colors_list = get_advanced_gradient_colors(elevations)

                # Création d'un groupe pour gérer l'affichage du sentier
                layer_name = os.path.basename(gpx_file_path)
                trail_layer = folium.FeatureGroup(name=layer_name)

                # Ajout du tracé coloré
                for i in range(1, len(lats_lons)):
                    folium.PolyLine(
                        locations=[lats_lons[i - 1], lats_lons[i]],
                        color=colors_list[i - 1],
                        weight=4,
                        opacity=0.5  # Rend le tracé plus fluide
                    ).add_to(trail_layer)

                # Ajout d'un marqueur pour le départ 🚩
                folium.Marker(
                    location=lats_lons[0],
                    icon=folium.Icon(color="green", icon="flag"),
                    popup="Départ du sentier"
                ).add_to(trail_layer)

                # Ajout d'un marqueur pour l’arrivée 🏁 avec les INFOS !
                arrival_popup = folium.Popup(
                    f"<b>Infos du sentier</b><br>"
                    f"📏 Distance : {distance:.2f} km<br>"
                    f"⬆️ Dénivelé + : {positive_elev:.1f} m<br>"
                    f"⬇️ Dénivelé - : {negative_elev:.1f} m<br>"
                    f"⛰️ Altitude min : {min_elev:.1f} m<br>"
                    f"🏔️ Altitude max : {max_elev:.1f} m",
                    max_width=300
                )

                folium.Marker(
                    location=lats_lons[-1],
                    icon=folium.Icon(color="red", icon="info-sign"),
                    popup=arrival_popup
                ).add_to(trail_layer)

                # Ajout du tracé et des icônes sur la carte
                map_object.add_child(trail_layer)


def add_legend(map_object):
    legend_html = """
    <div style="position: fixed; top: 10px; right: 10px; width: 250px; height: 80px;
        background-color: white; z-index:9999; font-size:14px; border:2px solid grey; padding: 10px;">
        <b>Choix du Gradient</b><br>
        <button onclick="toggleGradient('standard')">Standard</button>
        <button onclick="toggleGradient('advanced')">Avancé</button>
    </div>
    <script>
    function toggleGradient(mode) {
        document.querySelectorAll(".leaflet-control-layers-selector").forEach(el => {
            if (el.nextSibling.innerText.includes(mode)) {
                el.click();
            }
        });
    }
    </script>
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    map_object.get_root().add_child(legend)

if __name__ == "__main__":
    map_center = [46.603354, 1.888334]
    map_object = folium.Map(location=map_center, zoom_start=6)
    gpx_files = [os.path.join("data", f) for f in os.listdir("data") if f.endswith('.gpx')]
    for gpx_file in gpx_files:
        plot_gpx_on_map(gpx_file, map_object)
    add_legend(map_object)
    folium.LayerControl().add_to(map_object)
    map_object.save("map.html")
    print("Carte générée avec sélection du gradient : map.html")
