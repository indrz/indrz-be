import SourceVector from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { getCenter } from 'ol/extent';
import Point from 'ol/geom/Point';
import MultiPoint from 'ol/geom/MultiPoint';
import Feature from 'ol/Feature';
import GeoJSON from 'ol/format/GeoJSON';
import { Style, Stroke, Circle, Text, Fill } from 'ol/style';
import MapStyles from './mapStyles';
import MapUtil from './map';
import api from '~/util/api';
import config from '~/util/indrzConfig';

const { env } = config;

const routeGo = async (mapInfo, layers, globalRouteInfo, routeType = 0, env) => {
  let routeUrl = '';
  const { from, to } = globalRouteInfo;
  if (from.properties.space_id && to.properties.space_id && !to.properties.poiId) {
    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: from.properties.space_id,
        startFloor: from.properties.floor_num,
        endSearchText: to.properties.space_id,
        endFloor: to.properties.floor_num,
        routeType,
        searchType: 'spaceIdToSpaceId',
        foid: to.properties.frontoffice?.space_id
      }
    );
  } else if (from.properties.poiId && to.properties.poiId) {
    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: from.properties.poiId,
        startFloor: from.properties.floor_num,
        endSearchText: to.properties.poiId,
        endFloor: to.properties.floor_num,
        routeType,
        searchType: 'poiIdToPoiId'
      }
    );
  } else if (
    (from.properties.poiId && to.properties.space_id) ||
        (from.properties.space_id && to.properties.poiId)
  ) {
    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: (from.properties.space_id || to.properties.space_id),
        startFloor: from.properties.floor_num,
        endSearchText: (from.properties.poiId || to.properties.poiId),
        endFloor: to.properties.floor_num,
        routeType,
        searchType: 'spaceIdToPoiId',
        reversed: !(from.properties.space_id)
      }
    );
  } else if (
    (from.properties.shelfId && to.properties.coords) ||
        (from.properties.coords && to.properties.shelfId)) {
    const fromProperties = from.properties.shelfId ? from.properties : to.properties;
    const toProperties = to.properties.coords ? to.properties : from.properties;

    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: fromProperties,
        startFloor: fromProperties.floor_num,
        endSearchText: toProperties.coords,
        endFloor: toProperties.floor_num,
        routeType,
        searchType: 'bookToCoords'
      }
    );
  } else if (
    (from.properties.shelfId && to.properties.poiId) ||
        (from.properties.poiId && to.properties.shelfId)) {
    const fromProperties = from.properties.poiId ? from.properties : to.properties;
    const toProperties = to.properties.shelfId ? to.properties : from.properties;

    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: fromProperties.poiId,
        startFloor: fromProperties.floor_num,
        endSearchText: toProperties,
        endFloor: toProperties.floor_num,
        routeType,
        searchType: 'poiIdToBook'
      }
    );
  } else if (
    (from.properties.space_id && to.properties.shelfId) ||
        (from.properties.shelfId && to.properties.space_id)) {
    const fromProperties = from.properties.space_id ? from.properties : to.properties;
    const toProperties = to.properties.shelfId ? to.properties : from.properties;

    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: fromProperties.space_id,
        startFloor: fromProperties.floor_num,
        endSearchText: toProperties,
        endFloor: toProperties.floor_num,
        routeType,
        searchType: 'spaceIdToBook'
      }
    );
  } else if (from.properties.shelfId && to.properties.shelfId) {
    const fromProperties = from.properties;
    const toProperties = to.properties;

    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: fromProperties,
        startFloor: fromProperties.floor_num,
        endSearchText: toProperties,
        endFloor: toProperties.floor_num,
        routeType,
        searchType: 'bookToBook'
      }
    );
  } else if (
    (from.properties.coords && to.properties.poiId) ||
        (from.properties.poiId && to.properties.coords)
  ) {
    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: (from.properties.poiId || to.properties.poiId),
        startFloor: null,
        endSearchText: (from.properties.coords || to.properties.coords),
        endFloor: (from.properties.coords ? from.properties.floor_num : to.properties.floor_num),
        routeType,
        searchType: 'poiToCoords'
      }
    );
  } else if (
    (from.properties.coords && to.properties.space_id) ||
    (from.properties.space_id && to.properties.coords)
  ) {
    const fromProperties = from.properties.space_id ? from.properties : to.properties;
    const toProperties = to.properties.coords ? to.properties : from.properties;

    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: fromProperties.space_id,
        startFloor: fromProperties.floor_num,
        endSearchText: toProperties.coords,
        endFloor: toProperties.floor_num,
        routeType,
        searchType: 'spaceIdToCoords'
      }
    );
  } else if (from.properties.coords && to.properties.coords) {
    routeUrl = await getDirections(
      {
        mapInfo,
        layers,
        startSearchText: from.properties.coords,
        startFloor: from.properties.floor_num,
        endSearchText: to.properties.coords,
        endFloor: to.properties.floor_num,
        routeType,
        searchType: 'coords'
      }
    );
  } else {
    // setNoRouteFoundText();
    return {
      noRouteFound: true
    }
  }
  return routeUrl;
};

const clearRouteData = (map, includeAllLayers = false) => {
  const optionalLayers = [
    'RouteFromPoiToPoi'
  ];
  const defaultLayers = [
    'RouteToBook',
    'RouteLibraryMarkers',
    'RouteMarkers',
    'RouteFromSearch'
  ];
  const layerNamesToRemove = includeAllLayers ? defaultLayers.concat(optionalLayers) : defaultLayers;

  const layersToRemove = [];

  map.getLayers().forEach(function (layer) {
    if (layerNamesToRemove.includes(layer.get('name'))) {
      layersToRemove.push(layer);
    }
  });

  layersToRemove.forEach((layer) => {
    map.removeLayer(layer);
  });
};

const getNearestEntrance = async (globalPopupInfo) => {
  const url = `${env.BASE_API_URL}directions/near/coords=${globalPopupInfo.coords.join(',')}&floor=${globalPopupInfo.floor_num}&poiCatId=${env.NEAREST_ENTRANCE_POIID}/?format=json`;

  try {
    return await api.request({
      url
    }).then(function (response) {
      return Object.assign({ ...response.data, poiId: response.data.id });
    });
  } catch (err) {
    console.log(err);
  }
};

const getNearestMetro = async (globalPopupInfo) => {
  const url = `${env.BASE_API_URL}directions/near/coords=${globalPopupInfo.coords.join(',')}&floor=${globalPopupInfo.floor_num}&poiCatId=${env.NEAREST_METRO_POIID}/?format=json`;

  try {
    return await api.request({
      url
    }).then(function (response) {
      return Object.assign({ ...response.data, poiId: response.data.id });
    });
  } catch (err) {
    console.log(err);
  }
};

const getNearestDefi = async (globalPopupInfo) => {
  const url = `${env.BASE_API_URL}directions/near/coords=${globalPopupInfo.coords.join(',')}&floor=${globalPopupInfo.floor_num}&poiCatId=${env.NEAREST_DEFI_POIID}/?format=json`;

  try {
    return await api.request({
      url
    }).then(function (response) {
      return Object.assign({ ...response.data, poiId: response.data.id });
    });
  } catch (err) {
    console.log(err);
  }
};

const getDirections = async ({
  mapInfo,
  layers,
  startSearchText,
  startFloor,
  endSearchText,
  endFloor,
  routeType,
  searchType,
  foid,
  reversed = false
}) => {
  let geoJsonUrl = '';
  let routeUrl = '';

  const baseApiRoutingUrl = env.BASE_API_URL + 'directions/';
  const floatTypeStartFloor = Number(startFloor).toFixed(1);
  const floatTypeEndFloor = Number(endFloor).toFixed(1);
  const map = mapInfo.map;

  clearRouteData(map);

  switch (searchType) {
    case 'coords':
      geoJsonUrl = `${baseApiRoutingUrl}${startSearchText.join(',')},${startFloor}&${endSearchText.join(',')},${endFloor}`;
      break;
    case 'string':
      geoJsonUrl = `${baseApiRoutingUrl}startstr=${startSearchText}&endstr=${endSearchText}`;
      break;
    case 'poiToCoords':
      geoJsonUrl = `${baseApiRoutingUrl}poi=${startSearchText}&xyz=${endSearchText},${floatTypeEndFloor}`;
      break;
    case 'spaceIdToPoiId':
      geoJsonUrl = `${baseApiRoutingUrl}space=${startSearchText}&poi=${endSearchText}`;
      break;
    case 'spaceIdToSpaceId':
      geoJsonUrl = `${baseApiRoutingUrl}space=${startSearchText}&space=${endSearchText}`;
      if (foid) {
        geoJsonUrl += '&foid=' + foid;
      }
      break;
    case 'poiIdToPoiId':
      geoJsonUrl = `${baseApiRoutingUrl}poi=${startSearchText}&poi=${endSearchText}`;
      break;
    case 'spaceIdToBook':
      geoJsonUrl = `${baseApiRoutingUrl}space=${startSearchText}&xyz=${endSearchText.coords.join(',')},${floatTypeEndFloor}`;
      break;
    case 'bookToCoords':
      geoJsonUrl = `${baseApiRoutingUrl}start_xyz=${startSearchText.coords.join(',')},${floatTypeStartFloor}&end_xyz=${endSearchText},${floatTypeEndFloor}`;
      break;
    case 'poiIdToBook':
      geoJsonUrl = `${baseApiRoutingUrl}poi=${startSearchText}&xyz=${endSearchText.coords.join(',')},${floatTypeEndFloor}`;
      break;
    case 'bookToBook':
      geoJsonUrl = `${baseApiRoutingUrl}start_xyz=${startSearchText.coords.join(',')},${floatTypeStartFloor}&end_xyz=${endSearchText.coords.join(',')},${floatTypeEndFloor}`;
      break;
    case 'spaceIdToCoords':
      geoJsonUrl = `${baseApiRoutingUrl}space=${startSearchText}&xyz=${endSearchText},${floatTypeEndFloor}`;
      break;
    default:
      break;
  }
  if (reversed) {
    geoJsonUrl += `&reversed=${reversed}`
  }
  geoJsonUrl += `&type=${routeType}`;
  const source = new SourceVector();
  let floorNum = '';

  try {
    return await api.request({
      url: geoJsonUrl
    }, env).then(function (response) {
      if (!response) {
        return;
      }
      response = response.data;
      const geojsonFormat = new GeoJSON();
      const features = geojsonFormat.readFeatures(response, { featureProjection: 'EPSG:4326' });
      const routeJson = JSON.stringify(response);
      const routeData = JSON.parse(routeJson);
      const { route_info: routeInfo } = routeData;
      source.addFeatures(features);

      addMarkers(map, features, routeInfo);

      const frontOffice = mapInfo.globalRouteInfo.to.properties.frontoffice;

      if (frontOffice) {
        routeData.frontOffice = frontOffice;
      }

      if (routeInfo) {
        switch (searchType) {
          case 'coords':
            routeUrl = `?from-xy=${startSearchText.join(',')},${startFloor}&to-xy=${endSearchText.join(',')},${endFloor}`;
            break;
          case 'poiToCoords':
            routeUrl = '?from-poi=' + routeInfo.start.id + `&to-xy=${endSearchText.join(',')},${endFloor}`;
            break;
          case 'poiIdToPoiId':
            routeUrl = '?from-poi=' + routeInfo.start.id + '&to-poi=' + routeInfo.end.id;
            break;
          case 'spaceIdToPoiId':
            routeUrl = '?from-space=' + startSearchText + '&to-poi=' + endSearchText;
            break;
          case 'spaceIdToSpaceId':
            routeUrl = '?from-space=' + startSearchText + '&to-space=' + endSearchText;
            if (foid) {
              routeUrl += '&foid=' + foid;
            }
            break;
          case 'spaceIdToBook':
            routeUrl = '?from-space=' + startSearchText + '&to-book=' + endSearchText.key;
            break;
          case 'bookToCoords':
            routeUrl = '?from-book=' + startSearchText.key + `&to-xy=${endSearchText.join(',')},${floatTypeEndFloor}`;
            break;
          case 'poiIdToBook':
            routeUrl = `?from-poi=${startSearchText}&to-book=${endSearchText.key}`
            break;
          case 'bookToBook':
            routeUrl = '?from-book=' + startSearchText.key + '&to-book=' + endSearchText.key;
            break;
          case 'spaceIdToCoords':
            routeUrl = `?from-space=${startSearchText}&to-xy=${endSearchText.join(',')},${floatTypeEndFloor}`;
            break;
          default:
            break;
        }
      }
      if (reversed) {
        routeUrl += `&reversed=${reversed}`
      }
      routeUrl += `&type=${routeType}`;

      if (typeof (features[0]) !== 'undefined') {
        floorNum = features[0].getProperties().floor;

        if (floorNum) {
          mapInfo.$emit('selectFloor', features[0].getProperties().floor);
          MapUtil.activateLayer(env.LAYER_NAME_PREFIX + floorNum, layers.switchableLayers, map);
        }
      }

      const routeLayer = new VectorLayer({
        source: source,
        style: function (feature, resolution) {
          const featureFloor = Number(feature.getProperties().floor).toFixed(1);
          if (featureFloor === Number(floorNum).toFixed(1)) {
            feature.setStyle(MapStyles.routeActiveStyle);
          } else {
            feature.setStyle(MapStyles.routeInactiveStyle);
          }
        },
        title: 'RouteFromSearch',
        name: 'RouteFromSearch',
        visible: true,
        layer_id: 20090,
        zIndex: 4
      });

      map.getLayers().push(routeLayer);

      const extent = source.getExtent();
      map.getView().fit(extent);
      const curZoom = map.getView().getZoom();
      map.getView().setZoom(curZoom - 1);

      return {
        ...routeData.route_info,
        routeUrl
      };
    });
  } catch ({ response }) {
    if ((response && response.status === 404) || (response.data.error && response.data.error === 'no geometry')) {
      // setNoRouteFoundText();
      return {
        noRouteFound: true
      }
    } else {
      return { error: response.data.error };
    }
  }
};

const addMarkers = (map, routeFeatures, routeInfo) => {
  const markerFeatures = [];
  const lengthList = [];
  const floorList = [];
  const fontColor = '#158afc';
  let prevFloorNum = -99;
  let index = -1;
  const nFeatures = routeFeatures.length;
  let distance = 0;

  if (nFeatures === 0) {
    return;
  }
  // add middle icons
  for (let i = 0; i < nFeatures; i++) {
    const floorNumber = routeFeatures[i].getProperties().floor;
    if (prevFloorNum !== floorNumber) {
      floorList.push(floorNumber);
      index++;
      prevFloorNum = floorNumber;
      if (!lengthList[index]) {
        lengthList[index] = 0;
      }
    }
    lengthList[index] += routeFeatures[i].getGeometry().getLength();
  }

  index = 0;

  for (let i = 0; i < nFeatures; i++) {
    const floorNumber = routeFeatures[i].getProperties().floor;
    if (floorList[index] === floorNumber) {
      distance += routeFeatures[i].getGeometry().getLength();
    }
    if (floorList[index] === floorNumber && lengthList[index] / 2 < distance) {
      const lineExtent = routeFeatures[i].getGeometry().getExtent();
      const middleCoordinate = getCenter(lineExtent);
      const middlePoint = new Point(routeFeatures[i].getGeometry().getClosestPoint(middleCoordinate));
      const middleFeature = new Feature({
        geometry: middlePoint
      });

      const floorNumberStyle = new Style({
        image: new Circle({
          radius: 12,
          fill: new Fill({
            color: 'rgba(255, 255, 255, 0.8)'
          }),
          stroke: new Stroke({
            color: 'rgb(21,138,252, 0.8)',
            width: 3
          })
        }),
        text: new Text({
          font: '18px sans-serif',
          text: floorNumber.toString(),
          fill: new Fill({
            color: fontColor
          }),
          stroke: new Stroke({
            color: fontColor,
            width: 1
          })
        })
      });

      middleFeature.setStyle(floorNumberStyle);
      markerFeatures.push(middleFeature);

      index++;
      distance = 0;
    }
  }

  let mid = false;
  if (routeInfo) {
    if (routeInfo.hasOwnProperty('route_markers')) {
      const ll = routeInfo.route_markers;
      // front office marker aka mid route desitnation
      let frontOfficeGeometry = '';
      for (let i = 0; i < ll.length; i++) {
        if ('mid' in ll[i].properties) {
          mid = true;

          if (ll[i].geometry.type === 'MultiPoint') {
            frontOfficeGeometry = new MultiPoint(ll[i].geometry.coordinates);
          } else if (ll[i].geometry.type === 'Point') {
            frontOfficeGeometry = new Point(ll[i].geometry.coordinates);
          }
          const frontOfficeMarker = new Feature({
            geometry: frontOfficeGeometry
          });
          frontOfficeMarker.setStyle([MapStyles.faCircleSolidStyle, MapStyles.faFlagCheckeredStyle]);
          markerFeatures.push(frontOfficeMarker);
        }

        if ('start' in ll[i].properties) {
          let startPoint;

          if (ll[i].geometry.type === 'MultiPoint') {
            startPoint = new MultiPoint(ll[i].geometry.coordinates);
          }
          if (ll[i].geometry.type === 'Point') {
            startPoint = new Point(ll[i].geometry.coordinates);
          }
          const startMarker = new Feature({
            geometry: startPoint
          });
          startMarker.setStyle([MapStyles.routeMarkerCStyle]);
          markerFeatures.push(startMarker);
        }

        if ('end' in ll[i].properties) {
          let endPoint;
          if (ll[i].geometry.type === 'MultiPoint') {
            endPoint = new MultiPoint(ll[i].geometry.coordinates);
          }
          if (ll[i].geometry.type === 'Point') {
            endPoint = new Point(ll[i].geometry.coordinates);
          }
          const endMarker = new Feature({
            geometry: endPoint
          });

          endMarker.setGeometry(endPoint);
          markerFeatures.push(endMarker);

          if (mid === true) {
            endMarker.setStyle(MapStyles.routeMarkerCStyle);
          } else {
            endMarker.setStyle([MapStyles.faFlagCheckeredStyle]);
          }
        }
      }
    } else {
      const startPoint = new Point(routeFeatures[0].getGeometry().getLastCoordinate());
      const endPoint = new Point(routeFeatures[routeFeatures.length - 1].getGeometry().getLastCoordinate());
      const startMarker = new Feature({
        geometry: startPoint
      });
      const endMarker = new Feature({
        geometry: endPoint
      });
      // endMarker.setGeometry(endPoint);
      endMarker.setStyle([MapStyles.faFlagCheckeredStyle]);
      startMarker.setStyle([MapStyles.faCircleSolidStyle]);
      markerFeatures.push(startMarker);
      markerFeatures.push(endMarker);
    }
  }
  const markerLayer = new VectorLayer({
    source: new SourceVector({
      features: markerFeatures
    }),
    title: 'RouteMarkers',
    name: 'RouteMarkers',
    visible: true,
    layer_id: 20020,
    zIndex: 6
  });
  map.getLayers().push(markerLayer);
};

const routeToPoiFromPoi = (startPoiId, endPoiId) => {
  /*
      globalRouteInfo.startPoiId = startPoiId
      globalRouteInfo.endPoiId = endPoiId

      // http://localhost:8000/en/?start-poi-id=1049&end-poi-id=251
      globalRouteInfo.routeUrl = '?start-poi-id=' + startPoiId + '&end-poi-id=' + endPoiId

      geoJsonUrl = baseApiRoutingUrl + 'foo/start-poi-id=' + startPoiId + '&' + 'end-poi-id=' + endPoiId + '?format=json'

      if (routeLayer) {
        map.removeLayer(routeLayer)
        clearRouteDescription()

        //map.getLayers().pop();
      }

      var source = new ol.source.Vector()
      indrzApiCall(geoJsonUrl).then(function (response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON()
        var features = geojsonFormat.readFeatures(response,
          {featureProjection: 'EPSG:4326'})
        source.addFeatures(features)
        //
        //
        var routeJson = JSON.stringify(response)

        var routeData = JSON.parse(routeJson)

        var routeStartName = routeData.route_info.start_name
        var routeEndName = routeData.route_info.end_name
        var routeMidName = routeData.route_info.mid_name

        globalRouteInfo.startInfo = routeData.route_info.start
        globalRouteInfo.endInfo = routeData.route_info.end

        // startName = startPoiId;
        // endName = endPoiId;

        var startName = globalRouteInfo.startInfo.properties.name
        var endName = globalRouteInfo.endInfo.properties.name

        if (req_locale === 'de') {
          startName = globalRouteInfo.startInfo.properties.name_de
          endName = globalRouteInfo.endInfo.properties.name_de
        }

        globalRouteInfo.startName = startName
        globalRouteInfo.endName = endName

        var route_markers_data = routeData.route_info.route_markers
        temp_route_data.test = routeData.route_info

        if (routeData.route_info.mid_name !== '') {
          insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, true)
        } else {
          insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, false)
        }

        addMarkers(features, routeData.route_info)

        var start_floor = 0
        // active the floor of the start point
        if (typeof(features[0]) !== 'undefined') {
          start_floor = features[0].getProperties().floor
        }

        for (var i = 0; i < floor_layers.length; i++) {
          if (start_floor == floor_layers[i].floor_num) {
            activateLayer(i)
          }
        }

        // center up the route
        var extent = source.getExtent()
        map.getView().fit(extent)
      })

      routeLayer = new ol.layer.Vector({
        //url: geoJsonUrl,
        //format: new ol.format.GeoJSON(),
        source: source,
        style: function (feature, resolution) {
          var feature_floor = feature.getProperties().floor
          if (feature_floor == active_floor_num) {
            feature.setStyle(route_active_style)
          } else {
            feature.setStyle(route_inactive_style)
          }
        },
        title: 'RoutePoiToPoi',
        name: 'RoutePoiToPoi',
        visible: true,
        layer_id: 20070,
        zIndex: 4
      })

      map.getLayers().push(routeLayer)

      $('#clearRoute').removeClass('hide')
      $('#shareRoute').removeClass('hide')
      $('#routeText').removeClass('hide')
      $('#collapseRouting').collapse('show')
      $('#collapsePoi').collapse('hide')
      // $("#RouteDescription").removeClass("hide");

      window.location.href = '#map'

      $('html,body').animate({
          scrollTop: $('#map').offset().top
        },
        'slow')
    */
};

/* export default function (_store, _$t, _scope) {
  translate = _$t;
  scope = _scope;
 */
export default function (_store) {
  return {
    getDirections,
    getNearestEntrance,
    getNearestMetro,
    getNearestDefi,
    routeGo,
    routeToPoiFromPoi,
    clearRouteData
  };
}
