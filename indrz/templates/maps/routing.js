var routeLayer = null;
var markerLayer = null;


var start_maker_style = new ol.style.Style({
    image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: '/static/img/route_start.png',
    })
});


var end_maker_style = new ol.style.Style({
    image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: '/static/img/route_end.png'
    })
});


var switchableLayers = [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03];

var route_active_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
        color: 'red',
        width: 4
    })
});

var route_inactive_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
        color: 'red',
        width: 2,
        lineDash: [0.1, 5],
        opacity: 0.5
    })
});


function waitForFloors(space_floor_id) {
    if (floor_layers.length > 0) {
        for (var i = 0; i < building_info.num_floors; i++) {
            if (building_info.buildingfloor_set[i].id == space_floor_id) {
                activateLayer(i);
            }
        }
    }
    else {
        setTimeout(function () {
            waitForFloors(space_floor_id);
        }, 250);
    }
}


function hideLayers() {
    for (var i = 0; i < switchableLayers.length; i++) {
        switchableLayers[i].setVisible(false);
    }
    if (floor_layers.length > 0) {
        for (var i = 0; i < floor_layers.length; i++) {
            floor_layers[i].setVisible(false);
        }
    }
    $("#floor-links li").removeClass("active");
}


function setLayerVisible(index) {
    switchableLayers[index].setVisible(true);
    if (floor_layers.length > 0) {
        floor_layers[index].setVisible(true);
        $("#floor-links li:nth-child(" + (floor_layers.length - index) + ")").addClass("active");

        // set active_floor_num
        active_floor_num = floor_layers[index].getProperties().floor_num;
        if (routeLayer) {
            var features = routeLayer.getSource().getFeatures();
            for (var i = 0; i < features.length; i++) {
                var feature_floor = features[i].getProperties().floor;
                if (feature_floor == active_floor_num) {
                    features[i].setStyle(route_active_style);
                } else {
                    features[i].setStyle(route_inactive_style);
                }
            }
        }
    }
}


function activateLayer(index) {
    hideLayers();
    setLayerVisible(index);
}


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


function addRoute(buildingId, fromNumber, toNumber, routeType) {
    var baseUrl = '/api/v1/directions/';
    var geoJsonUrl = baseUrl + 'buildingid=' + buildingId + '&startid=' + fromNumber + '&endid=' + toNumber + '/?format=json';

    var startingLevel = fromNumber.charAt(0);

    if (routeLayer) {
        map.removeLayer(routeLayer);
        console.log("removing layer now");
        //map.getLayers().pop();
    }

    var source = new ol.source.Vector();
    $.ajax(geoJsonUrl).then(function (response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON();
        var features = geojsonFormat.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        source.addFeatures(features);

        addMarkers(features);

        // active the floor of the start point
        var start_floor = features[0].getProperties().floor;
        for (var i = 0; i < floor_layers.length; i++) {
            if (start_floor == floor_layers[i].getProperties().floor_num) {
                activateLayer(i);
            }
        }
    });

    routeLayer = new ol.layer.Vector({
        //url: geoJsonUrl,
        //format: new ol.format.GeoJSON(),
        source: source,
        style: function (feature, resolution) {
            var feature_floor = feature.getProperties().floor;
            if (feature_floor == active_floor_num) {
                feature.setStyle(route_active_style);
            } else {
                feature.setStyle(route_inactive_style);
            }
        },
        title: "Route",
        name: "Route",
        visible: true
    });

    map.getLayers().push(routeLayer);

    $("#clearRoute").removeClass("hide");
}

$("#clearRoute").click(function () {
    if (routeLayer) {
        map.removeLayer(routeLayer);
    }
    if (markerLayer) {
        map.removeLayer(markerLayer);
    }
    $("#clearRoute").addClass("hide");
    $("#route-to").val('');
    $("#route-from").val('');
});


function addMarkers(route_features) {
    var coordinates = route_features[0].getGeometry().getCoordinates();
    var start_point = new ol.geom.Point(coordinates[coordinates.length - 1]);
    coordinates = route_features[route_features.length - 1].getGeometry().getCoordinates()
    var end_point = new ol.geom.Point(coordinates[coordinates.length - 1]);
    var startMarker = new ol.Feature({
        geometry: start_point
    });
    var endMarker = new ol.Feature({
        geometry: end_point
    });
    endMarker.setGeometry(end_point);
    startMarker.setStyle(start_maker_style);
    endMarker.setStyle(end_maker_style);

    if (markerLayer) {
        map.removeLayer(markerLayer);
    }

    markerLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [startMarker, endMarker]
        }),
        title: "icon_layer",
        name: "icon_layer",
        visible: true
    });
    map.getLayers().push(markerLayer);
}