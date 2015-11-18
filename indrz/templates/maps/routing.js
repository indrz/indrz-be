var url_base = "/api/v1/directions/";
var start_coord = "-168527.958404064,5983885.94934575,-1";
var end_coord = "-168578.959377896,5983891.19705399,3";
var sel_Val = $("input:radio[name=typeRoute]:checked").val();
var geojs_url = url_base + start_coord + "&" + end_coord + "&" + sel_Val + '/?format=json';


var roomLayers = [];
var activeLayerIdx = 0;
var layerOffset = -1;


// uncomment this code if you want to reactivate
// the quick static demo switcher
//$(".radio").change(function () {
//    map.getLayers().pop();
//    var sel_Val2 = $("input:radio[name=typeRoute]:checked").val();
//    var routeUrl = '/api/v1/directions/-168527.958404064,5983885.94934575,-1&-168578.959377896,5983891.19705399,3&' + sel_Val2 + '/?format=json';
//
//    map.getLayers().push(new ol.layer.Vector({
//
//        //      source: new ol.source.GeoJSON({url: routeUrl}),
//        source: new ol.source.Vector({
//            url: routeUrl,
//            format: new ol.format.GeoJSON()
//        }),
//        style: new ol.style.Style({
//            stroke: new ol.style.Stroke({
//                color: 'blue',
//                width: 4
//            })
//        }),
//        title: "Route",
//        name: "Route"
//    }));
//
//});

var vectorLayer = new ol.layer.Vector({
    //source: new ol.source.GeoJSON({url: geojs_url}),
    source: new ol.source.Vector({
        url: geojs_url,
        format: new ol.format.GeoJSON()
    }),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 4
        })
    }),
    title: "Route",
    name: "Route"
});

var wmsUG01 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: 'http://ws1.gomogi.com/geoserver252/indrz/wms',
        params: {'LAYERS': 'indrz:ug01'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsUG01",
    floor: "-1",
    type: "floor level"


});

var wmsE00 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: 'http://ws1.gomogi.com/geoserver252/indrz/wms',
        params: {'LAYERS': 'indrz:e00'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: true,
    name: "wmsE00",
    floor: "0",
    type: "floor level"

});

var wmsE01 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: 'http://ws1.gomogi.com/geoserver252/indrz/wms',
        params: {'LAYERS': 'indrz:e01'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE01",
    floor: "1",
    type: "floor level"

});

var wmsE02 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: 'http://ws1.gomogi.com/geoserver252/indrz/wms',
        params: {'LAYERS': 'indrz:e02'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE02",
    floor: "2",
    type: "floor level"

});

var wmsE03 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: 'http://ws1.gomogi.com/geoserver252/indrz/wms',
        params: {'LAYERS': 'indrz:e03'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE03",
    floor: "3",
    type: "floor level"

});


var mapQuestOsm = new ol.layer.Tile({source: new ol.source.MapQuest({layer: 'osm'}), visible: false});
var OsmBackLayer = new ol.layer.Tile({source: new ol.source.OSM(), visible: true});

var allLayers = [vectorLayer,
     new ol.layer.Group({
      layers: [
          wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03
      ],
        type: "floor"
    }), new ol.layer.Group({
      layers: [
          mapQuestOsm, OsmBackLayer
      ],
        type: "background"
    })
  ];


var floorLevelsGroup = new ol.layer.Group({
    layers: [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    name: 'Floor Levels'
});


//function switchBackLayer()
// {
//  var checkedLayer = $('#layerswitcher input[name=layer]:checked').val();
//  for (i = 0, ii = backgroundLayers.length; i < ii; ++i) backgroundLayers[i].setVisible(i==checkedLayer);
// }
//
//$(function() { switchBackLayer() } );
//$("#layerswitcher input[name=layer]").change(function() { switchBackLayer() } );


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


var backLayers = [
  new ol.layer.Tile({
    style: 'Road',
    source: new ol.source.MapQuest({layer: 'osm'})
  }),
  new ol.layer.Tile({
    style: 'Aerial',
    visible: false,
    source: new ol.source.MapQuest({layer: 'sat'})
  })
];



var backgroundLayers = [];
backgroundLayers[0] = new ol.layer.Tile({source: new ol.source.MapQuest({layer: 'osm'}), visible: false});
backgroundLayers[1] = new ol.layer.Tile({source: new ol.source.OSM(), visible: true});


var backgroundLayerGroup = new ol.layer.Group({
    layers: backgroundLayers,
    name: 'Background Layers'
});

//var floor_levels = [];
//floor_levels[0] = wmsUG01;
//floor_levels[1] = wmsE00;
//floor_levels[1] = wmsE01;
//floor_levels[1] = wmsE02;
//floor_levels[1] = wmsE03;


var map = new ol.Map({
      interactions: ol.interaction.defaults().extend([
    new ol.interaction.DragRotateAndZoom()
  ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: allLayers,
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

map.addLayer(wmsUG01)
map.addLayer(backgroundLayers[0]);
map.addLayer(wmsUG01);
map.addLayer(wmsE00);
map.addLayer(wmsE01);
map.addLayer(wmsE02);
map.addLayer(wmsE03);
map.addLayer(vectorLayer);

//map.getLayerGroup().set('name', 'Root');

function addRoute(buildingId, fromNumber, toNumber, routeType) {
    map.getLayers().pop();
    console.log("addRoute big" + String(fromNumber));
    var baseUrl = 'http://localhost:8000/api/v1/directions/';
    var geoJsonUrl = baseUrl + 'building=' +  buildingId + '&startid=' + fromNumber + '&endid=' + toNumber + '/?format=json';

    console.log("final url " + geoJsonUrl);

    map.getLayers().push(new ol.layer.Vector({
        //source: new ol.source.GeoJSON({url: geoJsonUrl}),  // ol <= 3.40
        url: geoJsonUrl,
        format: new ol.format.GeoJSON(),
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


roomLayers = [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03];

function switchToRoomLayer(layer) {
    var len = roomLayers.length;

    for (var i = 0; i < len; i++) {
        console.info('pressed switch layer' + roomLayers[i].name + '  ' + layer.name);
        if (roomLayers[i].name == layer.name) {
            console.info('pressed switch layer' + roomLayers[i].name + '  ' + layer.name);
            roomLayers[i].setVisible(!roomLayers[i].getVisible());
        } else {
            roomLayers[i].setVisible(false);
        }
    }
}


function switchLayerTo(layer) {
    //deactivate centering on gps location
    //centerOnLocation = false;

    if (layer == activeLayerIdx) {
        return;
    }

    //$("#layer_" + (layer)).addClass('ui-btn-active');
    //$("#layer_" + (activeLayerIdx)).removeClass('ui-btn-active');  //ui-disabled

    var activeLayer = roomLayers[activeLayerIdx - layerOffset];
    var newActiveLayer = roomLayers[layer - layerOffset];

    //alert("received request to switch from " + activeLayer + " to " + newActiveLayer);
    switchToRoomLayer(newActiveLayer);   //turn layer tms off of old layer and on for new clicked active layer
    activeLayerIdx = layer;
    console.info('pressed switch layer' + activeLayer.name + '  ' + activeLayerIdx);
    //console.info(map.getLayerGroup().set('name', 'Root');)
    //doFloorStyle(activeLayerIdx);
}
