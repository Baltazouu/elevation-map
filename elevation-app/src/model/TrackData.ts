import { FeatureCollection } from "geojson";

export class TrackData {
    name?: string;
    time: string;

    points: Point[];

    constructor(points: Point[]) {
        this.points = points;
    }


    public toGeoJson(): FeatureCollection {
        const coordinates = this.points.map(p => [p.lon, p.lat, p.elevation]);
        return {
            type: "FeatureCollection",
            features: [
                {
                    type: "Feature",
                    properties: {},
                    geometry: {
                        type: "LineString",
                        coordinates: coordinates
                    }
                }
            ]
        }
    }

}

export class Point {
    lat: number;
    lon: number;
    elevation: number;
    time: string;
}
