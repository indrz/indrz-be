import Vector from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { getCenter } from 'ol/extent';
import config from '~/util/indrzConfig';
import POIHandler from '~/util/POIHandler';
import MapUtil from '~/util/map';
import api from '~/util/api';
import { openIndrzPopup, getTitle, getBuildingLetter, setI18n } from './popupModel';

const { env } = config;
const hostUrl = window.location.origin;

const closeIndrzPopup = (popup, globalPopupInfo) => {
  popup.setPosition(undefined);
  for (const member in globalPopupInfo) {
    globalPopupInfo[member] = null;
  }
  popup.setPosition(undefined);
  globalPopupInfo.poiId = 'noid';
  globalPopupInfo.poiCatId = 'noid';
  globalPopupInfo.bookId = false;
  globalPopupInfo.bookCoords = false;
  globalPopupInfo.name = false;
  return false;
};



// `addPoiTableRow` is legacy (DOM-based). Keep as a no-op to preserve API.
const addPoiTableRow = (_label, _value, _idname) => {};

const getRoomInfo = (floor, layers) => {
  const availableWmsLayers = layers.switchableLayers;
  let newel;

  availableWmsLayers.forEach(function (element) {
    if (floor === (env.LAYER_NAME_PREFIX + element.getProperties().floorNum)) {
      newel = element.getSource();
    }
  });
  return newel;
};

const handleShareClick = (mapInfo, globalPopupInfo, globalRouteInfo, globalSearchInfo, activeFloorNum, isRouteShare) => {
  let param = '';

  if (isRouteShare) {
    param = 'route';
  } else if (globalPopupInfo.bookId) {
    param = 'bookId';
  } else if (globalPopupInfo.poiCatId) {
    param = 'poiCatId';
  } else if (globalPopupInfo.src === 'wms_building') {
    param = 'wmsBuilding';
  } else if (globalSearchInfo.searchText) {
    param = 'search';
  } else if (globalPopupInfo.src === 'wms') {
    param = 'wmsInfo';
  } else if (globalPopupInfo.name === 'XY Location') {
    param = 'xy';
  }
  return updateUrl(param, mapInfo, globalPopupInfo, globalRouteInfo, globalSearchInfo, activeFloorNum);
};

const getFloorNumFromActiveFloor = (activeFloorNum) => {
  if (activeFloorNum === null || activeFloorNum === undefined) return '';

  // activeFloorNum is typically like "floor_0" (env.LAYER_NAME_PREFIX + number)
  if (typeof activeFloorNum === 'string') {
    if (activeFloorNum.includes(env.LAYER_NAME_PREFIX)) {
      return activeFloorNum.split(env.LAYER_NAME_PREFIX)[1] ?? '';
    }
    return activeFloorNum;
  }

  // If a number slips through, stringify it.
  if (typeof activeFloorNum === 'number' && Number.isFinite(activeFloorNum)) {
    return String(activeFloorNum);
  }

  return '';
};

const updateUrl = (mode, mapInfo, globalPopupInfo, globalRouteInfo, globalSearchInfo, activeFloorNum) => {
  const { map } = mapInfo;
  const currentExtent2 = map.getView().calculateExtent(map.getSize());
  const currentZoom2 = map.getView().getZoom();
  const centerCrd = map.getView().getCenter();
  const centerX2 = centerCrd[0];
  const centerY2 = centerCrd[1];

  let url;

  switch (mode) {
    case 'route':
      if (globalRouteInfo.routeUrl) {
        url = globalRouteInfo.routeUrl;
      } else if ((globalRouteInfo.startPoiId !== 'noid' && globalRouteInfo.endPoiId !== 'noid') || globalPopupInfo.poiId !== 'noid') {
        url = globalRouteInfo.routeUrl;
      } else if (globalPopupInfo.poiId === 'undefined' && globalPopupInfo.poiId === '' && globalPopupInfo.poiId !== 'noid') {
        url = '?startstr=' + globalRouteInfo.startName + '&endstr=' + globalRouteInfo.endName;
      } else {
        url = '?startstr=' + globalRouteInfo.startName + '&endstr=' + globalRouteInfo.endName;
      }
      break;
    case 'search':
      if (globalPopupInfo.hasOwnProperty('external_id')) {
        if (globalPopupInfo.external_id === globalPopupInfo.name) {
          url = '?q=' + globalPopupInfo.external_id;
        } else {
          url = '?q=' + globalPopupInfo.name;
        }
      }
      if (globalSearchInfo.searchText) {
        url = '?q=' + globalSearchInfo.searchText;
      } else {
        url = '?q=' + globalPopupInfo.name;
      }
      break;
    case 'map':
      {
        const floorNum = activeFloorNum.includes(env.LAYER_NAME_PREFIX)
          ? activeFloorNum.split(env.LAYER_NAME_PREFIX)[1]
          : activeFloorNum;

        url = '?centerx=' + centerX2 + '&centery=' + centerY2 + '&zlevel=' + currentZoom2 + '&floor=' + floorNum;

        if (mapInfo.selectedPoiCatIds.length) {
          url = `${url}&poi-cat-id=${mapInfo.selectedPoiCatIds.join(',')}`
        }
        break;
      }
    case 'bookId':
      url = hostUrl + globalRouteInfo.routeUrl;
      break;
    case 'poiCatId':
      {
        url = location.origin + '?' + globalPopupInfo.poiCatShareUrl;

        const poiId = globalPopupInfo.poiId || globalSearchInfo?.selectedItem?.id;

        // Always include the active floor; do not rely on legacy globalPopupInfo.floor_num.
        const floorNum =
          (globalPopupInfo && (globalPopupInfo.floor_num ?? globalPopupInfo.floorNum)) ??
          getFloorNumFromActiveFloor(activeFloorNum);

        const singlePoiUrl = `${location.origin}?poi-id=${poiId}&floor=${floorNum}`;

        return {
          type: 'poi',
          singlePoiUrl,
          poiCatUrl: url
        };
      }
    case 'wmsBuilding':
      url = hostUrl + '?q=' + globalPopupInfo.name;
      break;
    case 'wmsInfo':
      if (globalPopupInfo.room_code) {
        url = hostUrl + '?q=' + globalPopupInfo.room_code;
      } else {
        url = hostUrl + '?q=' + globalPopupInfo.wmsInfo;
      }
      break;
    case 'xy':
      url = `${hostUrl}?q=coords&x=${globalPopupInfo.coords[0]}&y=${globalPopupInfo.coords[1]}`
      break;
    default:
      url = location.href;
      break;
  }

  const data = {};
  data.extent = currentExtent2;
  data.zoom = currentZoom2;
  history.pushState(data, 'live_url_update', url);
  return location.href;
};

const handlePoiLoad = (map, activeFloorNum, { removedItems, newItems, oldItems }, env) => {
  removedItems = Array.isArray(removedItems) ? removedItems : [];
  newItems = Array.isArray(newItems) ? newItems : [];
  oldItems = Array.isArray(oldItems) ? oldItems : [];

  newItems.forEach((newItem) => {
    if (newItem && newItem.children) {
      newItems = newItem.children.map(item => item);
    }
  });
  if (removedItems && removedItems.length) {
    removedItems.forEach((item) => {
      if (item && POIHandler.poiExist(item, map)) {
        POIHandler.disablePoiById(item.id, map);
      }
    });
  }
  if (oldItems && oldItems.length) {
    oldItems.forEach((item) => {
      if (item) {
        POIHandler.setPoiVisibility(item, map);
      }
    });
  }
  if (newItems && newItems.length) {
    const fetches = [];
    newItems.forEach((item) => {
      if (item) {
        if (POIHandler.poiExist(item, map)) {
          POIHandler.setPoiVisibility(item.id, map);
        } else {
          fetches.push(
            POIHandler
              .fetchPoi(item.id, map, activeFloorNum, env)
              .then((poiLayer) => {
                map.getLayers().forEach((layer) => {
                  if (layer.getProperties().id === 99999) {
                    layer.getLayers().push(poiLayer);
                  }
                });
                return poiLayer;
              })
          );
        }
      }
    });
    return Promise.all(fetches);
  }

  return Promise.resolve([]);
};

const handleMapClick = (mapInfo, evt) => {
  const pixel = evt.pixel;
  const features = [];

  mapInfo.map.forEachFeatureAtPixel(pixel, function (feature) {
    features.push(feature);
  });
  const feature = features[0];
  let coordinate = mapInfo.map.getCoordinateFromPixel(pixel);
  const properties = feature ? feature.getProperties() : null;
  if (feature) {
    const featureType = feature.getGeometry().getType().toString();

    if (featureType === 'MultiPolygon' || featureType === 'MultiPoint') {
      closeIndrzPopup(mapInfo.popup, mapInfo.globalPopupInfo);

      if (featureType === 'MultiPoint') {
        properties.poiId = feature.getId();
        properties.src = 'poi';
        coordinate = feature.getGeometry().flatCoordinates;
      }
      mapInfo.globalSearchInfo = {
        selectedItem: { type: featureType, properties },
        searchText: properties.name
      };
      mapInfo.openIndrzPopup(properties, coordinate, feature);
      MapUtil.activateFloor(feature, mapInfo.layers, mapInfo.map);
    } else if (featureType === 'Point') {
      closeIndrzPopup(mapInfo.popup, mapInfo.globalPopupInfo);
      coordinate = mapInfo.map.getCoordinateFromPixel(pixel);
      properties.src = 'poi';
      if (feature.getProperties().hasOwnProperty('poiId')) {
        properties.poiId = feature.properties.poiId;
      }
      mapInfo.globalSearchInfo = {
        selectedItem: { type: featureType, properties },
        searchText: properties.name
      };
      mapInfo.openIndrzPopup(properties, coordinate, feature);
      MapUtil.activateFloor(feature, mapInfo.layers, mapInfo.map);
    }
  } else {
    const featuresWms = mapInfo.map.getFeaturesAtPixel(pixel);
    const v = mapInfo.map.getView();
    const viewResolution = /** @type {number} */ (v.getResolution());

    // WMS source lookup
    // New behavior: a single TileWMS source lives on the Vue map component (mapInfo.wmsSource)
    // Legacy behavior: per-floor switchable WMS layers via layers.switchableLayers
    let wmsSource2 = mapInfo.wmsSource || getRoomInfo(mapInfo.activeFloorNum, mapInfo.layers);

    // If the user clicks before floors/layers have initialized, try to create the WMS layer lazily.
    if (!wmsSource2 && typeof mapInfo.ensureWmsLayer === 'function') {
      mapInfo.ensureWmsLayer();
      wmsSource2 = mapInfo.wmsSource || getRoomInfo(mapInfo.activeFloorNum, mapInfo.layers);
    }

    // Still not available: nothing to query yet.
    if (!wmsSource2 || typeof wmsSource2.getFeatureInfoUrl !== 'function') {
      mapInfo.globalSearchInfo = {};
      mapInfo.closeIndrzPopup(true);
      return;
    }

    const url = wmsSource2.getFeatureInfoUrl(coordinate, viewResolution, 'EPSG:3857', {
      INFO_FORMAT: 'application/json',
      FEATURE_COUNT: 50
    });

    if (url) {
      api.request({ url }).then((response) => {
        mapInfo.globalPopupInfo.src = 'wms';
        const listFeatures = response.data && response.data.features ? response.data.features : [];
        const dataProperties = {};

        if (listFeatures.length > 0) {
          listFeatures.some(function (feature) {
            if (feature.id.startsWith('campus')) {
              const centroidSource = new Vector({
                features: (new GeoJSON()).readFeatures(feature)
              });
              const centroidCoords = getCenter(centroidSource.getExtent());
              if (!dataProperties.properties) {
                dataProperties.properties = {};
              }
              dataProperties.properties = { ...dataProperties.properties, ...feature.properties };
              dataProperties.centroid = centroidCoords;
              dataProperties.properties.src = 'wms_campus';
              return dataProperties;
            }

            if (feature.properties.hasOwnProperty('street')) {
              const centroidSource = new Vector({
                features: (new GeoJSON()).readFeatures(feature)
              });
              const centroidCoords = getCenter(centroidSource.getExtent());
              if (!dataProperties.properties) {
                dataProperties.properties = {};
              }
              dataProperties.properties = { ...dataProperties.properties, ...feature.properties };
              dataProperties.centroid = centroidCoords;
              dataProperties.properties.src = 'wms_building';
              return dataProperties;
            }
            if (feature.properties.hasOwnProperty('space_type_id')) {
              if (feature.properties.hasOwnProperty('room_code') || feature.properties.hasOwnProperty('roomcode')) {
                const centroidSource = new Vector({
                  features: (new GeoJSON()).readFeatures(feature)
                });
                const centroidCoords = getCenter(centroidSource.getExtent());
                if (!dataProperties.properties) {
                  dataProperties.properties = {};
                }
                dataProperties.properties = { ...dataProperties.properties, ...feature.properties };
                dataProperties.centroid = centroidCoords;
                dataProperties.properties.src = 'wms';
                return dataProperties;
              }
            }
            return false;
          });

          mapInfo.globalSearchInfo = {
            selectedItem: { type: 'Feature', properties: dataProperties.properties },
            searchText: dataProperties.properties?.room_code
          };
          mapInfo.openIndrzPopup(dataProperties.properties, dataProperties.centroid, featuresWms)
        } else {
          mapInfo.globalSearchInfo = {};
          mapInfo.closeIndrzPopup(true);
          // Commented out the xy functionality issue #290
          /* const floor = mapInfo.floors.find(floor => (env.LAYER_NAME_PREFIX + floor.floor_num) === mapInfo.activeFloorNum);

          mapInfo.globalSearchInfo = {};
          mapInfo.openIndrzPopup({
            xy: coordinate,
            floor_num: floor?.floor_num,
            floor_name: floor?.short_name
          }, coordinate, null) */
        }
      }).catch((error) => {
        console.error('wms error geoserver', error);
      });
    } else {
      // No feature info URL => treat as empty click and close panel/popup.
      mapInfo.globalSearchInfo = {};
      mapInfo.closeIndrzPopup(true);
    }
  }
};

export default {
  closeIndrzPopup,
  openIndrzPopup,
  getTitle,
  getBuildingLetter,
  addPoiTableRow,
  getRoomInfo,
  handleShareClick,
  updateUrl,
  handlePoiLoad,
  handleMapClick,
  setI18n
};
