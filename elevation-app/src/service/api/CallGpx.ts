import { unzipGzip } from '../../helpers/functions/UnzipGpx';

const apiUrl = 'http://localhost:8000';

export const getGpx = async (distance: number, elevation: number) => {
    try {
        const response = await fetch(apiUrl + '/generate_route?distance=' + distance + '&elevation=' + elevation, {
            method: 'GET',
            headers: {
                'Accept-Encoding': 'gzip',
            },
        });

        // Lire la réponse en tant qu'ArrayBuffer pour gérer GZip
        const compressedData = await response.arrayBuffer();

        // Décompresser la réponse GZip
        const gpxData = unzipGzip(compressedData);

        return gpxData;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
    }
};

export const addGpx = async (gzippedData: Uint8Array) => {
    try {
        const response = await fetch(apiUrl + '/upload_gpx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/gzip', // Spécifier que c'est un fichier gzip
            },
            body: gzippedData, // Envoi direct des données compressées
        });

        if (!response.ok) {
            const error = await response.json();
            console.error("Erreur :", error.detail);
        } else {
            const result = await response.json();
            console.log(result.message);
        }
    } catch (error) {
        console.error("Erreur lors de l'envoi du fichier :", error);
    }
};

