

function library_book_position(rvk_key) {

    return $.ajax({
        dataType: 'json',
        url: '/indrz/api/v1/library/location/' + rvk_key
    }).done(function (data) {
        // If successful
        // console.log('got book data', data);
        globalBookInfo[rvk_key.toUpperCase()] = data;

        routeLocalData.start = {};
        routeLocalData.start.xcoord = 1826545.2173675;
        routeLocalData.start.ycoord = 6142423.4241214;
        routeLocalData.start.floor = 0;
        var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;

        routeLocalData.start.routeValue = routeStartValue;
        routeLocalData.end = {};
        // console.log(JSON.stringify(data));
        routeLocalData.end.xcoord = data.geometry.coordinates[0];
        routeLocalData.end.ycoord = data.geometry.coordinates[1];
        routeLocalData.end.floor = data.properties.floor_num;

        var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;

        routeLocalData.end.routeValue = routeEndValue;

        routeToBook("LC Eingang", data.properties.name, routeStartValue, routeEndValue, 0);

        var libraryData = {};
        libraryData.route_info = {"walk_time":123.23};

        var popup_location = [data.geometry.coordinates[0]];
        popup_location.push(data.geometry.coordinates[1]);

        globalPopupInfo.bookId = data.properties.name;
        globalPopupInfo.bookCoords = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord;

        // globalRouteInfo.routeUrl = '?campus=1&key=' + rvk_key;

        // console.log("popuploacation is : " + popup_location);
        // console.log("coords  is : " + data.geometry.coordiantes);
        // console.log("props  is : " + data.properties);

        // TODO make library popup look good
        // uncomment to activate it works but looks bad
        open_popup(data.properties, popup_location, data.properties.name );

        $("#clearRoute").removeClass("hide");
        $("#shareRoute").removeClass("hide");
        $("#routeText").removeClass("hide");
        $('#collapseRouting').collapse('show');
        $('#collapsePoi').collapse('hide');


    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        //console.log(textStatus + ': ' + errorThrown);
    });
}



function routeToBook(startName, endName, startCoords, EndCoords, routeType) {


    if (routeLayer) {
        map.removeLayer(routeLayer);
        // map.removeLayer(markerLayer);
        clearRouteDescription();
        //map.getLayers().pop();
    }

    // if(markerLayer){
    //     map.removeLayer(markerLayer);
    // }

    if (routeNearestPoiLayer){
        map.removeLayer(routeNearestPoiLayer);
    }

    var geoJsonUrl = baseApiRoutingUrl + startCoords + "&" + EndCoords + "&" + routeType + '/?format=json';

    // var geoJsonUrl = baseApiRoutingUrl + "startstr=" + startSearchText + "&" + "endstr=" + endSearchText + '/?format=json';
    var startingLevel = routeType;

    var source = new ol.source.Vector();
    $.ajax({url:geoJsonUrl}).then(function (response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON();
        var features = geojsonFormat.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        source.addFeatures(features);
        //
        //
        var routeJson = JSON.stringify(response);
        var routeData = JSON.parse(routeJson);

        document.getElementById('route-to').value = endName;
        document.getElementById('route-from').value = startName;

        insertRouteDescriptionText(startName, endName, routeData, false);

        addLibraryMarkers(features, routeData.route_info);

        var start_floor = 0;
        // active the floor of the start point
        if(typeof(features[0]) !== 'undefined') {
            start_floor = features[0].getProperties().floor;
        }

        if (library_key !== "nokey") {
            start_floor = routeLocalData.end.floor;
        }

        for (var i = 0; i < floor_layers.length; i++) {
            if (start_floor == floor_layers[i].floor_num) {
                activateLayer(i);
            }
        }


        // center up the route
        var extent = source.getExtent();
        map.getView().fit(extent);


        globalRouteInfo.startName = startName;
        globalRouteInfo.endName = endName;
        globalRouteInfo.startPoiId = "noid";
        globalRouteInfo.endPoiId = "noid";
        globalRouteInfo.routeUrl = "?campus=1&key=" + endName;


    });

    libraryRouteLayer = new ol.layer.Vector({
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
        title: "RouteToBook",
        name: "RouteToBook",
        visible: true,
        layer_id: 3000,
        zIndex: 4
    });


    // routeLayerGroup.getLayers().push(libraryRouteLayer);
    map.addLayer(libraryRouteLayer);

    $("#clearRoute").removeClass("hide");
    $("#shareRoute").removeClass("hide");
    $("#routeText").removeClass("hide");
    $("#RouteDescription").removeClass("hide");

    window.location.href = "#map";

    $('html,body').animate({
            scrollTop: $("#map").offset().top
        },
        'slow');

}

function addLibraryMarkers(route_features, r_info) {

    var marker_features = [];
    var lengthList = [];
    var floorList = [];
    var prevFloorNum = -99;
    var index = -1;
    var nFeatures = route_features.length;
    var distance = 0;

    if (nFeatures == 0) return;
    // add middle icons
    for (var i = 0; i < nFeatures; i++) {
        var floor_num = route_features[i].getProperties().floor;
        if (prevFloorNum != floor_num) {
            floorList.push(floor_num);
            index++;
            prevFloorNum = floor_num;
            if (!lengthList[index]) lengthList[index] = 0;
        }
        lengthList[index] += route_features[i].getGeometry().getLength();
    }


    index = 0;
    for (i = 0; i < nFeatures; i++) {
        var floor_num = route_features[i].getProperties().floor;

        if (floorList[index] === floor_num)
            distance += route_features[i].getGeometry().getLength();
        if (floorList[index] === floor_num && lengthList[index] / 2 < distance) {
            var line_extent = route_features[i].getGeometry().getExtent();
            var middleCoordinate = ol.extent.getCenter(line_extent);
            var middlePoint = new ol.geom.Point(route_features[i].getGeometry().getClosestPoint(middleCoordinate));


            var middleFeature = new ol.Feature({
                geometry: middlePoint
            });
            var floor_num_style = new ol.style.Style({
                image: new ol.style.Icon({
                    src: '/static/img/route_floor_' + floor_num + '.png'
                })
            });


            middleFeature.setStyle(floor_num_style);
            marker_features.push(middleFeature);

            index++;
            distance = 0;
        }

    }


        var start_point = new ol.geom.Point(route_features[0].getGeometry().getFirstCoordinate());
        var end_point = new ol.geom.Point(route_features[route_features.length -1].getGeometry().getFirstCoordinate());

        var startMarker = new ol.Feature({
            geometry: start_point
        });
        startMarker.setStyle(route_marker_A_style);

        var endMarker = new ol.Feature({
            geometry: end_point
        });
        endMarker.setGeometry(end_point);
        endMarker.setStyle(route_marker_B_style);


        marker_features.push(startMarker);
        marker_features.push(endMarker);

    libraryMarkerLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: marker_features
        }),
        title: "RouteLibraryMarkers",
        name: "RouteLibraryMarkers",
        visible: true,
        layer_id: 20020,
        zIndex: 6
    });

    map.getLayers().push(libraryMarkerLayer);
}


// var createLibraryPopup = function (geometry, floor, building, fachboden, shelfID, rvk_key) {
//     //replace %20 with space
//     var key = rvk_key.split("%20").join(" ");
//     // zoom to feature
//     // removed fachboden icon show <tr align="center"><td colspan="2"><img height="35" width="35" src="img/lib_fachboden_'+fachboden+'.png"/></td></tr>
//     var contentHtml =
//         '<table width="100%" height="100%">' +
//         '<tr><td align="left"><b>' + $.t('library.building') + ':</b></td>' +
//         '<td align="left"><b>' + building + '</b></td></tr><tr>' +
//         '<td align="left"><b>' + $.t('routing.floor') + ':</b></td>' +
//         '<td align="left"><b>' + floor + '</b></td></tr><tr>' +
//         // '<td align="left"><b>'+$.t('library.shelf')+':</b></td>' +
//         // '<td align="left"><b>'+shelfID+'</b></td></tr><tr>' +
//         '<td align="left"><b>RVK:</b></td>' +
//         '<td align="left"><b>' + key + '</b></td></tr>' +
//         //'<tr><td colspan="2" align="center"><a href="http://www.wu.ac.at/library">'+ $.t("library.backToSearch")+'</a></td></tr>' +
//         '</table></td></tr></table>'
//
//     popupLocationGeom = getGeomWithPXOffset(geometry, 100, 0);
//
//     AppMain.viewer.tools['routingModule'].routingControl.libraryPopup = new GeoExt.Popup({
//         id: 'infoPopup',
//         title: $.t('library.popup_title'),
//         html: '<div id="libraryPopup">' + contentHtml + '</div>',
//         collapsible: true,
//         resizable: false,
//         draggable: true,
//         anchorPosition: 'bottom-right',
//         // location: geometry,
//         location: popupLocationGeom,
//         map: AppMain.viewer.mapPanel,
//         popupCls: "x-window-draggable"
//     });
//
//
//     AppMain.viewer.tools['routingModule'].routingControl.libraryPopup.show();
//
//
// };
//
// var destroyLibraryPopup = function () {
//     if (AppMain.viewer.tools['routingModule'].routingControl.libraryPopup != undefined) {
//         AppMain.viewer.tools['routingModule'].routingControl.libraryPopup.destroy();
//         AppMain.viewer.tools['routingModule'].routingControl.libraryPopup = undefined;
//     }
// };

// var calculateRouteToShelf = function (geo, floor) {
// var shelf_Middle = geo[0].geometry.getCentroid();
//
// AppMain.viewer.tools['routingModule'].addRouteStartPoint(1826545.2173675, 6142423.4241214, $.t('library.routeStart'), 0);
// AppMain.viewer.tools['routingModule'].addRouteEndPoint(shelf_Middle.x, shelf_Middle.y, $.t('library.routeEnd'), floor);
//
// //switch floor and center
// AppMain.viewer.tools['routingModule'].routingControl.centerTo(shelf_Middle.x, shelf_Middle.y, 22);
// AppMain.changeFloorTo(floor);

// function RouteToShelf(rvk_id) {
//     // request, start_coord, start_floor, end_coord, end_floor, route_type):
//     //http:/localhost:8000/api/v1/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&0
//
//     var baseUrl = '/api/v1/library/route/';
//     var geoJsonUrl = baseUrl + rvk_id;
//
//
//     if (routeLayer) {
//         map.removeLayer(routeLayer);
//         console.log("removing layer now");
//         //map.getLayers().pop();
//     }
//
//     var source = new ol.source.Vector();
//     $.ajax(geoJsonUrl).then(function (response) {
//         //console.log("response", response);
//         var geojsonFormat = new ol.format.GeoJSON();
//         var features = geojsonFormat.readFeatures(response,
//             {featureProjection: 'EPSG:4326'});
//         source.addFeatures(features);
//
//         addMarkers(features);
//
//         // active the floor of the start point
//         var start_floor = features[0].getProperties().floor;
//         for (var i = 0; i < switchableLayers.length; i++) {
//             if (start_floor == switchableLayers[i].getProperties().floor_num) {
//                 activateLayer(i);
//             }
//         }
//         // center up the route
//         var extent = source.getExtent();
//         map.getView().fit(extent, map.getSize());
//     });
//
//     routeLayer = new ol.layer.Vector({
//         //url: geoJsonUrl,
//         //format: new ol.format.GeoJSON(),
//         source: source,
//         style: function (feature, resolution) {
//             var feature_floor = feature.getProperties().floor;
//             if (feature_floor == active_floor_num) {
//                 feature.setStyle(route_active_style);
//             } else {
//                 feature.setStyle(route_inactive_style);
//             }
//         },
//         title: "Route",
//         name: "Route",
//         visible: true,
//         zIndex: 9999
//     });
//
//     map.getLayers().push(routeLayer);
//
//     $("#clearRoute").removeClass("hide");
//     $("#shareRoute").removeClass("hide");
//
// }
//
// var unanchorPopup = function (popup) {
//     popup.removeAnchorEvents();
//
//     //make the window draggable
//     popup.draggable = true;
//     popup.header.addClass("x-window-draggable");
//     popup.dd = new Ext.Window.DD(popup);
//
//     //remove anchor
//     popup.anc.remove();
//     popup.anc = null;
//
//     //hide unpin tool
//     popup.tools.unpin.hide();
// };


/*
 returns a new geom with pixel offset. has to be in 900973 format
 point should be  OpenLayers.Geometry.Point
 xOff and yOff are in Pixels
 */
// var getGeomWithPXOffset = function (point, xOff, yOff) {
//     var x = point.x;
//     var y = point.y;
//
//     console.log(AppMain);
//
//     var location = AppMain.viewer.tools['routingModule'].routingControl.map.getPixelFromLonLat(new OpenLayers.LonLat(x, y));
//
//     location.x += xOff;
//     location.y += yOff;
//
//     var locationLonLat = AppMain.viewer.tools['routingModule'].routingControl.map.getLonLatFromLayerPx(location);
//
//     return new OpenLayers.Geometry.Point(locationLonLat.lon, locationLonLat.lat);
// };
// ;