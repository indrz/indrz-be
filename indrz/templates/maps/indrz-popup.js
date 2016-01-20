var popup_container = document.getElementById('indrz-popup');
var popup_content = document.getElementById('popup-content');
var popup_closer = document.getElementById('popup-closer');

var selectRoom = new ol.interaction.Select();

/**
 * Create an overlay to anchor the popup to the map.
 */
var popup_overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
  element: popup_container,
  autoPan: true,
  autoPanAnimation: {
    duration: 250
  },
  zIndex: 99
}));

/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
popup_closer.onclick = function() {
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
  return false;
};

map.addOverlay(popup_overlay);

map.addInteraction(selectRoom);

map.on('singleclick', function (e) {
  map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
      if(feature.getGeometry().getType() == "MultiPolygon") {
          var coordinate = map.getCoordinateFromPixel(e.pixel);
          var properties = feature.getProperties();
          open_popup(properties, coordinate);
      }
  });
});

function open_popup(properties, coordinate){
  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
      coordinate, 'EPSG:3857', 'EPSG:4326'));
  popup_content.innerHTML = '<p>Building Name: ' + properties.fk_building.building_name + '</p>';
  popup_content.innerHTML += '<p>Floor Number: ' + properties.floor_num + '</p>';
  popup_content.innerHTML += '<p>Room Name: ' + properties.short_name + '</p>';
  popup_content.innerHTML += '<p>Coordinate:</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i> Bug report</a>  </p>';
  popup_overlay.setPosition(coordinate);
}
/*
map.on('singleclick', function(evt) {
  var coordinate = evt.coordinate;
  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

  popup_content.innerHTML = '<p>Coordinate:</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i> Bug report</a>  </p>';
  popup_overlay.setPosition(coordinate)
});

*/