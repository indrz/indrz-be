var map_type = true;

var full_screen_control = new ol.control.FullScreen({
    label: "Go Full Screen",
    className: "btn-fullscreen",
    target: document.getElementById("id-fullscreen")
});

// map.addControl(full_screen_control);

$("#id-map-switcher").on("click", function(evt){
    map_type = !map_type;
    if(map_type) {
        $(this).text('Satellite');
        ortho30cm_bmapat.setVisible(false);
        grey_bmapat.setVisible(true);
        // wmsOutdoorMap.setVisible(true);

        // setLayerVisible(1);

    } else {
        $(this).text('Map');
        ortho30cm_bmapat.setVisible(true);
        grey_bmapat.setVisible(false);
        // wmsOutdoorMap.setVisible(false);
        // hideLayers();
    }
});

var panToCampus = document.getElementById('id-zoom-to-campus')

panToCampus.addEventListener('click', function () {

  view.animate({
    center: CampusZoom,
    duration: 2000,
    zoom: 17
  })

}, false)


function zoomToCampusLocation (campusId) {

  // TODO if campus location point exists simply hide /show
  // ie do not re-create the geojson on every click

  var locationsUrl = baseApiUrl + 'campus/locations/?format=json'

  $('#campusLocations li').removeClass('active');

  $('#campusid-'+ campusId).addClass('active');

  indrzApiCall(locationsUrl).then(function (response) {

    response.features.forEach(function (feature) {

      if (parseInt(campusId) === feature.properties.id) {

        view.animate({
          center: feature.geometry.coordinates,
          duration: 2000,
          zoom: 17
        })

        open_popup(feature.properties, feature.geometry.coordinates, feature)

      }

    })

  })

}

