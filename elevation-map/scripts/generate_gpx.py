import os
import gpxpy
import gpxpy.gpx

def merge_gpx_files(gpx_files, output_file):
    combined_gpx = gpxpy.gpx.GPX()
    merged_track = gpxpy.gpx.GPXTrack()
    merged_segment = gpxpy.gpx.GPXTrackSegment()

    for gpx_file in gpx_files:
        with open(gpx_file, 'r') as f:
            gpx = gpxpy.parse(f)
        for track in gpx.tracks:
            for segment in track.segments:
                merged_segment.points.extend(segment.points)

    merged_track.segments.append(merged_segment)
    combined_gpx.tracks.append(merged_track)

    with open(output_file, 'w') as f:
        f.write(combined_gpx.to_xml())

    print(f"Fichier GPX fusionné créé : {output_file}")

if __name__ == "__main__":
    gpx_files = [os.path.join("data", f) for f in os.listdir("data") if f.endswith('.gpx')]

    if not gpx_files:
        print("Aucun fichier GPX trouvé dans le dossier 'data'.")
    else:
        merge_gpx_files(gpx_files, "output/output.gpx")

