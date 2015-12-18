var wmsUG01 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': 'indrz:ug01'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsUG01",
    floor: "-1",
    type: "floor"

});

var wmsE00 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': 'indrz:e00'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: true,
    name: "wmsE00",
    floor: "0",
    type: "floor"

});

var wmsE01 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': 'indrz:e01'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE01",
    floor: "1",
    type: "floor"

});

var wmsE02 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': 'indrz:e02'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE02",
    floor: "2",
    type: "floor"

});

var wmsE03 = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': 'indrz:e03'},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: false,
    name: "wmsE03",
    floor: "3",
    type: "floor"

});


var mapQuestOsm = new ol.layer.Tile({
    source: new ol.source.MapQuest({
        layer: 'osm'}),
    visible: false,
    type: "background"});

var OsmBackLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    type:"background"});

var SatelliteLayer = new ol.layer.Tile({
    source: new ol.source.MapQuest({layer: 'sat'}),
    visible: false,
    type:"background"
})