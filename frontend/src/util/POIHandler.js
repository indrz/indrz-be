import SourceVector from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Group from 'ol/layer/Group';
import { getCenter } from 'ol/extent';
import MapStyles from './mapStyles';
import MapUtil from './map';
import MapHandler from './mapHandler';
import config from './indrzConfig';
import api from './api';

const { env } = config;
const fetchPoi = (catId, map, activeFloorNum) => {
  return api.request({
    endPoint: `poi/cat/${catId}/?format=json`
  }, env)
    .then((response) => {
      return createPoilayer(response.data, catId, activeFloorNum, env.layerNamePrefix);
    });
};

const setPoiVisibility = (poiId, map) => {
  map.getLayers().forEach(function (layer) {
    if (layer instanceof Group) {
      layer.getLayers().forEach(function (sublayer, i) {
        if (sublayer.getProperties().id === poiId) {
          if (sublayer.getVisible() === true) {
            sublayer.setVisible(false);
          } else {
            sublayer.setVisible(true);
          }
        }
      });
    }
  });
};

const disablePoiById = (poiId, map) => {
  map.getLayers().forEach(function (layer, i) {
    if (layer instanceof Group) {
      if (layer.getProperties().id === 99999) {
        layer.getLayers().forEach(function (sublayer) {
          if (sublayer.getProperties().id === poiId) {
            sublayer.setVisible(false);
          }
        });
      }
    }
  });
};

const removePoiById = (poiId, map) => {
  map.getLayers().forEach(function (layer, i) {
    if (layer instanceof Group) {
      if (layer.getProperties().id === 99999) {
        layer.getLayers().forEach(function (sublayer) {
          if (sublayer.getProperties().id === poiId) {
            sublayer.setVisible(false);
            map.removeLayer(sublayer);
          }
        });
      }
    }
  });
};

const poiExist = (poiItem, map) => {
  const poiName = typeof poiItem.name !== 'undefined' ? poiItem.name : 0;
  const poiCatId = poiItem.id;
  let isExists = false;

  map.getLayers().forEach(function (layer, i) {
    if (layer instanceof Group) {
      layer.getLayers().forEach(function (sublayer, i) {
        if (sublayer.getProperties().id === poiCatId || sublayer.getProperties().name === poiName) {
          isExists = true;
        }
      });
    }
  });

  return isExists;
};

const createPoiVectorLayer = (poiSource, activeFloorNum, id, layerName = '') => {
  return new VectorLayer({
    source: poiSource,
    style: function (feature) {
      const properties = feature.getProperties();
      const poiFeatureFloor = properties.floor_num;
      const icon = properties.icon;

      if ((env.LAYER_NAME_PREFIX + poiFeatureFloor) === activeFloorNum) {
        feature.setStyle(MapStyles.createPoiStyle(icon, 'y', poiFeatureFloor));
      } else {
        feature.setStyle(MapStyles.createPoiStyle(icon, 'n', poiFeatureFloor));
      }
    },
    title: layerName,
    name: layerName,
    id,
    active: true,
    visible: true,
    zIndex: 999
  });
};

const createPoilayer = (data, poiCatId, activeFloorNum, layerName = '') => {
  const poiSource = new SourceVector();
  const geojsonFormat3 = new GeoJSON();
  const featuresSearch = geojsonFormat3.readFeatures(data, { featureProjection: 'EPSG:4326' });
  poiSource.addFeatures(featuresSearch);

  return createPoiVectorLayer(poiSource, activeFloorNum, poiCatId, layerName);
};

const loadSinglePoi = async (poiId) => {
  const { data } = await api.request({
    endPoint: `poi/${poiId}/?format=json`
  });
  const geojsonFormat3 = new GeoJSON();

  return geojsonFormat3.readFeatures(data, { featureProjection: 'EPSG:4326' });
};

const addPoisToMap = async (poiIds, map, activeFloorNum, layerName = '') => {
  let poiProperties;
  let poiLayer;
  const features = [];

  if (!Array.isArray(poiIds)) {
    poiIds = [poiIds];
  }

  for (const poiId of poiIds) {
    const poiSingleLayer = map
      .getLayers()
      .getArray()
      .find(layer => layer.getProperties() && layer.getProperties().id === parseInt(poiId, 10));
    if (poiSingleLayer) {
      map.removeLayer(poiSingleLayer);
    }
    const feature = await loadSinglePoi(poiId);
    features.push(feature[0]);
  }

  const poiSource = new SourceVector();

  poiSource.addFeatures(features);

  if (features.length) {
    poiProperties = features[0].getProperties();
    poiProperties.poiId = poiIds[0];

    poiLayer = createPoiVectorLayer(poiSource, activeFloorNum, poiProperties.poiId, layerName || poiProperties.name);

    map.addLayer(poiLayer);
  }

  return {
    poiLayer: poiLayer,
    properties: poiProperties,
    centerCoord: getCenter(poiSource.getExtent())
  };
};

const showSinglePoi = async (poiId, globalPopupInfo, zlevel, map, popup, activeFloorNum, layerNamePrefix) => {
  const offSetPos = [0, 0];
  const { poiLayer, properties, centerCoord } = await addPoisToMap(poiId, map, activeFloorNum);

  globalPopupInfo.poiId = poiId;
  globalPopupInfo.poiCatId = properties.category;
  globalPopupInfo.poiCatShareUrl = '?poi-cat-id=' + properties.category;
  MapHandler.openIndrzPopup(globalPopupInfo, null, poiId, 'en', null,
    null, null, activeFloorNum, popup, properties, centerCoord,
    null, offSetPos, layerNamePrefix);
  MapUtil.zoomer(map.getView(), centerCoord, zlevel);

  return {
    layer: poiLayer,
    feature: properties
  };
};

const setPoiFeatureVisibility = (map, activeFloorNum, layerNamePrefix) => {
  map.getLayers().forEach(function (layer, i) {
    if (layer instanceof Group) {
      if (layer.getProperties().name === 'poi group' || layer.getProperties().name === 'POI-Gruppe') {
        layer.getLayers().forEach(function (sublayer, i) {
          sublayer.getSource().forEachFeature(function (feature, i) {
            if ((env.LAYER_NAME_PREFIX + feature.getProperties().floor_num) !== activeFloorNum) {
              feature.setStyle(MapStyles.setPoiStyleOnLayerSwitch(feature.getProperties().icon, false));
            } else {
              feature.setStyle(MapStyles.setPoiStyleOnLayerSwitch(feature.getProperties().icon, true));
            }
          });
        });
      }
    }
  });
};

export default {
  createPoilayer,
  poiExist,
  disablePoiById,
  removePoiById,
  setPoiVisibility,
  fetchPoi,
  addPoisToMap,
  showSinglePoi,
  setPoiFeatureVisibility
};
