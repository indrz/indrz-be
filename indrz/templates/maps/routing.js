
var switchableLayers = [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03];
function hideLayers() {
    for (var i=0; i<switchableLayers.length; i++) {
        switchableLayers[i].setVisible(false);
    }
    if(floor_layers.length > 0) {
        for (var i = 0; i < floor_layers.length; i++) {
            floor_layers[i].setVisible(false);
        }
    }
    $("#floor-links li").removeClass("active");
}
function setLayerVisible(index) {
    switchableLayers[index].setVisible(true);
    if(floor_layers.length > 0) {
        floor_layers[index].setVisible(true);
        $("#floor-links li:nth-child(" + (index + 1) + ")").addClass("active");
    }
}
function activateLayer(index) {
    hideLayers();
    setLayerVisible(index);
}


function switchBackgroundTo(backNum) {
    if (backNum === 1) // OSM
    {
        backgroundLayers[1].setVisible(true);
        backgroundLayers[0].setVisible(false);
    }
    else if (backNum === 0) // Mapquest OSM
    {
        backgroundLayers[0].setVisible(true);
        backgroundLayers[1].setVisible(false);
    }

}


var vector = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/api/v1/buildings/spaces/' + building_id +'/' + space_id +'.json',
    format: new ol.format.GeoJSON()
  }),
        style:  new ol.style.Style({
            stroke: new ol.style.Stroke({
              color: 'red',
              width: 2
            })
          }),
        title: "spaces",
        name: "spaces",
        zIndex: 1,
        visible: true

});



var map = new ol.Map({
      interactions: ol.interaction.defaults().extend([
    new ol.interaction.DragRotateAndZoom()
  ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: [
        new ol.layer.Group({
                'title': 'Background',
                layers: [mapQuestOsm, OsmBackLayer, SatelliteLayer
                ]
        }),
        new ol.layer.Group({
            title: 'Etage',
            layers: [

                        wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03
                ]
            }),
    ],
    target: 'map',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }),
    view: new ol.View({
        center: [startCenterX, startCenterY],
        zoom: zoom_level
    })
});

var routeLayer = null;

function addRoute(buildingId, fromNumber, toNumber, routeType) {
    var baseUrl = '/api/v1/directions/';
    var geoJsonUrl = baseUrl + 'buildingid=' +  buildingId + '&startid=' + fromNumber + '&endid=' + toNumber + '/?format=json';

    var startingLevel = fromNumber.charAt(0);
    //switch(startingLevel) {
    //    case("9"):
    //        activateLayer(0);
    //        break;
    //    case("0"):
    //        activateLayer(0);
    //        break;
    //    case("1"):
    //        activateLayer(1);
    //        break;
    //    case("2"):
    //        activateLayer(2);
    //        break;
    //    case("3"):
    //        activateLayer(3);
    //        break;
    //    default:
    //        break;
    //}

    if (routeLayer) {
      map.removeLayer(routeLayer);
        console.log("removing layer now");
        //map.getLayers().pop();
   }

    var source = new ol.source.Vector();
    $.ajax(geoJsonUrl).then(function(response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON();
        var features = geojsonFormat.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        source.addFeatures(features);
        //console.log("route layer source", source);
    });

    routeLayer = new ol.layer.Vector({
        //url: geoJsonUrl,
        //format: new ol.format.GeoJSON(),
        source: source,
        style:  new ol.style.Style({
            stroke: new ol.style.Stroke({
              color: 'red',
              width: 2
            })
          }),
        title: "Route",
        name: "Route",
        visible: true
            });
    //map.addLayer(routeLayer);

    map.getLayers().push(routeLayer);

    $("#clearRoute").removeClass("hide");
}

$("#clearRoute").click(function(){
    if (routeLayer) {
        map.removeLayer(routeLayer);
    }
    $("#clearRoute").addClass("hide")
});


