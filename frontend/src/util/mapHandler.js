import Vector from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { getCenter } from 'ol/extent';
import axios from 'axios';
import config from '~/util/indrzConfig';
import POIHandler from '~/util/POIHandler';
import MapUtil from '~/util/map';

const { env } = config;
let translate = null;
const hostUrl = window.location.origin;

const setI18n = (i18n) => {
  translate = i18n;
};

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

const openIndrzPopup = (
  globalPopupInfo, popUpHomePage, currentPOIID, currentLocale,
  objCenterCoords, routeToValTemp, routeFromValTemp,
  activeFloorNum, popup, properties, coordinate, feature, offsetArray) => {
  const floorName = properties.floor_name;
  for (const member in globalPopupInfo) {
    globalPopupInfo[member] = null;
  }

  feature = (typeof feature !== 'undefined' && feature !== null) ? feature : -1;
  offsetArray = (typeof offsetArray !== 'undefined' && offsetArray !== null) ? offsetArray : [0, 0];

  if (properties.src === 'wms_campus') {
    globalPopupInfo.name = properties.name;
    globalPopupInfo.buildingAdress = properties.description;
  }

  if (properties.hasOwnProperty('street')) {
    globalPopupInfo.src = 'wms_building';
    globalPopupInfo.name = properties.name;
    globalPopupInfo.buildingName = properties.building_name;
    globalPopupInfo.buildingCity = properties.city;
    globalPopupInfo.buildingPlz = properties.postal_code;
    globalPopupInfo.buildingAdress = properties.street;
  }

  if (properties.hasOwnProperty('poiId')) {
    globalPopupInfo.src = 'poi';
    globalPopupInfo.poiId = properties.poiId;
  }
  if (properties.hasOwnProperty('category')) {
    globalPopupInfo.src = 'poi';
    globalPopupInfo.poiCatId = properties.category;
    offsetArray[1] = 0;
  }
  if (properties.hasOwnProperty('spaceid')) {
    globalPopupInfo.spaceid = properties.spaceid;
  }
  if (properties.hasOwnProperty('homepage')) {
    if (properties.homepage) {
      popUpHomePage = properties.homepage;
    }
  }
  if (properties.hasOwnProperty('src')) {
    if (properties.src) {
      globalPopupInfo.src = properties.src;
    }
  }
  if (properties.hasOwnProperty('space_type_id')) {
    if (properties.hasOwnProperty('src')) {
      if (properties.src) {
        globalPopupInfo.src = properties.src;
      } else {
        globalPopupInfo.src = 'wms';
      }
    }
    if (properties.hasOwnProperty('id')) {
      globalPopupInfo.spaceid = properties.id;
    }
    if (properties.hasOwnProperty('room_external_id')) {
      if (properties.room_external_id) {
        globalPopupInfo.external_id = properties.room_external_id;
      }
    }
  }
  if (properties.hasOwnProperty('room_code')) {
    globalPopupInfo.wmsInfo = properties.room_code;
  }
  if (properties.hasOwnProperty('roomcode')) {
    globalPopupInfo.wmsInfo = properties.roomcode;
  }
  if (properties.hasOwnProperty('poiId')) {
    currentPOIID = properties.poiId;
    globalPopupInfo.poiId = properties.poiId;
    if (properties.hasOwnProperty('category')) {
      globalPopupInfo.poiCatId = properties.category;
      if (currentLocale === 'de') {
        globalPopupInfo.poiCatName = properties.category.name_de;
      } else {
        globalPopupInfo.poiCatName = properties.category.name_en;
      }
      // globalPopupInfo.poiCatName = properties.category.cat_name;
      globalPopupInfo.poiCatShareUrl = hostUrl + '?poi-cat-id=' + globalPopupInfo.poiCatId;
    }
  } else if (feature !== -1) {
    if (globalPopupInfo.poiId === 'noid') {
      if (typeof feature !== 'string' && feature.getId()) {
        globalPopupInfo.poiId = feature.getId();
        globalPopupInfo.poiIdPopup = feature.getId();
        if (feature.get('category')) {
          globalPopupInfo.poiCatId = feature.get('category');
          if (currentLocale === 'de') {
            globalPopupInfo.poiCatName = feature.get('category_name_de');
          } else {
            globalPopupInfo.poiCatName = feature.get('category_name_en');
          }
          globalPopupInfo.poiCatShareUrl = hostUrl + '?poi-cat-id=' + globalPopupInfo.poiCatId;
        }
      }
    }
  }

  if (globalPopupInfo.poiId !== 'noid') {
    globalPopupInfo.poiCatShareUrl = 'poi-cat-id=' + globalPopupInfo.poiCatId;
  }
  objCenterCoords = coordinate;
  if (objCenterCoords || objCenterCoords !== '') {
    objCenterCoords = coordinate;
  } else {
    objCenterCoords = properties.centerGeometry.coordinates;
  }

  let titlePopup = '';

  const buildingName = getBuildingLetter(properties);
  let roomCode = null;
  let roomCat = null;

  if (properties.hasOwnProperty('category_de')) {
    if (properties.category_de) {
      if (currentLocale === 'de') {
        roomCat = properties.category_de;
      } else {
        roomCat = properties.category_en;
      }
    }
  }
  if (properties.hasOwnProperty('room_description')) {
    properties.name = properties.room_description;
  } else if (properties.hasOwnProperty('short_name')) {
    properties.name = properties.short_name;
  }

  titlePopup = getTitle(properties, currentLocale);

  if (typeof properties.label !== 'undefined') {
    roomCode = properties.room_code;
  } else {
    roomCode = properties.room_code;
  }
  const labelRoomCode = translate.t('label_room_code');
  const labelFloorName = translate.t('label_floor_name');
  const labelBuildingName = translate.t('label_building_name');
  const labelCategory = translate.t('label_category');
  const labelPoiName = translate.t('label_nearest_entrance');
  const labelRoomId = translate.t('label_room_id');
  const labelCapacity = translate.t('label_capacity');
  const labelBuidingAdress = translate.t('label_building_adress');
  const labelBuildingCode = translate.t('label_building_code');
  const labelBuidingPlz = translate.t('label_building_plz');
  const labelBuildingCity = translate.t('label_building_city');

  if (properties.src === 'wms_campus') {
    addPoiTableRow(labelBuidingAdress, properties.description, 'popup_building_adress');
  }

  if (properties.street) {
    addPoiTableRow(labelBuidingAdress, properties.street, 'popup_building_adress');
    addPoiTableRow(labelBuildingCode, properties.name, 'popup_building_code');
    addPoiTableRow(labelBuidingPlz, properties.postal_code, 'popup_building_plz');
    addPoiTableRow(labelBuildingCity, properties.city, 'popup_building_city');
  }

  if (properties.room_code) {
    addPoiTableRow(labelRoomCode, properties.room_code, 'popup_room_code');
  }
  if (floorName && !properties.xy) {
    addPoiTableRow(labelFloorName, floorName, 'popup_floor_name');
  }
  if (buildingName) {
    addPoiTableRow(labelBuildingName, buildingName, 'popup_building_name');
  }
  if (roomCat) {
    addPoiTableRow(labelCategory, roomCat, 'popup_room_cat');
  }
  if (properties.nearest_entrance) {
    addPoiTableRow(labelPoiName, properties.nearest_entrance, 'popup_nearest_entrance');
  }
  if (properties.room_external_id) {
    addPoiTableRow(labelRoomId, properties.room_external_id, 'popup_room_external_id');
  }
  if (properties.capacity) {
    addPoiTableRow(labelCapacity, properties.capacity, 'popup_room_capacity');
  }
  if (properties.xy) {
    addPoiTableRow('X', properties.xy[0].toFixed(3), 'popup_xy_x');
    addPoiTableRow('Y', properties.xy[1].toFixed(3), 'popup_xy_Y');
  }
  globalPopupInfo.name = titlePopup;
  globalPopupInfo.coords = objCenterCoords;
  globalPopupInfo.floor = activeFloorNum;
  globalPopupInfo.room_code = roomCode;
  globalPopupInfo.floor_num = properties.floor_num;

  popup.setPosition(coordinate);
  popup.setOffset(offsetArray);
};

const getTitle = (properties, locale = 'en') => {
  if (properties.street) {
    return properties.building_name;
  }
  if (properties['name_' + locale]) {
    return properties['name_' + locale];
  }
  if (properties.name) {
    return properties.name;
  }
  if (properties.short_name) {
    return properties.short_name;
  }
  if (properties.room_code) {
    return properties.room_code;
  }
  if (properties.label) {
    return properties.label;
  }
  if (properties.room_external_id) {
    return properties.room_external_id;
  }
  if (properties.xy) {
    return translate.t('directions');
  }
  return '';
};

const getBuildingLetter = (p) => {
  let buildingLetter;
  // TODO remove this roomcode stuf
  if (p.hasOwnProperty('building_name')) {
    if (p.building_name !== null || p.building_name !== '' || typeof p.building_name !== 'undefined') {
      buildingLetter = p.building_name;
      return buildingLetter;
    }
  } else if (p.hasOwnProperty('building')) {
    return p.building;
  }
  return '';
};

const addPoiTableRow = (label, value, idname) => {
  if (idname === 'popupHomepage') {
    value = '<a target="_blank" href="' + value + '">' + value + '</a>';
  }
};

const getRoomInfo = (floor, layers, layerNamePrefix) => {
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

const updateUrl = (mode, mapInfo, globalPopupInfo, globalRouteInfo, globalSearchInfo, activeFloorNum) => {
  const { map } = mapInfo;
  const currentExtent2 = map.getView().calculateExtent(map.getSize());
  const currentZoom2 = map.getView().getZoom();
  const centerCrd = map.getView().getCenter();
  const centerX2 = centerCrd[0];
  const centerY2 = centerCrd[1];
  // const buildingId = 1;

  let url = '?centerx=' + centerX2 + '&centery=' + centerY2 +
    '&zlevel=' + currentZoom2 + '&floor=' + activeFloorNum;

  const data = {};

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
      const floorNum = activeFloorNum.includes(env.LAYER_NAME_PREFIX) ? activeFloorNum.split(env.LAYER_NAME_PREFIX)[1] : activeFloorNum;
      url = '?centerx=' + centerX2 + '&centery=' + centerY2 + '&zlevel=' + currentZoom2 + '&floor=' + floorNum;

      if (mapInfo.selectedPoiCatIds.length) {
        url = `${url}&poi-cat-id=${mapInfo.selectedPoiCatIds.join(',')}`
      }
      break;
    case 'bookId':
      url = hostUrl + globalRouteInfo.routeUrl;
      break;
    case 'poiCatId':
      url = location.origin + '?' + globalPopupInfo.poiCatShareUrl;

      const poiId = globalPopupInfo.poiId || globalSearchInfo?.selectedItem?.id;
      const singlePoiUrl = `${location.origin}?poi-id=${poiId}&floor=${globalPopupInfo.floor_num}`;

      return {
        type: 'poi',
        singlePoiUrl,
        poiCatUrl: url
      };
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

  data.extent = currentExtent2;
  data.zoom = currentZoom2;
  history.pushState(data, 'live_url_update', url);
  return location.href;
};

const handlePoiLoad = (map, activeFloorNum, { removedItems, newItems, oldItems }, env) => {
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
    newItems.forEach((item) => {
      if (item) {
        if (POIHandler.poiExist(item, map)) {
          POIHandler.setPoiVisibility(item.id, map);
        } else {
          POIHandler
            .fetchPoi(item.id, map, activeFloorNum, env)
            .then((poiLayer) => {
              map.getLayers().forEach((layer) => {
                if (layer.getProperties().id === 99999) {
                  layer.getLayers().push(poiLayer);
                }
              });
            });
        }
      }
    });
  }
};

const handleMapClick = (mapInfo, evt, layerNamePrefix) => {
  const pixel = evt.pixel;
  let feature = mapInfo.map.getFeaturesAtPixel(pixel);
  const features = [];

  mapInfo.map.forEachFeatureAtPixel(pixel, function (feature, layer) {
    features.push(feature);
  });
  feature = features[0];
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
    const wmsSource2 = getRoomInfo(mapInfo.activeFloorNum, mapInfo.layers, layerNamePrefix);
    const url = wmsSource2.getFeatureInfoUrl(coordinate, viewResolution, 'EPSG:3857', {
      INFO_FORMAT: 'application/json',
      FEATURE_COUNT: 50
    });

    if (url) {
      axios.get(url).then((response) => {
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
