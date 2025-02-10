import pako from 'pako';

export const unzipGzip = (compressedData: ArrayBuffer): string => {
    try {
        const decompressedData = pako.ungzip(new Uint8Array(compressedData), { to: 'string' });
        return decompressedData;
    } catch (error) {
        console.error('Erreur lors de la décompression GZip:', error);
        return '';
    }
};

