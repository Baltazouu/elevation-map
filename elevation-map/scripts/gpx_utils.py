import os
import gzip

DATA_FOLDER = "data"

def save_gpx_from_gzip(gzip_data: bytes) -> str:
    """Décompresse un fichier gzip et sauvegarde le GPX dans le dossier data."""
    try:
        gpx_data = gzip.decompress(gzip_data)
    except gzip.BadGzipFile:
        raise ValueError("Le fichier fourni n'est pas un GZIP valide.")
    
    # Compter le nombre de fichiers GPX existants pour déterminer le nom
    existing_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".gpx")]
    new_filename = f"trajet{len(existing_files) + 1}.gpx"
    new_file_path = os.path.join(DATA_FOLDER, new_filename)

    # Sauvegarder le fichier
    with open(new_file_path, "wb") as f:
        f.write(gpx_data)

    return new_filename

