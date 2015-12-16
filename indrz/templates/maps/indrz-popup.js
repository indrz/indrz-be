var popup = new ol.Overlay({
    element: document.getElementById('indrz-popup')
});
map.addOverlay(popup);

map.on('click', function (evt) {
    var element = popup.getElement();
    var coordinate = evt.coordinate;
    var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

    $(element).popover('destroy');
    popup.setPosition(coordinate);
// the keys are quoted to prevent renaming in ADVANCED mode.
    $(element).popover({
        'placement': 'top',
        'animation': false,
        'html': true,
        'content': '<p>Coordinate:</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i> Bug report</a>  </p> '
    });
    $(element).popover('show');
});
