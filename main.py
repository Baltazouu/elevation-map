import os
import gpxpy
import gpxpy.gpx
import numpy as np
import folium
from branca.element import Template, MacroElement
import matplotlib.cm as cm
import matplotlib.colors as colors

SIMPLIFICATION_FACTOR = 10  # Garder 1 point sur 10 pour alléger la carte


def extract_elevation_data(gpx_file_path):
    """
    Lit un fichier GPX et extrait les données d'altitude.
    """
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        
    elevations = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                elevations.append(point.elevation)
    
    return np.array(elevations)


def analyze_elevation(elevations):
    """
    Analyse le dénivelé d'une liste d'altitudes.
    Retourne le dénivelé positif et négatif cumulés.
    """
    if len(elevations) < 2:
        return 0, 0
    
    # Différences entre chaque point
    diffs = np.diff(elevations)
    
    # Dénivelé positif (somme des montées) et négatif (somme des descentes)
    positive_elevation = np.sum(diffs[diffs > 0])
    negative_elevation = np.sum(diffs[diffs < 0])
    
    return positive_elevation, abs(negative_elevation)


def simplify_points(points, factor=SIMPLIFICATION_FACTOR):
    """
    Simplifie les points pour réduire la charge graphique.
    """
    return points[::factor]


def plot_gpx_on_map(gpx_file_path, map_object):
    """
    Trace un itinéraire GPX sur une carte Folium avec un gradient en fonction de l'altitude.
    """
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    
    for track in gpx.tracks:
        for segment in track.segments:
            points = []
            for point in segment.points:
                points.append([point.latitude, point.longitude, point.elevation])

            # Simplification des points
            points = simplify_points(points)

            if points:
                lats_lons = [(p[0], p[1]) for p in points]
                elevations = [p[2] for p in points]

                # Création d'une ligne colorée selon l'altitude
                colors_list = get_gradient_colors(elevations)

                for i in range(1, len(lats_lons)):
                    folium.PolyLine(
                        locations=[lats_lons[i - 1], lats_lons[i]],
                        color=colors_list[i - 1],
                        weight=4,
                        opacity=0.7
                    ).add_to(map_object)


def get_gradient_colors(elevations):
    """
    Génère une liste de couleurs pour chaque segment selon l'altitude.
    """
    if len(elevations) == 0:
        return ["black"]

    # Normalisation des altitudes pour les mapper entre 0 et 1
    norm = colors.Normalize(vmin=min(elevations), vmax=max(elevations))
    cmap = cm.get_cmap('RdYlGn_r')  # Rouge -> Jaune -> Vert inversé

    # Générer une liste de couleurs pour chaque segment
    color_gradient = [colors.to_hex(cmap(norm(e))) for e in elevations]

    return color_gradient


def add_legend(map_object):
    """
    Ajoute une légende à la carte Folium.
    """
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px; left: 50px; width: 200px; height: 120px;
        background-color: white; z-index:9999; font-size:14px;
        border:2px solid grey; padding: 10px;
        ">
        <b>Légende Dénivelé</b><br>
        <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Faible dénivelé<br>
        <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Dénivelé modéré<br>
        <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Dénivelé élevé
    </div>
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    map_object.get_root().add_child(legend)


def load_all_gpx_files(directory):
    """
    Charge tous les fichiers GPX d'un dossier donné.
    """
    gpx_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.gpx')]
    if not gpx_files:
        print("Aucun fichier GPX trouvé.")
        return []

    print(f"{len(gpx_files)} fichier(s) GPX trouvé(s) : {gpx_files}")
    return gpx_files


if __name__ == "__main__":
    # Création de la carte centrée
    map_center = [46.603354, 1.888334]
    map_object = folium.Map(location=map_center, zoom_start=6)

    # Chargement et tracé de tous les fichiers GPX
    gpx_files = load_all_gpx_files("data")
    for gpx_file in gpx_files:
        plot_gpx_on_map(gpx_file, map_object)

    # Ajout de la légende
    add_legend(map_object)

    # Sauvegarde de la carte
    map_object.save("map_gradient.html")
    print("Carte générée avec tous les trajets : map_gradient.html")
