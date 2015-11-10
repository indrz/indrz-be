var url_base = "/api/v1/directions/";
var start_coord = "-168527.958404064,5983885.94934575,-1";
var end_coord = "-168578.959377896,5983891.19705399,3";
var sel_Val = $("input:radio[name=typeRoute]:checked").val();
var geojs_url = url_base + start_coord + "&" + end_coord + "&" + sel_Val + '/?format=json';

// uncomment this code if you want to reactivate
// the quick static demo switcher
$( ".radio" ).change(function() {
   map.getLayers().pop();
   var sel_Val2 = $( "input:radio[name=typeRoute]:checked" ).val();
   var routeUrl = '/api/v1/directions/-168527.958404064,5983885.94934575,-1&-168578.959377896,5983891.19705399,3&' + sel_Val2  + '/?format=json';

  map.getLayers().push(new ol.layer.Vector({
            source: new ol.source.GeoJSON({url: routeUrl}),
            style:  new ol.style.Style({
                stroke: new ol.style.Stroke({
                  color: 'blue',
                  width: 4
                })
              }),
            title: "Route",
            name: "Route"
        }));

});

var vectorLayer = new ol.layer.Vector({
    source: new ol.source.GeoJSON({url: geojs_url}),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 4
        })
    }),
    title: "Route",
    name: "Route"
});



var tms_e00 = new ol.layer.Tile({
    source: new ol.source.XYZ({
        attributions: [            new ol.Attribution({
                html: 'Tiles &copy; <a href="http://www.basemap.at/">' +
                    '<b></b>asemap.at</a> (STANDARD).'
            })],
        url: '/static/e00/{z}/{x}/{y}.png'
    }),
    title: 'E00'
});

var tms_e01 = new ol.layer.Tile({
    source: new ol.source.XYZ({
        attributions: [            new ol.Attribution({
                html: 'Tiles &copy; <a href="http://www.basemap.at/">' +
                    '<b></b>asemap.at</a> (STANDARD).'
            })],
        url: '/static/e01/{z}/{x}/{y}.png'
    }),
    title: 'E01'
});

function switchLayer()
 {
  var checkedLayer = $('#layerswitcher input[name=layer]:checked').val();
  for (i = 0, ii = layers.length; i < ii; ++i) layers[i].setVisible(i==checkedLayer);
 }

$(function() { switchLayer() } );
$("#layerswitcher input[name=layer]").change(function() { switchLayer() } );

var layers = [];
layers[0] = new ol.layer.Tile({ source: new ol.source.MapQuest({layer: 'osm'}) });
layers[1] = new ol.layer.Group({ layers: [ new ol.layer.Tile({ source: new ol.source.MapQuest({layer: 'sat'}) }), new ol.layer.Tile({ source: new ol.source.MapQuest({layer: 'hyb'}) }) ] });
layers[2] = new ol.layer.Tile({ source: new ol.source.MapQuest({layer: 'sat'}) });
layers[3] = new ol.layer.Tile({ source: new ol.source.OSM() });
layers[4] = tms_e01;
layers[5] = tms_e00;
layers[6] = vectorLayer;


var map = new ol.Map({
    layers: layers,
    target: 'map',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }),
    view: new ol.View({
        center: [-168527.958404064, 5983885.94934575],
        zoom: 18
    })
});

function addRoute(fromNumber, toNumber, routeType) {
    map.getLayers().pop();
    console.log("addRoute big" + String(fromNumber));
    var baseUrl = 'http://localhost:8000/api/v1/directions/';
    var geoJsonUrl = baseUrl + fromNumber + '&' + toNumber + '&' + routeType + '/?format=json';
    console.log("final url " + geoJsonUrl);
    map.getLayers().push(new ol.layer.Vector({
        source: new ol.source.GeoJSON({url: geoJsonUrl}),
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'purple',
                width: 4
            })
        }),
        title: "Route",
        name: "Route"
    }));
}