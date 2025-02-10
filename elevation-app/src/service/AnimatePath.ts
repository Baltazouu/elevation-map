// import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import * as mapboxgl from 'mapbox-gl';

import * as turf from "@turf/turf";
import {computeCameraPosition} from "./Util";

const animatePath = async ({
                             map,
                             duration,
                             path,
                             startBearing,
                             startAltitude,
                             pitch,
                             setElevation,
                             setDistance
                           }) => {
  return new Promise<void>(async (resolve) => {
    const pathDistance = turf.lineDistance(path);
    let startTime;
    let previousElevation = null;
    let traveledCoordinates = [];
    let traveledColors = [];

    const getColorFromElevationChange = (elevationDiff, distance) => {
      const slope = elevationDiff / distance;

      if (slope > 0.15) return "#8B0000";
      if (slope > 0.1) return "#FF4500";
      if (slope > 0.05) return "#FFD700";
      if (slope < -0.15) return "#00008B";
      if (slope < -0.1) return "#4682B4";
      if (slope < -0.05) return "#87CEEB";
      return "#90EE90";
    };

    if (!map.getSource("path-source")) {
      map.addSource("path-source", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              geometry: {
                type: "LineString",
                coordinates: []
              },
              properties: {
                colors: []
              }
            }
          ]
        },
        lineMetrics: true
      });
    }

    if (!map.getLayer("path-layer")) {
      map.addLayer({
        id: "path-layer",
        type: "line",
        source: "path-source",
        paint: {
          "line-width": 4,
          "line-gradient": ["interpolate", ["linear"], ["line-progress"], 0, "#FFFFFF", 1, "#FFFFFF"]
        }
      });
    }

    if (!map.getSource("point-source")) {
      map.addSource("point-source", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: []
        }
      });
    }

    if (!map.getLayer("point-layer")) {
      map.addLayer({
        id: "point-layer",
        type: "circle",
        source: "point-source",
        paint: {
          "circle-radius": 10,
          "circle-color": "#FFD700"
        }
      });
    }

    const frame = async (currentTime) => {
      if (!startTime) startTime = currentTime;
      const animationPhase = (currentTime - startTime) / duration;
      if (animationPhase > 1) {
        resolve();
        return;
      }

      const currentDistance = pathDistance * animationPhase;
      const alongPath = turf.along(path, currentDistance).geometry.coordinates;
      const lngLat = { lng: alongPath[0], lat: alongPath[1] };

      traveledCoordinates.push([lngLat.lng, lngLat.lat]);

      let pointColor = "#FFD700";

      if (previousElevation !== null) {
        const dist = turf.distance(
            turf.point([traveledCoordinates[traveledCoordinates.length - 2][0], traveledCoordinates[traveledCoordinates.length - 2][1]]),
            turf.point([lngLat.lng, lngLat.lat])
        );

        const elevationDiff = Math.floor(map.queryTerrainElevation(lngLat, { exaggerated: false })) - previousElevation;
        pointColor = getColorFromElevationChange(elevationDiff, dist);
      }
      previousElevation = Math.floor(map.queryTerrainElevation(lngLat, { exaggerated: false }));

      traveledColors.push(pointColor);

      setDistance(currentDistance.toFixed(2));
      setElevation(previousElevation);

      if (map.getSource("point-source")) {
        map.getSource("point-source").setData({
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              geometry: {
                type: "Point",
                coordinates: [lngLat.lng, lngLat.lat]
              },
              properties: {
                color: pointColor
              }
            }
          ]
        });
      }

      if (map.getLayer("point-layer")) {
        map.setPaintProperty("point-layer", "circle-color", "#FFD700");
      }

      if (map.getSource("path-source") && map.getLayer("path-layer")) {
        map.getSource("path-source").setData({
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              geometry: {
                type: "LineString",
                coordinates: traveledCoordinates
              },
              properties: {
                colors: traveledColors
              }
            }
          ]
        });

        map.setPaintProperty("path-layer", "line-gradient", ["interpolate", ["linear"], ["line-progress"],
          ...traveledColors.flatMap((color, i) => [i / traveledColors.length, color])
        ]);
      }

      const bearing = startBearing;
      const correctedPosition = computeCameraPosition(
          pitch,
          bearing,
          lngLat,
          startAltitude,
          true
      );

      const camera = map.getFreeCameraOptions();
      camera.setPitchBearing(pitch, bearing);
      camera.position = mapboxgl.MercatorCoordinate.fromLngLat(
          correctedPosition,
          startAltitude
      );
      map.setFreeCameraOptions(camera);

      window.requestAnimationFrame(frame);
    };

    window.requestAnimationFrame(frame);
  });
};
export default animatePath;