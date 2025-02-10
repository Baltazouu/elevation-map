from io import BytesIO
from fastapi import FastAPI, Query, Response, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import gzip
from scripts.generate_route import create_connected_route, display_route_on_map, extract_segments, generate_gpx
from scripts.gpx_utils import save_gpx_from_gzip 

app = FastAPI()

# Désactiver CORS pour toutes les origines (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate_route")
def generate_route(distance: float = Query(..., description="Distance cible en km"),
                   elevation: float = Query(..., description="Dénivelé positif max en m")):
    gpx_files = [os.path.join("data", f) for f in os.listdir("data") if f.endswith('.gpx')]
    all_segments = []
    
    for gpx_file_path in gpx_files:
        print(f"Chargement du fichier GPX : {gpx_file_path}")
        segments = extract_segments(gpx_file_path)
        all_segments.extend(segments)
        print(f"Segments extraits : {len(segments)}")
    
    # Création du trajet optimal
    route_segments = create_connected_route(all_segments, distance, elevation)
    gpx_data = generate_gpx(route_segments).encode("utf-8")
    # Compresser les données GPX
    compressed_data = gzip.compress(gpx_data)

    return Response(
        content=compressed_data,
        media_type="application/gzip",
        headers={"Content-Disposition": "attachment; filename=route.gpx.gz"}
    )

@app.get("/map")
def get_compressed_gpx():
    #gpx_path = "output/output.gpx"
    gpx_path = "data/trajet20.gpx"

    # Compression en mémoire
    with open(gpx_path, "rb") as f:
        gpx_data = f.read()

    compressed_data = gzip.compress(gpx_data)

    return Response(
        content=compressed_data,
        media_type="application/gzip",
        headers={"Content-Disposition": "attachment; filename=map.gpx.gz"}
    )
    
@app.post("/upload_gpx")
async def upload_gpx(request: Request):
    """Ajoute un GPX envoyé en tant que fichier compressé"""
    try:
        # Lire les données gzip envoyées
        gzipped_data = await request.body()

        # Appeler la fonction pour décompresser et sauvegarder le fichier
        saved_filename = save_gpx_from_gzip(gzipped_data)

        return {"message": f"GPX sauvegardé sous le nom {saved_filename}"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Pour lancer l'API : uvicorn nom_du_fichier:app --reload
