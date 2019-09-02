var route_marker_A_style = new ol.style.Style({
  image: new ol.style.Icon({
    src: '/static/homepage/img/route_marker_A.png',
    anchor: [0.5, 1]
  }),
  zIndex: 6
})
var route_marker_B_style = new ol.style.Style({
  image: new ol.style.Icon({
    src: '/static/homepage/img/route_marker_B.png',
    anchor: [0.5, 1]
  }),
  zIndex: 6
})

var book_arrow_style = new ol.style.Style({
  text: new ol.style.Text({
    text: '\uf0a9', // blue circle arrow
    scale: 3,
    // font: 'normal 18px FontAwesome',
    font: '18px Font Awesome\ 5 Free',
    textBaseline: 'Bottom',
    rotateWithView: true,
    fill: new ol.style.Fill({color: 'blue'})
  })
})

var book_street_view_style = new ol.style.Style({
  text: new ol.style.Text({
    // text: "\uf05b", // cross hair
    text: '\uf21d', // street-map icon of user position
    scale: 2,
    font: 'normal 18px FontAwesome',
    // textBaseline: 'bottom',
    // placement: 'point 15 15',
    offsety: -30,
    offsetx: -10,
    fill: new ol.style.Fill({color: 'yellow'})
  })
})

var fa_flag_checkered_style = new ol.style.Style({
  text: new ol.style.Text({
    text: '\uf11e', // fas flag-checkered
    scale: 1,
    font: 'normal 18px FontAwesome',
    offsety: -30,
    offsetx: -10,
    fill: new ol.style.Fill({color: 'black'})
  })
})

var fa_flag_solid_style = new ol.style.Style({
  text: new ol.style.Text({
    text: '\uf024', // fas flag solid
    scale: 1,
    font: 'normal 18px FontAwesome',
    offsety: -30,
    offsetx: -10,
    fill: new ol.style.Fill({color: 'black'}),
    placement: "point",
    // backgroundFill: new ol.style.Fill({color:"white"}),
  })
})

var fa_circle_solid_style = new ol.style.Style({
  text: new ol.style.Text({
    text: '\uf111', // fas circle
    scale: 2,
    font: 'normal 18px FontAwesome',
    offsety: -30,
    offsetx: -10,
    fill: new ol.style.Fill({color: 'red'})
  })
})



var book_location_style = [book_arrow_style, book_street_view_style]

var route_marker_C_style = new ol.style.Style({
  image: new ol.style.Icon({
    src: '/static/homepage/img/route_marker_C.png',
    anchor: [0.5, 1]
  }),
  zIndex: 6
})

var route_active_style = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'red',
    width: 4
  }),
  zIndex: 6
})

var route_inactive_style = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'red',
    width: 2,
    lineDash: [0.1, 5],
    opacity: 0.5
  }),
  zIndex: 6
})

function clearRouteDescription () {

  $('#RouteDescription').remove()

  if (markerLayer) {
    map.removeLayer(markerLayer)
  }

}

function clearRouteData () {

  globalRouteInfo = {"routeUrl": null,"endSpaceId": null, "startSpaceId": null, "endPoiId": null,
    "startPoiId": null, "bookUrl": null, "startCoord": null, "endCoord": null};

  $('#RouteDescription').remove()

  if (bookLocationMarkerExact) {
    map.removeLayer(bookLocationMarkerExact)
  }

  if (routeLayer) {
    map.removeLayer(routeLayer)
  }
  if (markerLayer) {
    map.removeLayer(markerLayer)
  }
  if (routeNearestPoiLayer) {
    map.removeLayer(routeNearestPoiLayer)
  }

  if (libraryRouteLayer) {
    map.removeLayer(libraryRouteLayer)
    map.removeLayer(libraryMarkerLayer)
  }

  // for some reason the library route and markers aren't getting cleaned so we're doing this old school
  map.getLayers().forEach(function (layer) {
    if (layer) {
      // console.log(layer.get('name'));
      if (
        layer.get('name') !== undefined
        && (
          layer.get('name') === 'RouteToBook'
          || layer.get('name') === 'RouteLibraryMarkers'
          || layer.get('name') === 'RouteMarkers'
        )
      ) {
        // console.warn('removing layer'+ layer.get('name'));
        map.removeLayer(layer)
      }
    }
  })
}

function libraryMarker (location) {

  // location = [0, 0];
  // console.log(location)

  var iconFeature = new ol.Feature({
    geometry: new ol.geom.Point(location),
    name: 'Null Island',
    population: 4000,
    rainfall: 500
  })

  iconFeature.setStyle(book_street_view_style)

  var vectorSource = new ol.source.Vector({
    features: [iconFeature]
  })

  bookLocationMarkerExact = new ol.layer.Vector({
    source: vectorSource,
    layer_id: 20099,
    zIndex: 7
  })

  // map.getLayers().push(book_location_layer)

  map.addLayer(bookLocationMarkerExact)

}

function insertRouteDescriptionText (startSearchText, endSearchText, routeData, frontOffice) {

  $('#RouteDescription').remove()

  var ulList = '<ul id="RouteDescription" class="list-group"> </ul>'

  var routeTime = routeData.route_info.walk_time

  var minutes = Math.floor(routeTime / 60)
  var seconds = routeTime - minutes * 60
  var mins = gettext('minutes')
  var secs = gettext('seconds')
  var walkTimeString = minutes + ' ' + mins + ' ' + Math.floor(seconds) + ' ' + secs
  $('#routeTextContainer').append(ulList)

  if (frontOffice) {
    if (routeData.route_info.mid_name !== '') {
      var routeMidPointName = routeData.route_info.mid_name
      if (req_locale === 'de') {
        var x = gettext('Please first visit the ') + 'Front Office von ' + routeMidPointName

      } else {
        var x = gettext('Please first visit the ') + routeMidPointName + ' ' + gettext('front office')
      }

      $('#RouteDescription').append('<li class="list-group-item"><b>' + gettext('Start: ') + '</b>' + startSearchText + '</li><li class="list-group-item">' + x + '</li><li class="list-group-item"><b>' + gettext('Destination: ') + '</b>' + endSearchText + '</li><li class="list-group-item"><b> ' + gettext('Aprox. distance: ') + '</b>' + routeData.route_info.route_length + ' m</li>' +
        '<li class="list-group-item"><b>' + gettext('Aprox. walk time: ') + '</b>' + walkTimeString + '</li>')
    }

  } else {

    if (startSearchText) {

      $('#RouteDescription').append('<li class="list-group-item"><b>' + gettext('Start: ') + '</b>' + startSearchText + '</li><li class="list-group-item"><b>' + gettext('Destination: ') + '</b>' + endSearchText + '</li><li class="list-group-item"><b> ' + gettext('Aprox. distance: ') + '</b>' + routeData.route_info.route_length + ' m</li>' +
        '<li class="list-group-item"><b>' + gettext('Aprox. walk time: ') + '</b>' + walkTimeString + '</li>')

    } else {
      startSearchText = routeData.route_info.start_name
      endSearchText = routeData.route_info.end_name

      $('#RouteDescription').append('<li class="list-group-item"><b>' + gettext('Start: ') + '</b>' + startSearchText + '</li><li class="list-group-item"><b>' + gettext('Destination: ') + '</b>' + endSearchText + '</li><li class="list-group-item"><b> ' + gettext('Aprox. distance: ') + '</b>' + routeData.route_info.route_length + ' m</li>' +
        '<li class="list-group-item"><b>' + gettext('Aprox. walk time: ') + '</b>' + walkTimeString + '</li>')
    }

  }

}

function routeToPoiFromPoi (startPoiId, endPoiId) {

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

}




function routePoiToPoi(startPoiId, endPoiId){

}

function routeSpaceToSpace(startSpaceId, endSpaceId, direction, routeType){

  geoJsonUrl = baseApiRoutingUrl + 'startid=' + startSpaceId + '&' + 'endid=' + endSpaceId + '&type=' + routeType + '/?format=json'


}

function routeFromToXyz(startXyz, endXyz, direction, routeType){


}

function routePoiSpace(poiId, spaceId, direction, routeType){
  // route from poi-id to space id OR
  // route from space-id to poi-id
  // direction sets which is start and which is end

  if (direction === 'poi'){
    // route TO poi-id FROM space-id
  }else if (direction === 'space'){
    // route TO space-id FROM poi-id
  }else{
    console.log("error", "  no direction provided")
  }

  //
}

function routePoiXyz2(poiId, xyz, direction, routeType){

  if (direction === 'poi'){
    // route TO poi-id FROM xyz
  }else if (direction === 'xyz'){
    // route TO xyz FROM poi-id
  }else{
    console.log("error", "  no direction provided")
  }

}

function routeSpaceXyz(spaceId, xyz, direction, routeType){
  // route from poi-id to space id OR
  // route from space-id to poi-id
  // direction sets which is start and which is end

  if (direction === 'space'){
    // route TO space-id FROM xyz
  }else if (direction === 'xyz'){
    // route TO xyz from space-id
  }else{
    console.log("error", "  no direction provided")
  }

  //
}


var directionsOptions = ['poi2poi', 'poi2xyz', 'poi2space', 'space2space', 'space2poi', 'space2xyz',
                         'xyz2xyz', 'xyz2poi', 'xyz2space']



// valid startSearchText string is 21315.12,12312.123,3   x,y,floor_num
function getDirections2 (startSearchText, endSearchText, routeType, searchType, attributes) {

  route_type = routeType

  clearRouteData()

  var defaultAttributes = {
    reversed: false,
    start: {
      name: ''
    },
    end: {
      name: ''
    }
  }

  attributes = $.extend(defaultAttributes, attributes)

  var startName = attributes.end.name
  var endName = attributes.start.name

  // if(markerLayer){
  //     map.removeLayer(markerLayer);
  // }

  // if (routeNearestPoiLayer){
  //     map.removeLayer(routeNearestPoiLayer);
  // }

  // attributes = attributes || 0;
  // console.log(attributes);

  var geoJsonUrl = ''

  if (searchType === 'coords') {
    geoJsonUrl = baseApiRoutingUrl + startSearchText + '&' + endSearchText + '&' + routeType + '/?format=json'
  } else if (searchType === 'string') {
    geoJsonUrl = baseApiRoutingUrl + 'startstr=' + startSearchText + '&' + 'endstr=' + endSearchText + '&type=' + routeType + '/?format=json'
  } else if (searchType === 'poiToCoords') {
    geoJsonUrl = baseApiRoutingUrl + 'poi-id=' + startSearchText + '&' + 'xyz=' + endSearchText + '&reversed=' + attributes.reversed + '/?format=json'
  } else if (searchType === 'spaceIdToPoiId') {
    geoJsonUrl = baseApiRoutingUrl + 'space-id=' + startSearchText + '&' + 'poi-id=' + endSearchText + '&type=' + routeType + '/?format=json'
  } else if (searchType === 'spaceIdToSpaceId') {
    geoJsonUrl = baseApiRoutingUrl + 'startid=' + startSearchText + '&' + 'endid=' + endSearchText + '&type=' + routeType + '/?format=json'
  }


  var source = new ol.source.Vector()

 indrzApiCall(geoJsonUrl).then(function (response) {
    //console.log("response", response);
    var geojsonFormat = new ol.format.GeoJSON()
    var features = geojsonFormat.readFeatures(response,
      {featureProjection: 'EPSG:4326'})
    source.addFeatures(features)

    var routeJson = JSON.stringify(response)

    var routeData = JSON.parse(routeJson)

    // routeStartName = routeData.route_info.start_name;
    // routeEndName = routeData.route_info.end_name;
    // routeMidName = routeData.route_info.mid_name;

    // document.getElementById('route-to').value = endName;
    // document.getElementById('route-from').value = start Name;

    var route_markers_data = routeData.route_info.route_markers
    temp_route_data.test = routeData.route_info

    // globalRouteInfo.startName = startName;
    // globalRouteInfo.endName = endName;

    if (routeData.route_info.mid_name !== '') {
      insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, true)
    } else {
      insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, false)
    }

    addMarkers(features, routeData.route_info)

    if (searchType === 'coords') {

      startName = routeData.route_info.start_name
      endName = routeData.route_info.end_name
    }else if ( searchType === "spaceIdToSpaceId"){

      startName = routeData.route_info.start_name
      endName = routeData.route_info.end_name
      globalRouteInfo.routeUrl = "/?campus=1&start-spaceid=" + startSearchText + "&end-spaceid=" + endSearchText + "&type=" + routeType
      globalRouteInfo.startSpaceId =  startSearchText;
      globalRouteInfo.endSpaceId =  endSearchText;

      $('#route-from').val(startName)
      $('#route-to').val(endName)
      $('#collapseRouting').collapse('show')
      $('#collapsePoi').collapse('hide')
      $('#collapseCampus').collapse('hide')
      insertRouteDescriptionText(startName, endName, routeData, true)


    } else {
      startName = startSearchText
      endName = endSearchText

    }

    var start_floor = 0
    // active the floor of the start point
    if (typeof(features[0]) !== 'undefined') {
      start_floor = features[0].getProperties().floor
    }

    if (library_key !== 'nokey') {
      start_floor = routeLocalData.end.floor
    }

    for (var i = 0; i < floor_layers.length; i++) {
      if (start_floor == floor_layers[i].floor_num) {
        activateLayer(i)
      }
    }

    // center up the route
    var extent = source.getExtent()
    map.getView().fit(extent)

    // globalRouteInfo.startPoiId = 'noid'
    // globalRouteInfo.endPoiId = 'noid'
    // globalRouteInfo.routeUrl = "/?campus=" + building_id + "&startstr=" + startName + "&endstr=" + endName;

    // typeof NaN === 'number'; // Despite being "Not-A-Number"
    var checkName = Number(startName[0]) // should return NaN  if not a coordinate

    if (checkName > 0) {
      globalRouteInfo.routeUrl = '/?campus=' + building_id + '&start-xyz=' + startName + '&end-xyz=' + endName

    } else if (typeof checkName !== 'number' && startName !== '' && endName !== '') {
      globalRouteInfo.routeUrl = '/?campus=' + building_id + '&startstr=' + startName + '&endstr=' + endName + '&type=' + route_type

    }

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
    title: 'RouteFromSearch',
    name: 'RouteFromSearch',
    visible: true,
    layer_id: 20090,
    zIndex: 4
  })

  map.getLayers().push(routeLayer)

  $('#clearRoute').removeClass('hide')
  $('#shareRoute').removeClass('hide')
  $('#routeText').removeClass('hide')
  // $("#RouteDescription").removeClass("hide");

  window.location.href = '#map'

  $('html,body').animate({
      scrollTop: $('#map').offset().top
    },
    'slow')

}

function indrzMoveLayerBefore (old_idx, new_idx) {
  var layer = map.getLayers().removeAt(old_idx)
  map.getLayers().insertAt(new_idx, layer)
}

function indrzFindLayer (layer_id) {
  var layer_idx = -1
  $.each(map.getLayers().getArray(), function (k, v) {
    var this_layer_id = v.get('layer_id')
    if (this_layer_id == layer_id) {
      layer_idx = k
    }
  })
  return layer_idx
}

// usage
// indrzMoveLayerBefore(findLayer(44), findLayer(22));

$('#clearRoute').click(function () {

  if (bookLocationMarkerExact) {
    map.removeLayer(bookLocationMarkerExact)
  }

  if (routeLayer) {
    map.removeLayer(routeLayer)
    clearRouteDescription()
  }

  if (markerLayer) {
    map.removeLayer(markerLayer)
  }

  if (routeNearestPoiLayer) {
    map.removeLayer(routeNearestPoiLayer)
  }

  $('#clearRoute').addClass('hide')
  $('#shareRoute').addClass('hide')
  $('#routeText').addClass('hide')
  $('#route-to').val('')
  $('#route-from').val('')

  globalRouteInfo = {}
  globalPopupInfo.poiId = 'noid'

  clearAllRoutes()

  history.pushState({'bill': 'foo'}, 'live_url_update', '/' + req_locale + '/')
})

function createEntranceMarkers (route_features) {

  if (entranceMarkerLayer) {
    map.removeLayer(entranceMarkerLayer)
  }

  var marker_features = []
  var entranceList = []
  var entranceList2 = []
  var entranceLocation = {}
  var networkType = 99
  var prevFloorNum = -99
  var index = -1
  var nFeatures = route_features.length
  var distance = 0

  for (var i = 0; i < nFeatures; i++) {
    var cur_type = route_features[i].getProperties().network_type

    entranceLocation.geo = route_features[i].getGeometry()

    if (networkType != cur_type) {
      entranceList2.push(cur_type)

      if (cur_type === 4) {
        // entranceList.push(route_features[i].getGeometry());
        entranceList.push(route_features[i].getGeometry())
      }

      networkType = cur_type
      if (networkType === 4 || networkType === 9) {
        // entranceList.push(route_features[i].getGeometry());

        entranceLocation.geom = route_features[i].getGeometry()
        var entrance_coord = entranceLocation.geom.getLastCoordinate()
      }

    }
  }

  entranceCoordinates = []

  entranceCoordinates.push(entranceList[0].getFirstCoordinate())
  entranceCoordinates.push(entranceList.slice(-1)[0].getLastCoordinate())

  var entrance1 = entranceList[0].getFirstCoordinate()
  var entrance2 = entranceList.slice(-1)[0].getLastCoordinate()

  index = 0
  for (i = 0; i < nFeatures; i++) {
    var floor_num = route_features[i].getProperties().floor

    if (floorList[index] == floor_num)
      distance += route_features[i].getGeometry().getLength()
    if (floorList[index] == floor_num && lengthList[index] / 2 < distance) {

      var entrancePoint = new ol.geom.Point(entrance1)
      var entrancePoint2 = new ol.geom.Point(entrance2)
      //var entrancePoint = new ol.geom.Point(entranceLocation.geom.getLastCoordinate());

      var entranceFeature = new ol.Feature({
        geometry: entrancePoint
      })

      var entranceFeature2 = new ol.Feature({
        geometry: entrancePoint2
      })

      var entrance_style = new ol.style.Style({
        image: new ol.style.Icon({
          src: '/static/homepage/img/access_entrance_entrance.png'
        })
      })

      entranceFeature.setStyle(entrance_style)
      entranceFeature2.setStyle(entrance_style)

      //marker_features.push(entranceFeature);
      marker_features.push(entranceFeature2)

    }

  }

  var entranceMarkerLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: marker_features
    }),
    title: 'entranceMarker',
    name: 'entranceMarker',
    visible: true,
    layer_id: 10010,
    zIndex: 5
  })
  // map.getLayers().push(entranceMarkerLayePOIr);

  return entranceMarkerLayer

}

function addSimpleMarkers (route_features, r_info) {

  var marker_features = []
  var lengthList = []
  var floorList = []
  var entranceList = []
  var entranceList2 = []
  var entranceLocation = {}
  var networkType = 99
  var prevFloorNum = -99
  var index = -1
  var nFeatures = route_features.length
  var distance = 0

  if (nFeatures == 0) return
  // add middle icons
  for (var i = 0; i < nFeatures; i++) {
    var floor_num = route_features[i].getProperties().floor
    if (prevFloorNum != floor_num) {
      floorList.push(floor_num)
      index++
      prevFloorNum = floor_num
      if (!lengthList[index]) lengthList[index] = 0
    }
    lengthList[index] += route_features[i].getGeometry().getLength()
  }

  index = 0
  for (i = 0; i < nFeatures; i++) {
    var floor_num = route_features[i].getProperties().floor

    if (floorList[index] === floor_num)
      distance += route_features[i].getGeometry().getLength()
    if (floorList[index] === floor_num && lengthList[index] / 2 < distance) {
      var line_extent = route_features[i].getGeometry().getExtent()
      var middleCoordinate = ol.extent.getCenter(line_extent)
      var middlePoint = new ol.geom.Point(route_features[i].getGeometry().getClosestPoint(middleCoordinate))
      var middleFeature = new ol.Feature({
        geometry: middlePoint
      })
      var floor_num_style = new ol.style.Style({
        image: new ol.style.Icon({
          src: '/static/img/route_floor_' + floor_num + '.png'
        })
      })
      middleFeature.setStyle(floor_num_style)
      marker_features.push(middleFeature)

      index++
      distance = 0
    }

  }

  var start_point = new ol.geom.Point(route_features[0].getGeometry().getFirstCoordinate())
  var end_point = new ol.geom.Point(route_features[route_features.length - 1].getGeometry().getFirstCoordinate())

  if (r_info.hasOwnProperty('route_markers')) {

    var mrks = r_info.route_markers
    var mid

    for (i = 0; i < mrks.length; i++) {
      if (mrks[i].properties.hasOwnProperty('mid')) {
        // console.log("YES MID aavailable");
        mid = true
        var front_office_geo = new ol.geom.Point(mrks[i].geometry.coordinates)
        var frontOfficeMarker = new ol.Feature({
          geometry: front_office_geo
        })
        frontOfficeMarker.setStyle([fa_circle_solid_style,fa_flag_checkered_style])
        marker_features.push(frontOfficeMarker)

      }

      if (
        i === 0
        && mrks.length > 1
      ) {
        if (
          mrks[i].geometry
          && mrks[i].geometry.coordinates
          && mrks[i].geometry.coordinates.length > 1
        ) {
          end_point = new ol.geom.Point(mrks[i].geometry.coordinates)
        } else {
          end_point = new ol.geom.Point(mrks[i].geometry.coordinates[0])
        }
      }
    }

  }

  var startMarker = new ol.Feature({
    geometry: start_point
  })
console.log(start_point)
  startMarker.setStyle([fa_circle_solid_style,fa_flag_solid_style])

  var endMarker = new ol.Feature({
    geometry: end_point
  })
  endMarker.setGeometry(end_point)

  if (mid === true) {
    endMarker.setStyle(route_marker_C_style)

  } else {
    endMarker.setStyle([fa_circle_solid_style,fa_flag_checkered_style])

  }

  marker_features.push(startMarker)
  marker_features.push(endMarker)

  markerLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: marker_features
    }),
    title: 'RouteMarkers',
    name: 'RouteMarkers',
    visible: true,
    layer_id: 20020,
    zIndex: 6
  })

  // entranceMarkerLayer = createEntranceMarkers(route_features);
  // map.getLayers().push(entranceMarkerLayer);

  map.getLayers().push(markerLayer)
  //map.addLayer(markerLayer);
}




function addMarkers (route_features, r_info) {
  // console.log("hello", route_features, r_info)



  // if(markerLayer){
  //     map.removeLayer(markerLayer);
  // }

  var marker_features = []
  var lengthList = []
  var floorList = []
  var entranceList = []
  var entranceList2 = []
  var entranceLocation = {}
  var networkType = 99
  var prevFloorNum = -99
  var index = -1
  var nFeatures = route_features.length
  var distance = 0

  if (nFeatures === 0) return
  // add middle icons
  for (var i = 0; i < nFeatures; i++) {
    var floor_num = route_features[i].getProperties().floor
    if (prevFloorNum != floor_num) {
      floorList.push(floor_num)
      index++
      prevFloorNum = floor_num
      if (!lengthList[index]) lengthList[index] = 0
    }
    lengthList[index] += route_features[i].getGeometry().getLength()
  }

  index = 0
  for (i = 0; i < nFeatures; i++) {
    var floor_num = route_features[i].getProperties().floor

    if (floorList[index] === floor_num)
      distance += route_features[i].getGeometry().getLength()
    if (floorList[index] === floor_num && lengthList[index] / 2 < distance) {
      var line_extent = route_features[i].getGeometry().getExtent()
      var middleCoordinate = ol.extent.getCenter(line_extent)
      var middlePoint = new ol.geom.Point(route_features[i].getGeometry().getClosestPoint(middleCoordinate))

      var middleFeature = new ol.Feature({
        geometry: middlePoint
      })
      var floor_num_style = new ol.style.Style({
        image: new ol.style.Icon({
          src: '/static/img/route_floor_' + floor_num + '.png'
        })
      })

      middleFeature.setStyle(floor_num_style)
      marker_features.push(middleFeature)

      index++
      distance = 0
    }

  }

  var mid = false

  if (r_info) {


    if (r_info.hasOwnProperty('route_markers')) {

      ll = r_info.route_markers

      // front office marker aka mid route desitnation
      var front_office_geo = ''
      for (i = 0; i < ll.length; i++) {

        if ('mid' in ll[i].properties) {
          mid = true
          var front_office_geo

          if (ll[i].geometry.type === 'MultiPoint') {
            front_office_geo = new ol.geom.MultiPoint(ll[i].geometry.coordinates)

          } else if (ll[i].geometry.type === 'Point') {
            front_office_geo = new ol.geom.Point(ll[i].geometry.coordinates)

          }

          var frontOfficeMarker = new ol.Feature({
            geometry: front_office_geo
          })
          frontOfficeMarker.setStyle([fa_circle_solid_style,fa_flag_checkered_style])
          marker_features.push(frontOfficeMarker)

        }

        if ('start' in ll[i].properties) {
          var start_point

          if (ll[i].geometry.type === 'MultiPoint') {
            start_point = new ol.geom.MultiPoint(ll[i].geometry.coordinates)

          }
          if (ll[i].geometry.type === 'Point') {
            start_point = new ol.geom.Point(ll[i].geometry.coordinates)

          }

          var startMarker = new ol.Feature({
            geometry: start_point
          })

          // startMarker.setGeometry(start_point);
          startMarker.setStyle([fa_circle_solid_style,fa_flag_solid_style])
          marker_features.push(startMarker)
          //
        }

        if ('end' in ll[i].properties) {

          if (ll[i].geometry.type === 'MultiPoint') {
            var end_point = new ol.geom.MultiPoint(ll[i].geometry.coordinates)

          }
          if (ll[i].geometry.type === 'Point') {
            var end_point = new ol.geom.Point(ll[i].geometry.coordinates)

          }

          var endMarker = new ol.Feature({
            geometry: end_point
          })

          endMarker.setGeometry(end_point)
          marker_features.push(endMarker)
          //

          if (mid === true) {
            endMarker.setStyle(route_marker_C_style)

          } else {
            endMarker.setStyle([fa_circle_solid_style,fa_flag_checkered_style])

          }
        }

      }

    } else {
      var start_point = new ol.geom.Point(route_features[0].getGeometry().getFirstCoordinate())
      var end_point = new ol.geom.Point(route_features[route_features.length - 1].getGeometry().getLastCoordinate())

      var startMarker = new ol.Feature({
        geometry: start_point
      })
      startMarker.setStyle([fa_circle_solid_style,fa_flag_solid_style])

      var endMarker = new ol.Feature({
        geometry: end_point
      })
      endMarker.setGeometry(end_point)
      endMarker.setStyle([fa_circle_solid_style,fa_flag_checkered_style])

      marker_features.push(startMarker)
      marker_features.push(endMarker)

    }

  }

  markerLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: marker_features
    }),
    title: 'RouteMarkers',
    name: 'RouteMarkers',
    visible: true,
    layer_id: 20020,
    zIndex: 6
  })

  // entranceMarkerLayer = createEntranceMarkers(route_features);
  // map.getLayers().push(entranceMarkerLayer);

  // map.addLayer(markerLayer);
  map.getLayers().push(markerLayer)
}

var nearestPoi = function (coords, floorNum, poiId) {
  // coords = 1826748.9041401,6142337.0380243

  var urlPoi = hostUrl + req_locale + '/indrz/api/v1/directions/near/coords=' + coords + '&floor=' + floorNum + '&poiCatId=' + poiId + '/?format=json'

  // Assign handlers immediately after making the request,
  // and remember the jqxhr object for this request
  return indrzApiCall(urlPoi).done(function (data) {
      globalRouteInfo.nearestPoiName = data.name

    })
    .fail(function () {
      // console.log( "error" );
    })

}

var routePoiXyz = function (xyzCoords, floorNum, poiId, rev) {
  // route from a poi to xyz coordinate or visa versa   xyz to poi

  var defaultAttributes = {
    reversed: false,
    start: {
      name: ''
    },
    end: {
      name: ''
    }
  }

  // coords = 1826748.9041401,6142337.0380243

  var geoJsonUrl = baseApiRoutingUrl + 'poi-id=' + poiId + '&xyz=' + xyzCoords + '&floor=' + floorNum + '&reversed=' + rev + '/?format=json'

  clearAllRoutes()

  // http://localhost:8000/en/indrz/api/v1/directions/poi-id=27&xyz=1826685.08369146,6142499.125477515&floor=3&reversed=true

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

    // routeStartName = routeData.route_info.start_name;
    // routeEndName = routeData.route_info.end_name;
    // routeMidName = routeData.route_info.mid_name;

    startName = 'startname'
    endName = 'endname'

    // document.getElementById('route-to').value = endName;
    // document.getElementById('route-from').value = startName;

    var route_markers_data = routeData.route_info.route_markers
    temp_route_data.test = routeData.route_info

    // globalRouteInfo.startName = startName;
    // globalRouteInfo.endName = endName;

    if (routeData.route_info.mid_name !== '') {
      insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, true)
    } else {
      insertRouteDescriptionText(globalRouteInfo.startName, globalRouteInfo.endName, routeData, false)
    }

    addSimpleMarkers(features, routeData.route_info)

    var start_floor = 0
    // active the floor of the start point
    if (typeof(features[0]) !== 'undefined') {
      start_floor = features[0].getProperties().floor
    }

    if (library_key !== 'nokey') {
      start_floor = routeLocalData.end.floor
    }

    for (var i = 0; i < floor_layers.length; i++) {
      if (start_floor == floor_layers[i].floor_num) {
        activateLayer(i)
      }
    }

    // center up the route
    var extent = source.getExtent()
    map.getView().fit(extent)

    globalRouteInfo.poiStartId = 'noid'
    globalRouteInfo.poiEndId = 'noid'
    // globalRouteInfo.routeUrl = "/?campus=" + building_id + "&startstr=" + startName + "&endstr=" + endName;

    // typeof NaN === 'number'; // Despite being "Not-A-Number"
    var checkName = Number(startName[0]) // should return NaN  if not a coordinate

    if (checkName > 0) {
      globalRouteInfo.routeUrl = '/?campus=' + building_id + '&start-xyz=' + startName + '&end-xyz=' + endName

    } else if (typeof checkName !== 'number' && startName !== '' && endName !== '') {
      globalRouteInfo.routeUrl = '/?campus=' + building_id + '&startstr=' + startName + '&endstr=' + endName + '&type=' + route_type

    }

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
    title: 'RouteFromSearch',
    name: 'RouteFromSearch',
    visible: true,
    layer_id: 20090,
    zIndex: 4
  })

  map.getLayers().push(routeLayer)

  $('#clearRoute').removeClass('hide')
  $('#shareRoute').removeClass('hide')
  $('#routeText').removeClass('hide')
  // $("#RouteDescription").removeClass("hide");

  window.location.href = '#map'

  $('html,body').animate({
      scrollTop: $('#map').offset().top
    },
    'slow')

  // Assign handlers immediately after making the request,
  // and remember the jqxhr object for this request
  // return $.getJSON( geoJsonUrl, function(data) {
  //   // console.log( "success" );
  // })
  //   .done(function(data) {
  //       console.log(data);
  //
  //
  //
  //   })
  //   .fail(function() {
  //     // console.log( "error" );
  //   });

}

function routeToNearestPoi (startXY, floorNum, poiCatId, reversed, namePoiFrom, popupPoiId, triggerRoute) {

  if (triggerRoute === 'undefined') {
    triggerRoute = false
  }

  if (typeof globalPopupInfo.poiId === 'undefined' || globalPopupInfo.poiId === 'noid' ||
    globalPopupInfo.poiId === null && !triggerRoute || globalPopupInfo.spaceid) {

    console.log('we are in trouble')
    // route to string, bach api person, room, department see else below for if poi
    $.when(nearestPoi(startXY, floorNum, poiCatId)).then(function (b) {


      if (poiCatId === 71) {
        // route from popup TO the DEFI
        $('#route-to').val(b.name)

        globalRouteInfo.startPoiId = undefined
        globalRouteInfo.endPoiId = b.id
      } else {

        globalRouteInfo.startPoiId = b.id
        globalRouteInfo.endPoiId = undefined

        if (reversed === 'false') {
          $('#route-to').val(b.name)
        } else {
          $('#route-from').val(b.name)
        }
      }

      var routeStartValue = globalPopupInfo.coords[0] + ',' + globalPopupInfo.coords[1] + ',' + globalPopupInfo.floor

      globalRouteInfo.endName = b.name

      routeLocalData.end = {}
      routeLocalData.end.xcoord = b.geometry[0]
      routeLocalData.end.ycoord = b.geometry[1]
      routeLocalData.end.floor = b.floor
      var routeEndValue = routeLocalData.end.xcoord + ',' + routeLocalData.end.ycoord + ',' + routeLocalData.end.floor

      globalRouteInfo.endName = b.name
      globalRouteInfo.coords = b.geometry

      // getDirections2(routeStartValue, routeEndValue,0, "coords");

      // searchLayer && globalPopupInfo.poid === 'noid'
      if (globalPopupInfo.src === 'external person api' || globalPopupInfo.src === 'bach rooms') {

        var search_features = searchLayer.getProperties().source.getFeatures()
        var len_searchRes = search_features.length

        if (len_searchRes >= 1) {

          for (i = 0; i < search_features.length; i++) {

            var props = search_features[i].getProperties()

            if (props.poi_id === current_poi_id || props.hasOwnProperty('poi_id')) {

              yes_poi = true
              // getDirections2(startXYFloor, endXYFloor, "0", "coords");
              break

            }

            if (props.name === globalPopupInfo.name) {

              if (reversed === 'true') {

                globalRouteInfo.startName = b.name
                globalRouteInfo.endName = search_features[i].getProperties().name
                getDirections2(b.name, search_features[i].getProperties().name, '0', 'string')

                // getDirections2(b.geometry + "," + b.floor, props.centerGeometry.coordinates + "," + props.floor_num, "0", "coords");

                break

              } else {

                console.log("opt2")
                globalRouteInfo.startName = search_features[i].getProperties().name
                globalRouteInfo.endName = b.name
                getDirections2(search_features[i].getProperties().name, b.name, '0', 'string')

                // getDirections2(props.centerGeometry.coordinates + "," + props.floor_num, b.geometry + "," + b.floor, "0", "coords");

                break
              }

              // getDirections2(b.geometry + "," + b.floor, props.centerGeometry.coordinates + "," + props.floor_num, "0", "coords");

            }

          }

        }

      }


      if (globalPopupInfo.spaceid) {
        console.log("opt3")

        if (globalPopupInfo.spaceid) {
          // getDirections2(globalPopupInfo.roomcode, b.name, "0", "string")
          getDirections2(globalPopupInfo.spaceid, b.id, '0', 'spaceIdToPoiId')
          globalRouteInfo.startPoiId = b.id;
          if(globalPopupInfo.spaceid){
            globalRouteInfo.endSpaceId = globalPopupInfo.spaceid;
          }


        } else {
          console.log("else this is hugalsdjf")
          $('#enterRoute').trigger('click')
        }

      } else {
        console.log("opt4")
        // only should fire if roomcode null and wms getinfo is source
        getDirections2(b.geometry + ',' + b.floor, globalPopupInfo.coords + ',' + globalPopupInfo.floor, '0', 'coords')

      }

    })

  } else {
    console.log("opt5")

    $.when(nearestPoi(startXY, floorNum, poiCatId)).then(function (b) {

      if (reversed === 'false') {
        $('#route-to').val(b.name)
        // routeToPoiFromPoi(globalPopupInfo.poiId, b.id);
        var endCoords = '' + b.geometry[0] + ',' + b.geometry[1] + '&floor=' + b.floor
        console.log("opt6")
        getDirections2(globalPopupInfo.poiId, endCoords, '0', 'poiToCoords')
        globalRouteInfo.routeUrl = hostUrl + req_locale + '/?start-poi-id=' + b.id + '&end-poi-id=' + globalPopupInfo.poiId

      } else {
        $('#route-from').val(b.name)
        console.log("opt7")
        routeToPoiFromPoi(b.id, globalPopupInfo.poiId)
        globalRouteInfo.routeUrl = hostUrl + req_locale + '/?start-poi-id=' + globalPopupInfo.poiId + '&end-poi-id=' + b.id
      }

    })

  }

}

function clearAllRoutes () {

  clearRouteDescription()

  globalRouteInfo = {"routeUrl": null,"endSpaceId": null, "startSpaceId": null, "endPoiId": null,
    "startPoiId": null, "bookUrl": null, "startCoord": null, "endCoord": null};

  if (routeLayerGroup.getLayers()) {

    routeLayerGroup.getLayers().forEach(function (layer) {
      map.removeLayer(layer)
    })

  }

  if (typeof libraryRouteLayer !== 'undefined') {
    map.removeLayer(libraryRouteLayer)
    map.removeLayer(libraryMarkerLayer)
  }

  [markerLayer, routeLayer, routeNearestPoiLayer].forEach(function (layer) {
    if (typeof layer !== 'undefined') {
      map.removeLayer(layer)
    }
  })

}