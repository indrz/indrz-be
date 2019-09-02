var indrzMarkerVectorLayer = new ol.layer.Vector({ source: new ol.source.Vector(), zIndex:8 });
map.getLayers().push(indrzMarkerVectorLayer);

// var pin_icon = '//cdn.rawgit.com/jonataswalker/ol3-contextmenu/master/examples/img/pin_drop.png';
// var center_icon = '//cdn.rawgit.com/jonataswalker/ol3-contextmenu/master/examples/img/center.png';
// var list_icon = '//cdn.rawgit.com/jonataswalker/ol3-contextmenu/master/examples/img/view_list.png';

var indrz_contextmenu_items = [
  {
    text: 'Route FROM here',
    classname: 'bold',
    icon: '/static/homepage/img/contextmenu-start-marker.png',
    callback: setStartCoord
  },
      {
    text: 'Route TO here',
    classname: 'bold',
    icon: '/static/homepage/img/contextmenu-end-marker.png',
    callback: setEndCoord
  },
      {
    text: 'Clear Route',
    classname: 'bold',
    icon: '/static/homepage/img/contextmenu-clear-marker.png',
    callback: contextClearRoute
  },

  {
    text: 'Center map here',
    classname: 'bold',
    icon: "/static/homepage/img/contextmenu-center-map.png",
    callback: center
  },
  {
    text: 'Add a Marker',
    icon: "/static/homepage/img/contextmenu-add-marker.png",
    callback: marker
  },
          {
    text: 'Remove Markers',
    classname: 'bold',
    icon: '/static/homepage/img/contextmenu-remove-markers.png',
    callback: removeAllContextMarkers
  }


];

var indrzcontextmenu = new ContextMenu({
  width: 180,
  items: indrz_contextmenu_items
});

map.addControl(indrzcontextmenu);

var removeMarkerItem = {
  text: 'Remove this Marker',
  classname: 'marker',
  callback: removeMarker
};



indrzcontextmenu.on('open', function (evt) {

  var feature =	map.forEachFeatureAtPixel(evt.pixel, function(ft){return ft});
  
  if (feature && feature.get('type') === 'removable') {
    indrzcontextmenu.clear();
    removeMarkerItem.data = { marker: feature };
    indrzcontextmenu.push(removeMarkerItem);
  } else {
    indrzcontextmenu.clear();
    indrzcontextmenu.extend(indrz_contextmenu_items);
    indrzcontextmenu.extend(indrzcontextmenu.getDefaultItems());
  }
});

map.on('pointermove', function (e) {
  if (e.dragging) return;

  var pixel = map.getEventPixel(e.originalEvent);
  var hit = map.hasFeatureAtPixel(pixel);

  map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});


function center(obj) {
  view.animate({
    duration: 700,
    center: obj.coordinate
  });
}

var startCoord, endCoord;

function setStartCoord(obj) {
  globalRouteInfo.startName = obj.coordinate;
  globalRouteInfo.startCoord = obj.coordinate;
  globalRouteInfo.startFloor = active_floor_num;
  var feature = new ol.Feature({
        type: 'removable',
        geometry: new ol.geom.Point(obj.coordinate),
          zIndex:100
      });

  feature.setStyle([fa_circle_solid_style,fa_flag_solid_style]);
  indrzMarkerVectorLayer.getSource().addFeature(feature);
  $("#route-from").val(globalRouteInfo.startCoord + "," + active_floor_num );
  $('#collapseRouting').collapse('show');

}

function setEndCoord(obj) {
    indrzMarkerVectorLayer.getSource().clear();
    if (routeLayer) {
        map.removeLayer(routeLayer);
        // map.removeLayer(markerLayer);
        clearRouteDescription();
        //map.getLayers().pop();
    }


    globalRouteInfo.endCoord = obj.coordinate;
    globalRouteInfo.endFloor = active_floor_num;
    globalRouteInfo.endName = obj.coordinate;
    globalRouteInfo.routeUrl =  hostUrl + req_locale + "/?start-xyz=" + globalRouteInfo.startCoord + "," +
                                globalRouteInfo.startFloor + "&end-xyz=" + globalRouteInfo.endCoord + "," +
                                globalRouteInfo.endFloor;

    if (globalRouteInfo.startCoord !== undefined) {
        getDirections2(globalRouteInfo.startCoord + "," + globalRouteInfo.startFloor, obj.coordinate + "," + active_floor_num, "0", "coords");
    }

    $("#clearRoute").removeClass("hide");
    $("#shareRoute").removeClass("hide");
    $("#routeText").removeClass("hide");

    // $("#route-from").val(globalRouteInfo.startCoord);
    $("#route-to").val(obj.coordinate + "," + active_floor_num );

    $('#collapseRouting').collapse('show');
    $('#collapsePoi').collapse('hide');

}

function removeMarker(obj) {
  indrzMarkerVectorLayer.getSource().removeFeature(obj.data.marker);
}

function removeAllContextMarkers(obj) {
  indrzMarkerVectorLayer.getSource().clear();
}

function marker(obj) {


  var coord4326 = ol.proj.transform(obj.coordinate, 'EPSG:3857', 'EPSG:4326'),
      coord3857 = obj.coordinate,
      template = '({x} | {y})/\n',
      iconStyle = new ol.style.Style({
        image: new ol.style.Icon({ scale: .6, src: "/static/homepage/img/other.png" }),
        text: new ol.style.Text({
          offsetY: -20,
          text: "WGS84 " + ol.coordinate.format(coord4326, template, 4) + "EPSG:3857 " + ol.coordinate.format(coord3857, template, 4),
          font: '15px Open Sans,sans-serif',
          fill: new ol.style.Fill({ color: '#111' }),
          stroke: new ol.style.Stroke({ color: '#eee', width: 2 })
        })
      }),
      feature = new ol.Feature({
        type: 'removable',
        geometry: new ol.geom.Point(obj.coordinate)
      });

  feature.setStyle(iconStyle);
  indrzMarkerVectorLayer.getSource().addFeature(feature);
}

function contextClearRoute(){
        if (routeLayer) {
        map.removeLayer(routeLayer);
        // map.removeLayer(markerLayer);
        clearRouteDescription();
        //map.getLayers().pop();
    }


}
