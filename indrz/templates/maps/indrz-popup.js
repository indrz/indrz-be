var popup_container = document.getElementById('indrz-popup');
var popup_content = document.getElementById('popup-content');
var popup_closer = document.getElementById('popup-closer');

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


/**
 * Add a click handler to the map to render the popup.
 */
map.on('singleclick', function(evt) {
  var coordinate = evt.coordinate;
  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

  popup_content.innerHTML = '<p>Coordinate:</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i> Bug report</a>  </p>';
  popup_overlay.setPosition(coordinate)
});