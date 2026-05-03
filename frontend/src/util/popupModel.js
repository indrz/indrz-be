import config from './indrzConfig';

const { env } = config;

let translate = null;
const hostUrl = window.location.origin;

// cache translated popup labels per locale to avoid repeating translate.t calls
const _labelCache = new Map();

const getPopupLabels = (locale) => {
  const t = (key) => {
    try {
      return (translate && typeof translate.t === 'function') ? translate.t(key) : key;
    } catch (_e) {
      return key;
    }
  };

  const key = locale || 'en';
  if (_labelCache.has(key)) {
    return _labelCache.get(key);
  }
  const labels = {
    labelRoomCode: t('label_room_code'),
    labelFloorName: t('label_floor_name'),
    labelBuildingName: t('label_building_name'),
    labelCategory: t('label_category'),
    labelPoiName: t('label_nearest_entrance'),
    labelRoomId: t('label_room_id'),
    labelCapacity: t('label_capacity'),
    labelBuidingAdress: t('label_building_adress'),
    labelBuildingCode: t('label_building_code'),
    labelBuidingPlz: t('label_building_plz'),
    labelBuildingCity: t('label_building_city'),
    label_wing_name: t('label_wing_name'),
    labelExternalId: t('label_external_id')
  };
  _labelCache.set(key, labels);
  return labels;
};

const setI18n = (i18n) => {
  // Normalize various i18n shapes to an object with a `t(key)` function.
  // - vue-i18n composer: { t() }
  // - nuxt/i18n plugin: { global: { t() } }
  // - Vue instance: { $t() }
  if (!i18n) {
    translate = { t: (key) => key };
    _labelCache.clear();
    return;
  }

  if (typeof i18n.t === 'function') {
    translate = i18n;
  } else if (typeof i18n.$t === 'function') {
    translate = { t: i18n.$t.bind(i18n) };
  } else if (i18n.global && typeof i18n.global.t === 'function') {
    translate = i18n.global;
  } else {
    translate = { t: (key) => key };
  }

  _labelCache.clear();
};

const getTitle = (properties, locale = 'en') => {
  const resolvedLocale = (locale && typeof locale === 'object' && 'value' in locale) ? locale.value : locale;
  const t = (key) => {
    try {
      return (translate && typeof translate.t === 'function') ? translate.t(key) : key;
    } catch (_e) {
      return key;
    }
  };

  if (properties.street) {
    return properties.building_name;
  }
  if (properties['name_' + resolvedLocale]) {
    return properties['name_' + resolvedLocale];
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
    return t('directions');
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

const openIndrzPopup = (
  globalPopupInfo, popUpHomePage, currentLocale,
  objCenterCoords, routeToValTemp, routeFromValTemp,
  activeFloorNum, popup, properties, coordinate, feature, offsetArray) => {
  // popUpHomePage is legacy output; keep signature for compatibility

  // Collect details for the UI (LeftPanel/InfoOverlay can render this)
  const details = [];
  const pushDetail = (label, value) => {
    if (!label || value === undefined || value === null || value === '') return;
    details.push({ label, value });
  };

  // Normalize early
  const floorName = properties.floor_name;
  feature = (typeof feature !== 'undefined' && feature !== null) ? feature : -1;
  offsetArray = (typeof offsetArray !== 'undefined' && offsetArray !== null) ? offsetArray : [0, 0];

  // Keep globalPopupInfo updated for legacy share/routing flows
  for (const member in globalPopupInfo) {
    globalPopupInfo[member] = null;
  }
  globalPopupInfo.details = details;

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
  if (properties.hasOwnProperty('homepage') && properties.homepage) {
    globalPopupInfo.homepage = properties.homepage;
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
    globalPopupInfo.poiId = properties.poiId;
    if (properties.hasOwnProperty('category')) {
      globalPopupInfo.poiCatId = properties.category;
      if (currentLocale === 'de') {
        globalPopupInfo.poiCatName = properties.category.name_de;
      } else {
        globalPopupInfo.poiCatName = properties.category.name_en;
      }
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

  // category label for rooms (optional)
  let roomCat = null;
  if (properties.hasOwnProperty('category_de')) {
    if (properties.category_de) {
      roomCat = currentLocale === 'de' ? properties.category_de : properties.category_en;
    }
  }

  const title = getTitle(properties, currentLocale);
  const labels = getPopupLabels(currentLocale);

  // Build details array (legacy consumers still can use globalPopupInfo fields)
  if (properties.room_code) {
    pushDetail(labels.labelRoomCode, properties.room_code);
  }
  if (floorName && !properties.xy) {
    pushDetail(labels.labelFloorName, floorName);
  }
  if (properties.wing && !properties.xy) {
    pushDetail(labels.label_wing_name, properties.wing);
  }
  if (properties.capacity) {
    pushDetail(labels.labelCapacity, properties.capacity);
  }

  // Keep additional legacy details in globalPopupInfo for share/routing, but do not force them into the new details list
  if (properties.src === 'wms_campus') {
    globalPopupInfo.buildingAdress = properties.description;
  }
  if (properties.street) {
    globalPopupInfo.buildingAdress = properties.street;
    globalPopupInfo.buildingCode = properties.name;
    globalPopupInfo.buildingPlz = properties.postal_code;
    globalPopupInfo.buildingCity = properties.city;
  }
  if (roomCat) {
    globalPopupInfo.roomCategory = roomCat;
  }

  // Normalize coords
  const normalizedCoords = coordinate || (properties.centerGeometry?.coordinates);

  globalPopupInfo.name = title;
  globalPopupInfo.coords = normalizedCoords;
  globalPopupInfo.floor = activeFloorNum;

  popup.setPosition(coordinate);
  popup.setOffset(offsetArray);

  // Return a pure model for Vue
  return {
    title,
    details,
    src: globalPopupInfo.src,
    poiId: globalPopupInfo.poiId,
    poiCatId: globalPopupInfo.poiCatId,
    floor: globalPopupInfo.floor,
    coords: globalPopupInfo.coords,
    homepage: globalPopupInfo.homepage,
    properties
  };
};

export {
  openIndrzPopup,
  getTitle,
  getBuildingLetter,
  setI18n
};
