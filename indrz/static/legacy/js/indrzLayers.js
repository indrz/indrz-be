var tilegrid = new ol.tilegrid.WMTS({
    origin: [-20037508.3428, 20037508.3428],
    extent: [977650, 5838030, 1913530, 6281290],
    resolutions: [
        156543.03392811998,
        78271.51696419998,
        39135.758481959994,
        19567.879241008,
        9783.939620504,
        4891.969810252,
        2445.984905126,
        1222.9924525644,
        611.4962262807999,
        305.74811314039994,
        152.87405657047998,
        76.43702828523999,
        38.21851414248,
        19.109257071295996,
        9.554628535647998,
        4.777314267823999,
        2.3886571339119995,
        1.1943285669559998,
        0.5971642834779999,
        0.29858214174039993,
        0.14929107086936
    ],
    ////resolutions: [
    ////    559082264.029 * 0.28E-3,
    ////    279541132.015 * 0.28E-3,
    ////    139770566.007 * 0.28E-3,
    ////    69885283.0036 * 0.28E-3,
    ////    34942641.5018 * 0.28E-3,
    ////    17471320.7509 * 0.28E-3,
    ////    8735660.37545 * 0.28E-3,
    ////    4367830.18773 * 0.28E-3,
    ////    2183915.09386 * 0.28E-3,
    ////    1091957.54693 * 0.28E-3,
    ////    545978.773466 * 0.28E-3,
    ////    272989.386733 * 0.28E-3,
    ////    136494.693366 * 0.28E-3,
    ////    68247.3466832 * 0.28E-3,
    ////    34123.6733416 * 0.28E-3,
    ////    17061.8366708 * 0.28E-3,
    ////    8530.91833540 * 0.28E-3,
    ////    4265.45916770 * 0.28E-3,
    ////    2132.72958385 * 0.28E-3,
    ////    1066.36479193 * 0.28E-3,
    ////    533.182395962 * 0.28E-3
    ////],
    matrixIds: [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '20'
    ]
});

// source: new ol.source.OSM({
//   attributions: [
//     new ol.Attribution({
//       html: 'All maps © ' +
//           '<a href="https://www.opencyclemap.org/">OpenCycleMap</a>'
//     }),
//     ol.source.OSM.ATTRIBUTION
//   ],

function createWmtsLayer(layerSrcName, type, isVisible, sourceName) {
    var gg, sm, templatepng, urlsbmappng, WmtsTileSource, wmtsLayer;
    gg = ol.proj.get('EPSG:4326');
    sm = ol.proj.get('EPSG:3857');
    templatepng = '{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}' + type;
    urlsbmappng = [
        'https://maps1.wien.gv.at/basemap/' + templatepng,
        'https://maps2.wien.gv.at/basemap/' + templatepng,
        'https://maps3.wien.gv.at/basemap/' + templatepng,
        'https://maps4.wien.gv.at/basemap/' + templatepng
    ];


    WmtsTileSource = new ol.source.WMTS({
        tilePixelRatio: 1,
        projection: sm,
        layer: layerSrcName,
        style: 'normal',
        matrixSet: 'google3857',
        urls: urlsbmappng,
        crossOrigin: 'anonymous',
        requestEncoding: /** @type {ol.source.WMTSRequestEncoding} */ ('REST'),
        tileGrid: tilegrid,
        attributions: '© <a href="https://www.basemap.at/' + '">Basemap.at       </a>',


    });

    wmtsLayer = new ol.layer.Tile({
        name: layerSrcName,
        source: WmtsTileSource,
        minResolution: 0.298582141738,
        visible: isVisible,
        type: "background"

    });

    return wmtsLayer;


}

function createWmtsLayerIndrz(name, layerSrcName, floorNumber, isVisible, zIndexValue) {
    var gg, sm, templatepng, urlsbmappng, WmtsTileSource, wmtsLayer;
    gg = ol.proj.get('EPSG:4326');
    sm = ol.proj.get('EPSG:3857');
    var gridsetName = 'EPSG:3857';
    var gridNames = ["EPSG:3857:0",
                    "EPSG:3857:1",
                    "EPSG:3857:2",
                    "EPSG:3857:3",
                    "EPSG:3857:4",
                    "EPSG:3857:5",
                    "EPSG:3857:6",
                    "EPSG:3857:7",
                    "EPSG:3857:8",
                    "EPSG:3857:9",
                    "EPSG:3857:10",
                    "EPSG:3857:11",
                    "EPSG:3857:12",
                    "EPSG:3857:13",
                    "EPSG:3857:14",
                    "EPSG:3857:15",
                    "EPSG:3857:16",
                    "EPSG:3857:17",
                    "EPSG:3857:18",
                    "EPSG:3857:19",
                    "EPSG:3857:20",
                    "EPSG:3857:21",
                    "EPSG:3857:22",
                    "EPSG:3857:23"];

    // var resolutions = [156543.03390625,
    //                     78271.516953125,
    //                     39135.7584765625,
    //                     19567.87923828125,
    //                     9783.939619140625,
    //                     4891.9698095703125,
    //                     2445.9849047851562,
    //                     1222.9924523925781,
    //                     611.4962261962891,
    //                     305.74811309814453,
    //                     152.87405654907226,
    //                     76.43702827453613,
    //                     38.218514137268066,
    //                     19.109257068634033,
    //                     9.554628534317017,
    //                     4.777314267158508,
    //                     2.388657133579254,
    //                     1.194328566789627,
    //                     0.5971642833948135,
    //                     0.2985821416974068,
    //                     0.1492910708487034,
    //                     0.0746455354243517,
    //                     0.0373227677121758,
    //                     0.0186613838560879];
    var style = '';
      var projection = ol.proj.get('EPSG:3857');
      var projectionExtent = projection.getExtent();
      var size = ol.extent.getWidth(projectionExtent) / 256;
      var resolutions = new Array(23);
      var matrixIds = new Array(23);
      for (var z = 0; z < 23; ++z) {
        // generate resolutions and matrixIds arrays for this WMTS
        resolutions[z] = size / Math.pow(2, z);
        matrixIds[z] = z;
      }




    WmtsTileSource = new ol.source.WMTS({
            url: baseGeoserverUrl + "gwc/service/wmts",
            layer: layerSrcName,
            matrixSet: gridsetName,
            format: 'image/png',
            projection: projection,
            tileGrid: new ol.tilegrid.WMTS({
                origin: ol.extent.getTopLeft(projectionExtent),
              tileSize: [256,256],
              extent: [-2.003750834E7,-2.003750834E7,2.003750834E7,2.003750834E7],

              resolutions: resolutions,

              matrixIds: gridNames
            }),
            style: style,
            wrapX: true
          });

    wmtsLayer = new ol.layer.Tile({
        name: layerSrcName,
        floor_num: floorNumber,
        type: "floor",

        source: WmtsTileSource,
        zIndex: zIndexValue,
        maxResolution:4.777314267158508,
        minResolution:0.0186613838560879,
        visible: isVisible

    });

    return wmtsLayer;


}




function createImageWms(geoserverLayer){

   var wmsSource2 = new ol.source.ImageWMS({
    url: baseGeoserverUrl + "indrz/wms",
    params: {LAYERS: 'indrz:' + geoserverlayer, 'FORMAT': 'image/png', 'VERSION': '1.1.1', STYLES:''},
    serverType: 'geoserver',
    crossOrigin: 'anonymous'
    });

    var wmsFloorLayer = new ol.layer.Image({
    source: wmsSource2
    });

    return wmsFloorLayer;

}

function createTileXyz(name, layer, floor, is_visible, zIndex) {
    var f_url = baseGeoserverUrl + 'gwc/service/tms/1.0.0/' + layer + '/{z}/{x}/{-y}.png';

    var tmp_lyr = new ol.layer.Tile({

        source: new ol.source.XYZ({
            url: f_url,
            minZoom: 15,
        }),
        visible: is_visible,
        name: name,
        floor_num: floor,
        type: 'floor',
        zIndex: zIndex,
        crossOrigin: "anonymous"
    });

    return tmp_lyr;

}


function createWmsLayer(layerName, geoserverLayer, floorNumber, isVisible, zIndexValue) {
    var newWmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: baseGeoserverUrl + "indrz/wms",
            params: {'LAYERS': geoserverLayer, 'TILED': true},
            serverType: 'geoserver',
            crossOrigin: ''
        }),
        visible: isVisible,
        name: layerName,
        floor_num: floorNumber,
        type: "floor",
        zIndex: zIndexValue,
        crossOrigin: "anonymous"

    });

    return newWmsLayer;
}

var grey_bmapat = createWmtsLayer('bmapgrau', '.png', true, "basemap.at");
// var wmsOutdoorMap = createWmtsLayerIndrz('outdoorMap', 'indrz:outdoor', '0', 'true', 1 );
var ortho30cm_bmapat = createWmtsLayer('bmaporthofoto30cm', '.jpg', false, "basemap.at");

var backgroundLayerGroup = new ol.layer.Group({layers: [grey_bmapat, ortho30cm_bmapat], name: "background maps"});

var wmsE00, wmsE01, wmsE02, wmsE03;

// wmsE00 = createWmtsLayerIndrz('e00', 'indrz:e00', '0', 'true', 3);
// wmsE01 = createWmtsLayerIndrz('e01', 'indrz:e01', '1', 'false', 3);
// wmsE02 = createWmtsLayerIndrz('e02', 'indrz:e02', '2', 'false', 3);
// wmsE03 = createWmtsLayerIndrz('e03', 'indrz:e03', '3', 'false', 3);

wmsE00 = createWmsLayer('e00', 'indrz:e00', '0', 'true', 3);
wmsE01 = createWmsLayer('e01', 'indrz:e01', '1', 'false', 3);
wmsE02 = createWmsLayer('e02', 'indrz:e02', '2', 'false', 3);
wmsE03 = createWmsLayer('e03', 'indrz:e03', '3', 'false', 3);



var wmsfloorLayerGroup = new ol.layer.Group({layers: [wmsE00, wmsE01, wmsE02, wmsE03], name: "wms floor maps"});
var poiLayerGroup = new ol.layer.Group({layers: [], id:99999, name: "poi group"});
var campusLocationsGroup = new ol.layer.Group({layers: [], id:900, name: "campus locations"});

var routeLayerGroup = new ol.layer.Group({layers:[], name: "route group"});

// var floor_layers = [ wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06 ];

var OsmBackLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    type: "background"
});


indrzApiCall( baseApiUrl + "campus/1/floors/" )
    .then(function (response) {
        floors_info = response;

        for (var i = 0; i < floors_info.length; ++i) {
            floor_layers.push(floors_info[i]);
            // appendFloorNav(floors_info[i].short_name, [i]);
            appendFloorNav(floors_info[i].floor_num, [i]);
            }

        activateLayer(floor_num);

    });


function appendFloorNav(floor_info, index) {
    $("#floor-links").prepend("<li class='list-group-item ' >" +
        "<a href='#' onclick='activateLayer(" + index + ");' id='floorIndex_" + index  + "' class='indrz-floorswitcher' >" + floor_info + " </a>" +
        "</li>");

    if(index[0] === 1){
        var option_html = "<option selected='selected' value='"+ index +"'>" + floor_info + "</option>";
        $("#floor-links-select").prepend(option_html);
    }else{
        $("#floor-links-select").prepend("<option value='"+ index +"'>" + floor_info +"</option>");
    }
}
