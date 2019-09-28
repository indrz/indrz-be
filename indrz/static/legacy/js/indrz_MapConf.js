var hostUrl = window.location.origin;
var req_locale = "en";
var baseApiUrl = hostUrl + 'api/v1/';
var baseApiRoutingUrl = baseApiUrl + 'directions/';
var baseApiSearchUrl = baseApiUrl + 'search';
var baseUrlWms = hostUrl + '/geoserver/indrz/wms';
var baseGeoserverUrl = "https://www.indrz.com/geoserver/";
var indrzApiToken = "Token 42519ebe7bada4d7a151c76832b94614ea5b198d";

var zoom_level = "16";
var campus_id = "(1,)";
var floor = "1";
var building_id = "1";
var floor_id = "";
var floor_num = "1";
var space_id = "0";
var poi_id = "none";
var poi_name = "";
var poi_cat_name = "none";
var poi_cat_id = [];
var poi_start_id = "-1";
var poi_end_id = "-1";
var poiActive = false;
var search_text = "";
var active_floor_num = "1";
var floor_layers = [];
var timer_waitfor_floor = null;
var building_info = null;
var map_name = "None";
var route_from = "";
var route_to = "";
var route_from_spaceid = "0";
var route_to_spaceid = "0";
var route_from_xyz = "";
var route_to_xyz = "";
var route_to_poi_id = "0"
var route_from_poi_id = "0"
var route_type = "0";
var centerx = "0";
var centery = "0";
var tempStart = [];
var tempEnd = [];
var routeLocalData = {};
var request = null;
var routeLayer = null;
var routeNearestPoiLayer = null;
var libraryRouteLayer = null;
var libraryMarkerLayer = null;
var bookLocationMarkerExact;
var markerLayer = null;
var routeDestinationName = "";
var library_key = "nokey";
var foo = {};
var globalBookInfo = {};
var globalPopupInfo = {
    "poiId": "noid",
    "poiCatId": "noid",
    "poiIdPopup": null,
    "poiCatName": null,
    "poiCatShareUrl": null,
    "bookId": false,
    "bookCoords": false,
    "name": false,
    "roomcode": null,
    'src': null,
    'floor': null,
    'coords': null,
    "spaceid": null,
    "wmsInfo": null
};
var globalRouteInfo = {
    "routeUrl": null,
    "endSpaceId": null,
    "startSpaceId": null,
    "endPoiId": null,
    "startPoiId": null,
    "bookUrl": null,
    "startCoord": null,
    "endCoord": null
};
var globalSearchInfo = {
    "searchText": false,
    "searchResult": false
}
var temp_route_data = {};
var current_poi_id = 0;


// var share_xy = "(&#39;&#39;,)"  // an array like [1826602.52,6142514.22]
var share_xy = [1822252.75, 6139984.70];
var StartCenterX = 1822252.75;
var StartCenterY = 6139984.70;
var CampusZoom = [StartCenterX, StartCenterY];


building_id = 1;
//
// var te = indrzApiCall(hostUrl +  req_locale + "/autocomplete/Hörsaal?format=json").done(function(data){return data})
// console.log(te)

var searchValues = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    // prefetch: baseApiUrl + 'spaces/search/?format=json',
    // local: te.responseJSON.length,
    // prefetch: {
    //     url: hostUrl + req_locale + '/autocomplete/Hörsaal?format=json',
    //     prepare: function(query, settings){
    //         settings.url = settings.url + query + "?format=json"
    //       settings.headers = {
    //           "Authorization": "Token 8473cc9b7c4e97627b3de5abc9b9d5a21929388a"
    //       }
    //       return settings;
    //   }
    // },
    remote: {
        url: hostUrl + 'autocomplete/',
        prepare: function (query, settings) {
            settings.url = settings.url + query + "?format=json"
            settings.headers = {
                "Authorization": indrzApiToken
            }
            return settings;
        },
        wildcard: '%QUERY'
    }
});

searchValues.initialize();


function styleIndrzAutocomplete(dataSource) {

    var person = "./img/autocomplete_person.png";
    var org = "./img/autocomplete_org.png";
    var room = "./img/autocomplete_room.png";
    var poi = "./img/autocomplete_poi.png";
    var icon = "./img/autocomplete_poi.png";

    if (dataSource.src === 'external person api') {

        icon = person;

    }

    if (dataSource.src === 'external organization api') {
        icon = org;
    }

    if (dataSource.src === "external rooms api" || dataSource.src === "indrz spaces") {
        icon = room;
    }

    if (dataSource.src === "indrz poi" || dataSource.src === "indrz poi cat") {
        icon = poi;
    }

    var extraText = "";

    if (dataSource.hasOwnProperty('roomcode') && dataSource.roomcode !== "" && dataSource.roomcode !==
        'undefined') {

        if (dataSource.roomcode === dataSource.name) {

            if (dataSource.category_de !== "") {
                // aau api 22.06.2018 has no EN category values change below when it dows
                // TODO
                if (req_locale === "de" || req_locale === "en") {
                    extraText = " (" + dataSource.category_de + ")";

                } else {
                    extraText = " (" + dataSource.category_en + ")";

                }

            } else {
                extraText = "";
            }

        } else {
            extraText = " (" + dataSource.roomcode + ")";

        }

    } else if (dataSource.hasOwnProperty('parent')) {

        if (dataSource.parent !== dataSource.name) {

            if (dataSource.parent === "Womens WC") {
                extraText = "";

            } else {
                extraText = " (" + dataSource.parent + ")";
            }

        } else {
            extraText = "";
        }

    } else {
        extraText = "";
    }

    if (dataSource !== "sorry nothing found") {
        var res = '<p id="indrzAutoComplete"><img style="margin-right:5px; height:20px; width:20px;" src=' +
            icon + '>' + dataSource.name + '<span style="font-size: 10px; color:#337ab7;">' + extraText +
            '</span> </p>';

    } else {
        var res = '<p id="indrzAutoComplete" >' + "Sorry nothing found" + '</p>';

    }

    return res;
}



// passing in `null` for the `options` arguments will result in the default
// options being used
$('#search-input').typeahead(null, {
    hint: true,
    highlight: true,
    minLength: 3,
    name: 'search-field',
    limit: 50,
    display: "name", // set which field key to display in autocomplete dropdown
    source: (function (ttadapter) {
        return function (query, process, x) {
            if (query.length < 3) {
                return false;
            }
            return ttadapter(query, process, x);
        };
    })(searchValues.ttAdapter()),
    templates: {
        empty: "Sorry nothing found",
        suggestion: function (data) {

            return styleIndrzAutocomplete(data)
        }
    }



    // templates: {
    //         empty: 'not found', //optional
    //         suggestion: function(el){return '<img src="https://encrypted-tbn0.g.com/images?q=tbn:ANd9GcREZsX_jcmMUqvVF3HW8-3dyjxZ9wZO4ugIvYQyj761-RYwcH91" />'+el.name}
    //     }


});

$('#search-input').on('typeahead:asyncrequest', function (type, dataset, query) {
    var searchElement = $('#search-input');
    var searchString = searchElement.val();

    if (searchString.length < 3) {
        searchElement.removeClass('spinner');
        return false;
    }
    searchElement.addClass('spinner');
});


$('#search-input').on('typeahead:asyncreceive', function (type, dataset, query) {
    $('#search-input').removeClass('spinner');
});



$('#search-input').on('typeahead:selected', function (e, item) {


    searchIndrz(building_id, item.name, 20);
    globalSearchInfo.searchText = item.name;
    fixContentHeight();



}).on('typeahead:autocompleted', function (e, item) {
    // console.log("autocompleted item: " + item);
}).on("keydown", function (e) {
    if (e.keyCode === 13) {
        // validate(e)
    }
});


function validate(e) {
    var text = e.target.value;
    // console.log("TEXT IS: "+ text);
    searchIndrz(building_id, text, zoom_level);
}


// $("#showPoi").submit(function (event) {
//    // alert( "Handler for .submit() called." + $('#poi-input').val()   );
//     var poiName = $('#poi-input').val();
//     searchPoi(building_id, poiName);
//     event.preventDefault();
//     });
//
//     var roomNums = new Bloodhound({
//     datumTokenizer: Bloodhound.tokenizers.whitespace,
//     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     prefetch: baseApiUrl + 'spaces/search/?format=json'
// });

// passing in `null` for the `options` arguments will result in the default
// options being used
$('#prefetch-start-location .typeahead').typeahead(null, {
    hint: true,
    highlight: true,
    minLength: 3,
    name: 'route-from-field',
    limit: 15,
    display: "name",
    source: searchValues,
    templates: {
        empty: "Sorry nothing found",
        suggestion: function (data) {

            if (data.src === "bach") {


            }
            return styleIndrzAutocomplete(data)
        }
    }
});

$('#prefetch-end-location .typeahead').typeahead(null, {
    hint: true,
    highlight: true,
    minLength: 3,
    name: 'route-to-field',
    limit: 15,
    display: "name",
    source: searchValues,
    templates: {
        empty: "Sorry nothing found",
        suggestion: function (data) {

            if (data.src === "bach") {


            }
            return styleIndrzAutocomplete(data)
        }
    }
});

function setGlobalRouteInfo(item, position) {

    if (position === 'from') {
        if (item.hasOwnProperty('name')) {
            globalRouteInfo.startName = item.name;
        }
        if (item.hasOwnProperty('centerGeometry')) {
            globalRouteInfo.startCoord = item.centerGeometry.coordinates;
        }

        if (item.hasOwnProperty('poi_id')) {

            if (item.poi_id) {
                globalRouteInfo.startPoiId = item.poi_id;
            }

        }

        if (item.hasOwnProperty('floor_num')) {
            globalRouteInfo.startFloor = item.floor_num;
        }


    }
    if (position === 'to') {
        if (item.hasOwnProperty('name')) {
            globalRouteInfo.endName = item.name;
        }
        if (item.hasOwnProperty('centerGeometry')) {
            globalRouteInfo.endCoord = item.centerGeometry.coordinates;
        }

        if (item.hasOwnProperty('poi_id')) {
            globalRouteInfo.endPoiId = item.poi_id;
        }

        if (item.hasOwnProperty('floor_num')) {
            globalRouteInfo.endFloor = item.floor_num;
        }

    }


}


$('#route-from').on('typeahead:selected', function (e, item) {
    // get_start(item);
    // getRouteToFromInfo(item,'start')

    // console.log(start_val);
    if (item) {
        $('#route-from').val(item.name);
        setGlobalRouteInfo(item, 'from');
    }

});

$('#route-to').on('typeahead:selected', function (e, item) {
    if (item) {
        $('#route-to').val(item.name);
        setGlobalRouteInfo(item, 'to');

    }

});


$("#enterRoute").on("click", function (event) {

    var startSearchText = $('#route-from').val();
    var endSearchText = $('#route-to').val();
    var route_type = 0;
    if ($("#routeTypeBarrierFree").is(":checked")) {
        route_type = 1;
    }

    if (globalRouteInfo.startSpaceId && globalRouteInfo.endSpaceId) {

        getDirections2(globalRouteInfo.startSpaceId, globalRouteInfo.endSpaceId, '0',
            'spaceIdToSpaceId')


    } else if (globalRouteInfo.startPoiId && globalRouteInfo.endSpaceId) {

        getDirections2(globalRouteInfo.endSpaceId, globalRouteInfo.startPoiId, '0', 'spaceIdToPoiId')

    } else if (globalRouteInfo.startPoiId && globalRouteInfo.endPoiId) {

        routeToPoiFromPoi(globalRouteInfo.startPoiId, globalRouteInfo.endPoiId)

    } else if (parseFloat(startSearchText.split(',')[0]) || parseFloat(endSearchText.split(',')[0])) {
        // then start and end are coordinates

        var startCoords = startSearchText;
        var endCoords = endSearchText;

        getDirections2(startCoords, endCoords, "0", "coords");


    } else if (!parseFloat.startSearchText && !parseFloat.endSearchText) {


        $.when(fetcherMd(startSearchText), fetcherMd(endSearchText)).then(function (a, b) {

            var poiToCoordsRoute = true;

            if (b[0] && b[0].features[0] && b[0].features[0].properties && b[0].features[0]
                .properties.centerGeometry) {
                poiToCoordsRoute = false;
            }

            var startSpaceId = a[0].features[0].properties.spaceid;
            var endSpaceId = b[0].features[0].properties.spaceid;



            console.log(a[0].features[0].properties.spaceid)

            if (startSpaceId && endSpaceId) {

                getDirections2(startSpaceId, endSpaceId, '0', 'spaceIdToSpaceId')
                globalRouteInfo.startSpaceId = startSpaceId;
                globalRouteInfo.endSpaceId = endSpaceId;

            } else if (!startSpaceId && !endSpaceId) {

                routeLocalData.start = {};

                routeLocalData.start.xcoord = a[0].features[0].properties.centerGeometry
                    .coordinates[0];
                routeLocalData.start.ycoord = a[0].features[0].properties.centerGeometry
                    .coordinates[1];
                routeLocalData.start.floor = a[0].features[0].properties.floor_num;
                var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start
                    .ycoord + "," + routeLocalData.start.floor;

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
                    return;
                }



                var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end
                    .ycoord + "," + routeLocalData.end.floor;

                routeLocalData.end.routeValue = routeEndValue;

                globalRouteInfo.startName = startSearchText;
                globalRouteInfo.endName = endSearchText;

                var poiId = globalRouteInfo.startPoiId;
                if (poiId === undefined) {
                    poiId = routeFromPoiIdTemp;
                }

                var endCoords = endSearchText + "&floor=" + routeLocalData.end.floor;

                getDirections2(poiId, endCoords, route_type, "poiToCoords");
                globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" +
                    startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;


            } else {


                routeLocalData.start = {};

                routeLocalData.start.xcoord = a[0].features[0].properties.centerGeometry
                    .coordinates[0];
                routeLocalData.start.ycoord = a[0].features[0].properties.centerGeometry
                    .coordinates[1];
                routeLocalData.start.floor = a[0].features[0].properties.floor_num;
                var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start
                    .ycoord + "," + routeLocalData.start.floor;

                routeLocalData.start.routeValue = routeStartValue;

                routeLocalData.end = {};
                routeLocalData.end.xcoord = b[0].features[0].properties.centerGeometry
                    .coordinates[0];
                routeLocalData.end.ycoord = b[0].features[0].properties.centerGeometry
                    .coordinates[1];
                routeLocalData.end.floor = b[0].features[0].properties.floor_num;

                var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end
                    .ycoord + "," + routeLocalData.end.floor;

                routeLocalData.end.routeValue = routeEndValue;

                globalRouteInfo.startName = startSearchText;
                globalRouteInfo.endName = endSearchText;


                getDirections2(startSearchText, endSearchText, route_type, "string");
                globalRouteInfo.routeUrl = hostUrl + req_locale + "/?campus=1&startstr=" +
                    startSearchText + "&endstr=" + endSearchText + "&type=" + route_type;

            }
        });

    }



    event.preventDefault();
});



$('#route-to').on('typeahead:asyncrequest', function (type, dataset, query) {
    $('#route-to').addClass('spinner');
});


$('#route-to').on('typeahead:asyncreceive', function (type, dataset, query) {
    $('#route-to').removeClass('spinner');
});

$('#route-from').on('typeahead:asyncrequest', function (type, dataset, query) {
    $('#route-from').addClass('spinner');
});


$('#route-from').on('typeahead:asyncreceive', function (type, dataset, query) {
    $('#route-from').removeClass('spinner');
});



function zoomToCampus() {

    view.animate({
        center: CampusZoom,
        duration: 2000,
        zoom: 17
    });

}

$("#id-zoom-to-campus-left").on("click", function (evt) {
    zoomToCampus();


});


$("#id-zoom-to-campus-map").on("click", function (evt) {

    zoomToCampus();

});

$("#enterSearchGoButton").click(function (e) {

    var searchString = $('#search-input').val();
    searchIndrz(building_id, searchString, 20);
    globalSearchInfo.searchText = searchString;
    e.preventDefault();

});
