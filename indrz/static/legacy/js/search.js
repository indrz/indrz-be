var searchLayer = null;


var image = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: '/static/homepage/img/other.png'
        }));

var poiHideIcon = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: '/static/homepage/img/other.png',
            opacity: 0.1
        }));

var show_poi_search_style = new ol.style.Style({
    image: image
  });


var hide_poi_search_style = new ol.style.Style({
    image: poiHideIcon
  });




var show_search_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#4ff0ff',
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(38, 215, 255, 0.4)'
    })
  });




var hide_search_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#fff6d2',
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(162, 162, 162, 0.1)'
    })
  });

var styles = {
  'Point': [new ol.style.Style({
    image: image
  })],
  'LineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#68ff5b',
      width: 1
    })
  })],
  'MultiLineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#68ff5b',
      width: 1
    })
  })],
  'MultiPoint': [new ol.style.Style({
    image: image
  })],
  'MultiPolygon': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#4ff0ff',
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(38, 215, 255, 0.4)'
    })
  })],
  'Polygon': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#4ff0ff',
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(38, 215, 255, 0.4)'
    })
  })],
  'GeometryCollection': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'magenta',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'magenta'
    }),
    image: new ol.style.Circle({
      radius: 10,
      fill: null,
      stroke: new ol.style.Stroke({
        color: 'magenta'
      })
    })
  })],
  'Circle': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'red',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'rgba(255,0,0,0.2)'
    })
  })]
};


var styleFunctionHide = function(feature, resolution) {

    var fType = feature.getGeometry().getType();


    if(fType === "MultiPolygon"){
        return styles[feature.getGeometry().getType()];

    }else if (fType === "MultiPoint"){

        var poiImage = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: feature.get('icon'),
            opacity: 0.3
        }));

        var stylesPoi = new ol.style.Style({
                image: poiImage
              });

        return stylesPoi;

    }
};


var styleFunction = function(feature, resolution) {

    var fType = feature.getGeometry().getType();
    if(fType === "MultiPolygon"){
        return styles[feature.getGeometry().getType()];

    }else if (fType === "MultiPoint"){

        var poiImage = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: feature.get('icon'),
            opacity: 1
        }));

        var stylesPoi = new ol.style.Style({
                image: poiImage
              });

        return stylesPoi;


    }
};


var search_res_style = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.6)'
    }),
    stroke: new ol.style.Stroke({
        color: '#319FD3',
        width: 2
    }),
    text: new ol.style.Text({
        font: 'bold 12px Arial,sans-serif',
        fill: new ol.style.Fill({
            color: '#000'
        }),
        maxResolution: 2000,
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
        })
    })
});


function setSearchFeatureStyle(feature, resolution) {
    if (feature) {

        if (feature.get('short_name') !== null) {
            //info.innerHTML = feature.getId() + ': ' + feature.get('name');
            search_res_style.getText().setText(resolution < 0.1 ? feature.get('short_name') : '');
            return [search_res_style];

        }
    }

}

function searchType(obj){

    if(obj.length === 1){
        var indrzSearchTypes = ['poi', 'space', 'building', 'campus', 'externalApi'];

        indrzType = null;

        var props = obj.getProperties();

        if (props.hasOwnProperty('poi_id')){
            indrzType = 'poi';
            return indrzType
        } else if (props.hasOwnProperty('poi_id')){

        }


    }


}

function zoomToFeature(source) {

    var view = map.getView();
    // // view.setCenter([centerx, centery]);
    // view.setZoom(19);

    var feature = source.getFeatures()[0];
    var polygon = /** @type {ol.geom.SimpleGeometry} */ (feature.getGeometry());
    var size = /** @type {ol.Size} */ (map.getSize());
    view.fit(polygon, size, {padding: [170, 50, 30, 150], constrainResolution: false})

    // view.fit(polygon, size, {padding: [170, 50, 30, 150], nearest: true})}
    // view.fit(point, size, {padding: [170, 50, 30, 150], minResolution: 50})}
    }


function getCenterOfExtent(Extent){
    var X = Extent[0] + (Extent[2]-Extent[0])/2;
    var Y = Extent[1] + (Extent[3]-Extent[1])/2;
    return [X, Y];
}

function zoomer(coord, zoomLevel){
    view.animate({
              center: coord,
              duration: 2000,
              zoom: zoomLevel
            });

    }




function activateFloor(feature){
    // console.log(feature.getProperties().floor_num);

    // feature.get('floor_num')
    var floor = feature.getProperties().floor_num;
    for (var i = 0; i < switchableLayers.length; i++) {

        if (typeof floor === "number" ){
            floor = floor.toString();

        }else{

        }

        if (floor === switchableLayers[i].getProperties().floor_num) {

            activateLayer(i);
        }
    }

}

function clearSearchResults(){

    search_text = "";

    if (searchLayer) {
        map.removeLayer(searchLayer);

    }

    closeIndrzPopup();

    $("#search-results-list").empty();
    $("#search-res").addClass("hide");
    $("#clearSearch").addClass("hide");
    $("#shareSearch").addClass("hide");
    $("#search-input").val('');
    $("#search-input-kiosk").val('');
    $("#searchTools").hide(); // hide div tag

    fixContentHeight();

    // if (routeLayer) {
    //     map.removeLayer(routeLayer);
    // }
    // if (markerLayer) {
    //     map.removeLayer(markerLayer);
    // }
    // $("#clearRoute").addClass("hide");
    // $("#shareRoute").addClass("hide");
    // $("#route-to").val('');
    // $("#route-from").val('');


}


function getResultTitle(properties){
    var name;
    if (properties.fancyname_de !== "" && typeof properties.fancyname_de !== 'undefined') {
        name = properties.fancyname_de;
        return name;
    }
    else if(properties.name !== "" && typeof properties.name !== 'undefined'){
        // console.log(req_locale);

        if(properties.hasOwnProperty('name_de') && req_locale === "de"){
            name = properties.name_de;
            return name;

        }

        name = properties.name;
        return name;

    }
    else if (properties.short_name !== "" && typeof properties.short_name !== 'undefined'){
        name = properties.room_code;
        return name;
    }
    else if (properties.label !== "" && typeof properties.label !== 'undefined'){
        name = properties.fancyname_de;
        return name;
    }
    else if (properties.roomcode && typeof properties.label !== 'undefined'){
        name = properties.roomcode;
        return name;
    }
    else if (properties.room_code !== "" && typeof properties.room_code !== 'undefined') {
        name = properties.room_code;
        return name;
    }else{
        name = "";
        return name;
    }

}



function generateResultLinks(att, searchString, f_center, className, floor, fid, poi_icon){
        fid = fid || 0;
        poi_icon = poi_icon || 0;
        var poi_icon_html = "";

        var poiId = fid;
        if(fid === 0){
           var elId = "searchResListItem_" + att
        }else{
            var elId = "searchResListItem_" + att + "-" + poiId;
            poi_icon_html = '<img src=\"' + poi_icon + '" alt=\"POI\" style=\"height: 25px; padding-right:5px;\">';

        }



        var htmlInsert = '<a href="#" onclick="showRes(' + searchString + "," + f_center + "," + poiId + ')" id="'+ elId +
        '" class="list-group-item indrz-search-res" >' + className + ' <span class="badge">'+ gettext("Floor  ") + floor +'</span> </a>';

        if(poi_icon !== ""){
            var htmlInsert = '<a href="#" onclick="showRes(' + searchString + "," + f_center + "," + poiId + ')" id="'+ elId +
            '" class="list-group-item indrz-search-res" >  ' + poi_icon_html + className + ' <span class="badge">'+ gettext("Floor  ") + floor +'</span> </a>';

        }

        // properties.name = "001_40_OG04_002500"

        // <a href="#" onclick="showRes('001_40_OG04_002500',1826377.039420815,6142543.448732315)"
        //        id="searchResListItem_001_40_OG04_002500-buildingfloorspace"
        //        class="list-group-item indrz-search-res">001_40_OG04_002500 <span class="badge">Ebene 4</span> </a>

        return htmlInsert;

}





function searchIndrz(campusId, searchString, zoomLevel) {

    var searchUrl = hostUrl + req_locale + '/search/' + searchString + '?format=json';

    if (searchLayer) {
        map.removeLayer(searchLayer);
        clearSearchResults();

    }

    var searchSource = new ol.source.Vector();

    indrzApiCall(searchUrl).then(function (response) {
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);

        searchSource.forEachFeature(function(feature) {

            var f_name = feature.get("name");

            var f_extent = feature.getGeometry().getExtent();
            var f_center = ol.extent.getCenter(f_extent);
            var zoom_coord = [f_center];

            var att = searchString;

            if (searchString === f_name){
                att = searchString;
            }else{
                att = f_name
            }

            var full_name = att;

            var featureNameGet = "category_"+ req_locale;

            var floor = feature.get("floor_num");
            var roomcat = feature.get(featureNameGet);
            var roomcode = feature.get('roomcode');
            var somethin = "";

            if(att !== roomcode){
                somethin = " (" + roomcode + ")"
            }else{
                somethin = ""

            }

            var f_id = "";
            var poiIconPath = "";


            if(feature.getProperties().hasOwnProperty('poi_id')){

                    f_id = feature.get("poi_id");
                    poiIconPath = feature.get("icon");
                    globalPopupInfo.poiId = feature.get("poi_id");
                    globalPopupInfo.src = feature.get("src")

            }else{
                globalPopupInfo.poiId = "noid";
                globalPopupInfo.src = feature.get("src")
            }


            var infoo = "'" + att + "'";
            var f_info = "'"+ feature + "'";

            if (roomcat !== "" && typeof roomcat !== 'undefined'){

                var resultListName = full_name + ' ('+ roomcat + ')';
                var htmlInsert = generateResultLinks(att, infoo, f_center, resultListName, floor, f_id, poiIconPath)

            }
            else if (roomcode !== "" && typeof roomcode !== 'undefined'){

                var className = full_name + somethin;
                var htmlInsert = generateResultLinks(att, infoo, f_center, className, floor, f_id, poiIconPath)

            }
            else{
                var className = full_name;
                var htmlInsert = generateResultLinks(att, infoo, f_center, className, floor, f_id, poiIconPath)


            }

            $("#search-results-list").append(htmlInsert);


            });


        var centerCoord = ol.extent.getCenter(searchSource.getExtent());

        if (featuresSearch.length === 1){

            open_popup(featuresSearch[0].getProperties(), centerCoord);
            zoomer(centerCoord, zoomLevel);

            space_id = response.features[0].properties.space_id;
            poi_id = response.features[0].properties.poi_id;
            search_text = searchString;

            // active the floor of the start point
            activateFloor(featuresSearch[0]);

        }else if (featuresSearch.length === 0){

            var htmlInsert = '<p href="#" class="list-group-item indrz-search-res" > ' + gettext("Sorry nothing found")  +'</p>';
            $("#search-results-list").append(htmlInsert);


        }else{

            var resExtent = searchSource.getExtent();
            map.getView().fit(resExtent);
            map.getView().setZoom(zoomLevel);

        }
        fixContentHeight();
    } );


    searchLayer = new ol.layer.Vector({
        source: searchSource,
        style: styleFunction,
        title: "SearchLayer",
        name: "SearchLayer",
        zIndex: 999
    });

    map.getLayers().push(searchLayer);
    window.location.href="#map";


    $('html,body').animate({
        scrollTop: $("#map").offset().top},
        'slow');

    $("#search-res").removeClass("hide");
    $("#clearSearch").removeClass("hide");
    $("#shareSearch").removeClass("hide");
    $("#searchTools").toggle(true); // show div tag

}

function initRoute(route_from, route_to){

        $.when(fetcherMd(route_from),fetcherMd(route_to)).then(function(a,b) {

        routeLocalData.start = {};
        routeLocalData.start.xcoord = a[0].features[0].properties.centerGeometry.coordinates[0];
        routeLocalData.start.ycoord = a[0].features[0].properties.centerGeometry.coordinates[1];
        routeLocalData.start.floor = a[0].features[0].properties.floor_num;
        var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;

        // console.log(routeStartValue);

        routeLocalData.start.routeValue = routeStartValue;

        routeLocalData.end = {};
        routeLocalData.end.xcoord = b[0].features[0].properties.centerGeometry.coordinates[0];
        routeLocalData.end.ycoord = b[0].features[0].properties.centerGeometry.coordinates[1];
        routeLocalData.end.floor = b[0].features[0].properties.floor_num;
        var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;

        routeLocalData.end.routeValue = routeEndValue;

        // console.log(a[0]);
        // console.log(b[0]);
        //
        // console.log(JSON.stringify(routeLocalData));
        // console.log("START IS "+a[0].features[0].properties);
        // console.log("END IS "+b[0].features[0].properties);

        // getDirections2(routeStartValue, routeEndValue,0);

         globalRouteInfo.startName = route_from;
         globalRouteInfo.endName =  route_to;
         globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=" + building_id + "&startstr=" + globalRouteInfo.startName + "&endstr=" + globalRouteInfo.endName + "&type=" + route_type;
        getDirections2(route_from, route_to, route_type, "string");
    });

}

function searchForRoute(startSearchText, endSearchText) {
    if (!startSearchText) {
        startSearchText = $('#route-from').val();
    }
    if (!endSearchText) {
        endSearchText = $('#route-to').val();
    }

    startSearchText = startSearchText.trim();
    endSearchText = endSearchText.trim();

    var route_type = 0;
    if ($("#routeTypeBarrierFree").is(":checked")) {
        route_type = 1;
    }
    // console.log('searchForRoute', startSearchText, endSearchText);

    if (!startSearchText.length > 0 || !endSearchText.length > 0) {
        console.warn('Invalid search fields');
        return;
    }

    $.when(fetcherMd(startSearchText), fetcherMd(endSearchText)).then(function (startPoint, endPoint) {

        // for each point we try to get the data based on source priority
        // 1. globalRouteInfo
        // 2. fetcher search results
        // 3. coordinate validation
        // 4. globalBookInfo

        // reset
        routeLocalData = {
            start: {},
            end: {}
        };

       // console.log("start point", startPoint);
       //  console.log("end point ", endPoint)

        var startPointProcessed = getCoordinatesFromGlobalRouteInfo('start');

        if (!startPointProcessed) {
            startPointProcessed = getCoordinatesFromResult(startPoint);

            if (!startPointProcessed) {
                startPointProcessed = getCoordinatesFromSearchText(startSearchText);

                if (!startPointProcessed) {
                    startPointProcessed = getCoordinatesFromGlobalBookInfo(startSearchText);
                }
            }
        }

        if (!startPointProcessed) {
            console.warn('no start point data for:' + startSearchText);
            return;
        }

        var endPointProcessed = getCoordinatesFromGlobalRouteInfo('end');

        if (!endPointProcessed) {
            endPointProcessed = getCoordinatesFromResult(endPoint);

            if (!endPointProcessed) {
                endPointProcessed = getCoordinatesFromSearchText(endSearchText);

                if (!endPointProcessed) {
                    endPointProcessed = getCoordinatesFromGlobalBookInfo(endSearchText);
                }
            }
        }

        if (!endPointProcessed) {
            console.warn('no end point data for:' + endSearchText);
            return;
        }

        var startPointText, endPointText;

        globalRouteInfo.startName = startSearchText;
        globalRouteInfo.endName =  endSearchText;

        if (startPointProcessed.poiId && endPointProcessed.poiId) {
           // console.log('routing poi to poi', startPointProcessed.poiId, endPointProcessed.poiId);

            routeToPoiFromPoi(startPointProcessed.poiId, endPointProcessed.poiId);

        } else if (startPointProcessed.poiId || endPointProcessed.poiId) {
            // console.log('routing from poi');

            var attributes = {};

            // correct way
            if (startPointProcessed.poiId) {
                startPointText = startPointProcessed.poiId;
                endPointText = endPointProcessed.xCoord + ',' + endPointProcessed.yCoord + '&floor=' + endPointProcessed.floorNum;
            } else {
                startPointText = endPointProcessed.poiId;
                endPointText = startPointProcessed.xCoord + ',' + startPointProcessed.yCoord + '&floor=' + startPointProcessed.floorNum;
                attributes.reversed = true;
            }

            getDirections2(startPointText, endPointText, route_type, "poiToCoords", attributes);
            globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" + startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;
        } else {
            console.log('routing from coords to coords');

            startPointText = startPointProcessed.xCoord + ',' + startPointProcessed.yCoord + ',' + startPointProcessed.floorNum;
            endPointText = endPointProcessed.xCoord + ',' + endPointProcessed.yCoord + ',' + endPointProcessed.floorNum;

            getDirections2(startPointText, endPointText, route_type, "coords");

            globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" + startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;

        }

        return;

            var poiToCoordsRoute = true;

            if (endPoint[0] && endPoint[0].features[0] !== undefined && endPoint[0].features[0].properties && endPoint[0].features[0].properties.centerGeometry !== undefined) {
                poiToCoordsRoute = false;
            }

            if (poiToCoordsRoute) {
                routeLocalData.start = {};

                routeLocalData.start.xcoord = startPoint[0].features[0].properties.centerGeometry.coordinates[0];
                routeLocalData.start.ycoord = startPoint[0].features[0].properties.centerGeometry.coordinates[1];
                routeLocalData.start.floor = startPoint[0].features[0].properties.floor_num;
                var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;

                routeLocalData.start.routeValue = routeStartValue;

                routeLocalData.end = {};
                var invalidCoordinatesPattern = /[^0-9,.\s]+/;

                if (globalRouteInfo.endCoord) {
                    routeLocalData.end.xcoord = globalRouteInfo.endCoord[0];
                    routeLocalData.end.ycoord = globalRouteInfo.endCoord[1];
                    routeLocalData.end.floor = globalRouteInfo.endFloor;
                } else if (!invalidCoordinatesPattern.test(endSearchText)) {
                    var coords = endSearchText.split(',');
                    routeLocalData.end.xcoord = coords[0];
                    routeLocalData.end.ycoord = coords[1];
                    if (coords.length > 2) {
                        routeLocalData.end.floor = coords[2];
                    } else {
                        routeLocalData.end.floor = 0;
                    }
                } else {
                    console.warn('no data');
                    return;
                }



                var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;

                routeLocalData.end.routeValue = routeEndValue;

                globalRouteInfo.startName = startSearchText;
                globalRouteInfo.endName = endSearchText;

                var poiId = globalRouteInfo.startPoiId;
                if (poiId === undefined) {
                    poiId = routeFromPoiIdTemp;
                }

                var endCoords = endSearchText + "&floor=" + routeLocalData.end.floor;

                getDirections2(poiId, endCoords, route_type, "poiToCoords");
                globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" + startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;


            } else {


                routeLocalData.start = {};

                routeLocalData.start.xcoord = startPoint[0].features[0].properties.centerGeometry.coordinates[0];
                routeLocalData.start.ycoord = startPoint[0].features[0].properties.centerGeometry.coordinates[1];
                routeLocalData.start.floor = startPoint[0].features[0].properties.floor_num;
                var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;

                routeLocalData.start.routeValue = routeStartValue;

                routeLocalData.end = {};
                routeLocalData.end.xcoord = endPoint[0].features[0].properties.centerGeometry.coordinates[0];
                routeLocalData.end.ycoord = endPoint[0].features[0].properties.centerGeometry.coordinates[1];
                routeLocalData.end.floor = endPoint[0].features[0].properties.floor_num;

                var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;

                routeLocalData.end.routeValue = routeEndValue;

                // console.log(a[0]);
                // console.log(b[0]);
                //
                // console.log(JSON.stringify(routeLocalData));
                // console.log("START IS "+a[0].features[0].properties);
                // console.log("END IS "+b[0].features[0].properties);

                // getDirections2(routeStartValue, routeEndValue,0, "coords");

                globalRouteInfo.startName = startSearchText;
                globalRouteInfo.endName = endSearchText;


                getDirections2(startSearchText, endSearchText, route_type, "string");
                globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" + startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;

            }
        });


}

function getCoordinatesFromResult(result) {
    var processedResult = false;

    if (
        result[0] !== undefined
        && result[0].features[0] !== undefined
        && result[0].features[0].properties !== undefined
        && result[0].features[0].properties.centerGeometry !== undefined
        && result[0].features[0].properties.centerGeometry.coordinates !== undefined
    ) {
        var coordinates = result[0].features[0].properties.centerGeometry.coordinates;

        if (Array.isArray(coordinates[0])) {
            coordinates = coordinates[0];
        }

        processedResult = {
            xCoord: coordinates[0],
            yCoord: coordinates[1],
            floorNum: result[0].features[0].properties.floor_num
        }
    } else {
        console.log('no data from result', result)
    }

    return processedResult;
}

function getCoordinatesFromGlobalRouteInfo(point) {
    var processedResult = false;

    switch (point) {
        case 'start':
            if (
                globalRouteInfo.startPoiId && globalRouteInfo.startPoiId !== 'noid'
                && globalRouteInfo.startPoiId && globalRouteInfo.startPoiId > 0
            ) {
                processedResult = {
                    poiId: globalRouteInfo.startPoiId
                }
            } else if (globalRouteInfo.startCoord) {
                processedResult = {
                    xCoord: globalRouteInfo.startCoord[0],
                    yCoord: globalRouteInfo.startCoord[1],
                    floorNum: globalRouteInfo.startFloor
                };
            }
            break;
        case 'end':
            if (
                globalRouteInfo.endPoiId && globalRouteInfo.endPoiId !== 'noid'
                && globalRouteInfo.endPoiId && globalRouteInfo.endPoiId > 0
            ) {
                processedResult = {
                    poiId: globalRouteInfo.endPoiId
                }
            } else if (globalRouteInfo.endCoord) {
                processedResult = {
                    xCoord: globalRouteInfo.endCoord[0],
                    yCoord: globalRouteInfo.endCoord[1],
                    floorNum: globalRouteInfo.endFloor
                };
            }
            break;
    }

    return processedResult;
}

function getCoordinatesFromSearchText(searchText) {
    var processedResult = false;
    var invalidCoordinatesPattern = /[^0-9,.\s]+/;

    if (!invalidCoordinatesPattern.test(searchText)) {
        var coords = searchText.split(',');

        if (coords.length < 2) {
            return processedResult;
        }

        processedResult = {
            xCoord: coords[0],
            yCoord: coords[1],
            floorNum: 0
        };

        if (coords.length > 2) {
            processedResult.floorNum = coords[2];
        }
    }

    return processedResult;
}

function getCoordinatesFromGlobalBookInfo(name) {
    var processedResult = false;

    if (globalBookInfo.hasOwnProperty(name.toUpperCase())) {
        processedResult = {
            xCoord: globalBookInfo[name].geometry.coordinates[0],
            yCoord: globalBookInfo[name].geometry.coordinates[1],
            floorNum: globalBookInfo[name].properties.floor_num
        };
    }

    return processedResult;
}

$("#clearSearch").click(function () {
    if (searchLayer) {
        map.removeLayer(searchLayer);
    }

    clearSearchResults();
    clearRouteData();

});


// function showRes(feature, x, y){
function showRes(featureName, x, y, poiId ){

    var center = [x,y];

    // if only one feature in list
    // if featureName is unique
    // get that feature and open_popup, zoomer, activateFloor

    // else get all unique names

    searchLayer.getSource().forEachFeature(function(feature) {

        var f_properties = feature.getProperties();

        var offSetPos = [0,-35];

        // console.log(feature.get('centerGeometry').coordinates);
        if (poiId !== 0 && typeof f_properties.hasOwnProperty('poi_id') !== "undefined"){

            if(f_properties.poi_id === poiId){
                // console.log(f_properties.poi_id);

                // createPoi(1,f_properties.name, poiId, f_properties);

                // console.log("yeessss");
               // popupCenterLocation = feature.get('centerGeometry').coordinates;

                open_popup(f_properties, center, -1, offSetPos);
                zoomer(center, 20);
                activateFloor(feature);

            }

        }else if (f_properties.name === featureName){
                 // popupCenterLocation = feature.get('centerGeometry').coordinates;
                open_popup(f_properties, center, -1, offSetPos);
                zoomer(center, 20);
                activateFloor(feature);

            }

    });

        $('html,body').animate({
        scrollTop: $("#map").offset().top},
        'slow');
}

// Generic function to make an AJAX call
var fetchData2 = function(text) {
    // console.log("IN FETCHDATA 2 : " + text);
    // Return the $.ajax promise
    return indrzApiCall("/search/" + text);
};

var fetcherMd = function(searchstring) {
    return indrzApiCall('/search/' + searchstring).done(function (data) {
        // If successful
        //console.log(data);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        //console.log(textStatus + ': ' + errorThrown);
    });
};

// var runRouteM = function(startP, endP) {
//     return indrzApiCall('/directions/' + startP + endP).done(function (data) {
//         // If successful
//         //console.log(data);
//     }).fail(function (jqXHR, textStatus, errorThrown) {
//         // If fail
//         //console.log(textStatus + ': ' + errorThrown);
//     });
// };


function eliminateDuplicates(arr) {
  var i,
      len=arr.length,
      out=[],
      obj={};

  for (i=0;i<len;i++) {
    obj[arr[i]]=0;
  }
  for (i in obj) {
    out.push(i);
  }
  return out;
}


function getAllSearchResultFeaturesNames(){
    all_feats = searchLayer.getProperties().source.getFeatures();
    names = [];
    for (i=0;i<all_feats.length;i++) {
        names.push(all_feats[i].getProperties().name);

    }
    return names
}


