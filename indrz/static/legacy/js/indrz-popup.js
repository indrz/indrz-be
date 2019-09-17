var popup_container = document.getElementById('indrz-popup');
var popup_container_plain = document.getElementById('indrz-popup-plain');
var popup_content = document.getElementById('popup-content');
var popup_links = document.getElementById('popup-links');
var popup_closer = document.getElementById('popup-closer');

var selectRoom = new ol.interaction.Select({
    style: show_poi_search_style
});

/**
 * Create an overlay to anchor the popup to the map.
 */
var popup_overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
    element: popup_container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    },
    zIndex: 5,
    name: "indrzPopup"
}));


function closeIndrzPopup() {

    for (var member in globalPopupInfo) globalPopupInfo[member] = null;
    for (var st in globalSearchInfo) globalSearchInfo[st] = false;
    popup_overlay.setPosition(undefined);
    popup_closer.blur();

    // clear the selected feature since it copies it to another layer
    selectRoom.getFeatures().clear();

    globalPopupInfo.poiId = "noid";
    globalPopupInfo.poiCatId = "noid";
    globalPopupInfo.bookId = false;
    globalPopupInfo.bookCoords = false;
    globalPopupInfo.name = false;

    globalRouteInfo.bookUrl = false;
    library_key = "nokey";


    // globalRouteInfo.routeUrl = false;

    // indrzRemoveLayerById(globalPopupInfo.poiId);

    // if (searchLayer) {
    //     map.removeLayer(searchLayer);
    //     //map.getLayers().pop();
    // }
    // map.getLayers().pop();
    return false;
}


popup_closer.onclick = function () {
    closeIndrzPopup();
};


map.addOverlay(popup_overlay);

map.addInteraction(selectRoom);

function getRoomInfo(floor) {

    // if (floor === "-1") {
    //     var floor_param = "indrz:ug01_space_polys"
    // } else {
    //     floor_param = 'indrz:e0' + floor + '_space_polys';
    // }

    var availableWmsLayers = [wmsE00, wmsE01, wmsE02, wmsE03];
    var newel;

    availableWmsLayers.forEach(function(element){

        if(floor === element.getProperties().floor_num ){
            // console.log("matcheer");

            newel = element.getSource();
            // console.log(element.getProperties());

        }



    });

    // console.log(newel);

    return newel;


    // var wmsSource2 = new ol.source.ImageWMS({
    //     url: "https://campusplan.aau.at/geoserver2112/indrz/wms",
    //     params: {'LAYERS': floor_param},
    //     serverType: 'geoserver',
    //     crossOrigin: 'anonymous'
    // });
    //
    //
    // return wmsSource2;

}


var displayFeatureInfo = function (pixel) {

    var feature = map.getFeaturesAtPixel(pixel);

    var features = [];

    map.forEachFeatureAtPixel(pixel, function (feature, layer) {
        features.push(feature);
    });

    // take the first feature hit by click
    // many features could be at same xy but different floors
    feature = features[0];

    if (feature) {

        var coordinate;
        var properties = {};



        if (feature.getGeometry().getType() === "MultiPolygon" || feature.getGeometry().getType() === "MultiPoint") {
            closeIndrzPopup();

            coordinate = map.getCoordinateFromPixel(pixel);
            properties = feature.getProperties();

             if (feature.getGeometry().getType() === "MultiPoint"){
               properties.poiId = feature.getId();
               properties.src = "poi";
             }

            open_popup(properties, coordinate, feature);
            activateFloor(feature);


        } else if (feature.getGeometry().getType() === "Point") {


            closeIndrzPopup();

            properties = feature.getProperties();

            coordinate = map.getCoordinateFromPixel(pixel);
            properties = feature.getProperties();

            properties.src = "poi"

            if (feature.getProperties().hasOwnProperty('poi_id')) {
                properties.poiId = feature.properties.poi_id
            }

            open_popup(properties, coordinate, feature);
            activateFloor(feature);


        }


    } else {

          var featuresWms = map.getFeaturesAtPixel(pixel)

          coordinate = map.getCoordinateFromPixel(pixel)

          floorNum = active_floor_num

          // document.getElementById('info').innerHTML = '';
          var v = map.getView()
          var viewResolution = /** @type {number} */ (v.getResolution())

          var wmsSource2 = getRoomInfo(active_floor_num)

          var url = wmsSource2.getGetFeatureInfoUrl(
            coordinate, viewResolution, 'EPSG:3857',
            {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50})

          if (url) {

            $.ajax(url).then(function (response) {

              globalPopupInfo.src = 'wms'
              var listFeatures = response.features
              var propertiesPresent = response.features && response.features[0] && response.features[0].properties
              var data_properties = {}

              if (listFeatures.length > 0) {

                listFeatures.forEach(function (feature) {

                  if (feature.properties.hasOwnProperty('space_type_id')) {

                    if (feature.properties.hasOwnProperty('room_code') || feature.properties.hasOwnProperty('roomcode')) {

                      var centroidSource = new ol.source.Vector({
                        features: (new ol.format.GeoJSON()).readFeatures(feature)
                      })

                      var centroid_coords = ol.extent.getCenter(centroidSource.getExtent())

                      data_properties.properties = feature.properties
                      data_properties.centroid = centroid_coords

                    }

                  }

                })

                data_properties.properties.src = "wms"

                open_popup(data_properties.properties, data_properties.centroid, featuresWms)

              }

            })

          }
        }

};

map.on('singleclick', function (evt) {
    var pixel = evt.pixel;
    displayFeatureInfo(pixel);
});


function getTitle(properties) {

    var name = "";
    var popup_roomcode = "";


    if (properties.hasOwnProperty('room_code')) {

        if (properties.room_code) {
            popup_roomcode = properties.room_code;
            name = properties.room_code;

        }

    }

    if (properties.hasOwnProperty('name')) {

        if (properties.name) {
            name = properties.name;
            return name
        }

    }


    if (properties.hasOwnProperty('name_de')) {

        if (properties.name_de) {

            if (req_locale === "de") {
                name = properties.name_de;
                return name
            } else {
                name = properties.name;
                return name
            }

        }

    }

    if (properties.hasOwnProperty('short_name')) {


        if (properties.short_name) {

            name = properties.short_name;
            return name
        } else if (popup_roomcode) {

            name = popup_roomcode;
            return name
        }

    }

    if (properties.hasOwnProperty('label')) {

        if (properties.label) {
            name = properties.label;
            return name;

        } else if (popup_roomcode) {
            name = popup_roomcode;
            return name
        }

    }

    if (properties.hasOwnProperty('key')) {

        if (properties.key) {
            name = properties.key;
            return name;

        } else if (popup_roomcode) {
            name = popup_roomcode;
            return name
        }

    }

    if (properties.hasOwnProperty('campus_name')) {

        if (properties.campus_name) {
            name = properties.campus_name;
            return name;

        } else if (popup_roomcode) {
            name = popup_roomcode;
            return name
        }

    }

    if (properties.hasOwnProperty('room_external_id'))
        if (properties.room_external_id) {
            if (!name) {
                name = properties.room_external_id;
                return name;
            }
        }

    if (properties.room_code) {
        name = properties.room_code;
        return name;
    } else {
        return name;
    }

}

function getBuildingLetter(p) {
    var buildingLetter;

    if (p.hasOwnProperty('roomcode')) {

        if (p.roomcode) {

            buildingLetter = p.roomcode.split(".")[0];
            return buildingLetter
        }

    }
    else if (p.hasOwnProperty('building_name')) {

        if (p.building_name !== null || p.building_name !== "" || typeof p.building_name !== 'undefined') {
            buildingLetter = p.building_name;
            return buildingLetter;
        }

    }
    else {
        var empty = "";
        return empty
    }
}


function addPoiTableRow(row1, row2, idname) {
    var table = document.getElementById("popupTable");


  if(idname === 'popupHomepage'){

    console.log('<a target="_blank" href="' + row2 + '">' + row2 + '</a>');

    row2 = '<a target="_blank" href="' + row2 + '">' + row2 + '</a>';
  }

    // if(idname ==="popupHomepage"){
    //   row2 = '<a href="' + row2 + '>':
    // }

    var row = table.insertRow(0);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);

    cell1.innerHTML = row1;
    cell2.innerHTML = row2;

    cell1.setAttribute('class', 'no-wrap');
    cell2.setAttribute("id", idname);

}


var routeToValTemp = "";
var routeToPoiIdTemp = "";
var routeFromValTemp = "";
var routeFromPoiIdTemp = "";
var objCenterCoords = "";
var floorNum;


function open_popup(properties, coordinate, feature, offsetArray) {
  // TODO reset globalPopInfo values all to null on start !
      for (var member in globalPopupInfo) globalPopupInfo[member] = null

      feature = (typeof feature !== 'undefined' && feature !== null) ? feature : -1
      offsetArray = typeof offsetArray !== 'undefined' ? offsetArray : [0, 0]

      var name_popup = properties.name

      var indrzLibraryShelf = ''

      if(properties.hasOwnProperty('poiId')) {

        globalPopupInfo.src = "poi";
        globalPopupInfo.poiId = properties.poiId;
      }


      if(properties.hasOwnProperty('fk_poi_category')){

        globalPopupInfo.src = "poi";
        globalPopupInfo.poiCatId = properties.fk_poi_category.id;


      }

      if (properties.hasOwnProperty('spaceid')) {

        globalPopupInfo.spaceid = properties.spaceid

      }

      var popup_homepage = null

      if (properties.hasOwnProperty('homepage')) {

        if (properties.homepage) {
          popup_homepage = properties.homepage

        }

      }


      if (properties.hasOwnProperty('src')) {

          if (properties.src) {
            globalPopupInfo.src = properties.src
          }

        }


      if (properties.hasOwnProperty('space_type_id')) {

        if (properties.hasOwnProperty('src')) {

          if (properties.src) {
            globalPopupInfo.src = properties.src
          } else {
            globalPopupInfo.src = 'wms'

          }

        }

        if (properties.hasOwnProperty('id')) {

          globalPopupInfo.spaceid = properties.id

        }

        if (properties.hasOwnProperty('room_external_id')) {

          if (properties.room_external_id) {

            globalPopupInfo.external_id = properties.room_external_id
          }

        }

      }

      if (properties.hasOwnProperty('room_code')) {

        globalPopupInfo.wmsInfo = properties.room_code
        properties.roomcode = properties.room_code

      }


    if (properties.hasOwnProperty('poi_id')) {
        current_poi_id = properties.poi_id;
        globalPopupInfo.poiId = properties.poi_id;
        if (properties.hasOwnProperty('fk_poi_category')) {

            globalPopupInfo.poiCatId = properties.fk_poi_category.id;
            if (req_locale === "de") {
                globalPopupInfo.poiCatName = properties.fk_poi_category.cat_name_de;
            } else {
                globalPopupInfo.poiCatName = properties.fk_poi_category.cat_name_en;
            }
            // globalPopupInfo.poiCatName = properties.fk_poi_category.cat_name;
            globalPopupInfo.poiCatShareUrl = hostUrl + "?poi-cat-id=" + globalPopupInfo.poiCatId;

        }


    } else if (feature !== -1) {
        if (globalPopupInfo.poiId === "noid") {
            if (
                typeof feature !== 'string'
                && feature.getId()
            ) {
                globalPopupInfo.poiId = feature.getId();
                globalPopupInfo.poiIdPopup = feature.getId();

                // globalRouteInfo.startPoiId = feature.getId();
                if (feature.get('fk_poi_category')) {
                    globalPopupInfo.poiCatId = feature.get('fk_poi_category').id;

                    if (req_locale === "de") {
                        globalPopupInfo.poiCatName = feature.get('fk_poi_category').cat_name_de;
                    } else {
                        globalPopupInfo.poiCatName = feature.get('fk_poi_category').cat_name_en;
                    }
                    // globalPopupInfo.poiCatName = feature.get('fk_poi_category').cat_name;

                    globalPopupInfo.poiCatShareUrl = hostUrl + "?poi-cat-id=" + globalPopupInfo.poiCatId;
                }


            }

        }

    }

    if (globalPopupInfo.poiId !== "noid") {

        globalPopupInfo.poiCatShareUrl = "?poi-cat-id=" + globalPopupInfo.poiCatId;
        // globalRouteInfo.startPoiId = globalPopupInfo.poiId;

    }


    objCenterCoords = coordinate;

    if (objCenterCoords || objCenterCoords !== '') {
        objCenterCoords = coordinate
    }
    else {
        objCenterCoords = properties.centerGeometry.coordinates;
    }
    var titlePopup = "";
    var titleBuildingName = gettext('Building: ');
    var titleFloorNumber = gettext('Floor Number: ');
    var titleRoomcode = gettext('Room Number: ');
    var titleRoomCat = gettext('Category: ');
    var titleFrontOffice = gettext('Front Office: ');
    var titleNearestEntrance = gettext('Entrance: ');
    var titleHomepage = gettext('Homepage: ');

    //var name;

    var buildingName = getBuildingLetter(properties);
    var roomcode = null;
    var roomCat;


    if(properties.hasOwnProperty('category_de')){

        if (properties.category_de) {
            if (req_locale === "de") {
                roomCat = properties.category_de;
            } else {
                roomCat = properties.category_en;
            }
        }


    }

    if(properties.hasOwnProperty('room_description')){
        properties.name = properties.room_description;
    }else if(properties.hasOwnProperty('short_name')){
        properties.name = properties.short_name;
    }

    if(properties.hasOwnProperty('room_code')){
        properties.roomcode = properties.room_code;
    }

    titlePopup = getTitle(properties);

    routeToValTemp = titlePopup;

    // TODO fix this property
    if (properties.hasOwnProperty('centroid') === true) {
        // data coming from click on rooms polyon by user and generate centroid

        routeToValTemp = properties.centroid;

    }





    var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

    if (typeof properties.label !== 'undefined') {
        //var properties = properties[0].properties;

        popupTitle = properties.label;
        floorNum = properties.floor_num;
        // buildingName = properties.building_name;
        roomcode = properties.roomcode;
    } else {
        floorNum = properties.floor_num;
        // buildingName = properties.building_name;
        roomcode = properties.roomcode;
    }

    var tb = '<table id="popupTable" style="user-select: text;"></table>';


    popup_content.innerHTML = '<h4 style="user-select: text;">' + titlePopup + '</h4>';
    popup_content.innerHTML += '<div><p>';
    popup_content.innerHTML += tb;

    // popup_content.innerHTML += titleFloorNumber + floorNum + '<br>';

    if(typeof floorNum === 'undefined'){
        floorNum = active_floor_num;
    }

    if(properties.hasOwnProperty('campus_name')){

      $('#popup-links').hide();

    }else{

                  $('#popup-links').show();

                  // TODO links from AAU api are old and wrong
                  // if (popup_homepage){
                  //   addPoiTableRow(titleHomepage, popup_homepage, 'popupHomepage')
                  // }

                        if (typeof properties.building_name !== 'undefined' && properties.building_name !== "") {
                      // popup_content.innerHTML += titleBuildingName + buildingName + '<br>';
                      addPoiTableRow(titleBuildingName, buildingName, "popupBuilding");
                  }

                  if (properties.hasOwnProperty('shelfID')) {
                      // indrzLibraryShelf = properties.shelfID;
                      // addPoiTableRow("Shelf: ", indrzLibraryShelf, "popupBuilding");
                      addPoiTableRow(titleBuildingName, properties.building, "popupBuilding");
                  }

                  if (roomcode) {
                      // popup_content.innerHTML += titleRoomcode + roomcode + '<br>';
                      addPoiTableRow(titleRoomcode, roomcode, "popupRoomCode");
                  }

                  if (roomCat) {
                           addPoiTableRow(titleRoomCat, roomCat, "popupRoomCat");
                  }

                  if (properties.room_external_id) {
                      // popup_content.innerHTML += titleRoomCat + roomCat + '<br>';
                      addPoiTableRow("Room Code", properties.room_external_id, "popupSpaceAks");
                  }

                  if (typeof(floorNum) === "undefined") {
                      floorNum = active_floor_num;
                  }
                  addPoiTableRow(titleFloorNumber, floorNum, "popupFloorNumber");





          // this function gets the nearest entrance for the selected feature shown in the popup
          // $.getJSON("/en/indrz/api/v1/directions/near/coords=" + coordinate + "&floor=" + floorNum + "&poiCatId=13/?format=json", function (data) {
          //
          //     }).done(function (pooor) {
          //
          //
          //
          //
          //         globalRouteInfo.startPoiId = pooor.id;
          //
          //         if (properties.floor_num === floorNum) {
          //
          //             addPoiTableRow(titleNearestEntrance, pooor.name, "popupNearestEntrance");
          //
          //         }
          //
          //
          //
          //
          //     }).always(function (foo) {
          //
          //     });



    }



    if(globalPopupInfo.roomcode){
      routeFromValTemp = globalPopupInfo.roomcode;
    }else if (roomcode) {
      routeFromValTemp = roomcode
    }else if (globalPopupInfo.name){
      routeFromValTemp = globalPopupInfo.name;
    }else if (titlePopup){
      routeFromValTemp = titlePopup;

    }



    popup_content.innerHTML += '</p></div>';

    globalPopupInfo.name = titlePopup;
    globalPopupInfo.coords = objCenterCoords;
    globalPopupInfo.floor = floorNum;
    globalPopupInfo.roomcode = roomcode;


    // uncomment below to show the coordinate in popup
    // popup_content.innerHTML += '<p>' + gettext('Coordinate: ')+ '</p><code>' + coordinate + '</code><p></p><code>' + hdms + '</code>';

    popup_overlay.setPosition(coordinate);
    popup_overlay.setOffset(offsetArray);
}

$(function () {
    $("#routeFromHere").click(function () {
            globalRouteInfo.startPoiId = null;

            if(globalPopupInfo.hasOwnProperty('spaceid')){
                globalRouteInfo.startSpaceId = globalPopupInfo.spaceid;
            }

            if(globalPopupInfo.hasOwnProperty('poiId')){
                globalRouteInfo.startPoiId = globalPopupInfo.poiId;
            }

            globalRouteInfo.startName = routeFromValTemp

            $('#collapseRouting').collapse('show');
            $('#collapsePoi').collapse('hide');


            document.getElementById('route-from').value = routeFromValTemp;
            routeFromPoiIdTemp = globalPopupInfo.poiId;

        }
    );

    $("#routeToHere").click(function () {
            globalRouteInfo.endPoiId = null;

            if(globalPopupInfo.hasOwnProperty('spaceid')){
                globalRouteInfo.endSpaceId = globalPopupInfo.spaceid;
            }

            if(globalPopupInfo.hasOwnProperty('poiId')){
                globalRouteInfo.endPoiId = globalPopupInfo.poiId;
            }


            globalRouteInfo.endName = routeToValTemp;


            document.getElementById('route-to').value = routeToValTemp;
            $('#collapseRouting').collapse('show');
            $('#collapsePoi').collapse('hide');
            routeToPoiIdTemp = globalPopupInfo.poiId;

        }
    )
});


function createPopupData() {
    var popupBuilding = $("#popupBuilding").text();
    var popupRoomCode = $("#popupRoomCode").text();
    var popupFloorNumber = $("#popupFloorNumber").text();
    var popupRoomCat = $("#popupRoomCat").text();
    var popupPoiId = "";

    if (globalPopupInfo.poiId !== -1 || globalPopupInfo.poiId !== "-1") {
        popupPoiId = globalPopupInfo.poiId;
    } else if (poi_id !== "" && poi_id !== 0 && poi_id !== "0") {
        popupPoiId = poi_id;
    }

    var pData = {
        "poiId": popupPoiId,
        "building": popupBuilding,
        "roomcode": popupRoomCode,
        "floor_num": popupFloorNumber,
        "category": popupRoomCat,
        "coords": objCenterCoords
    };

    return pData;
}


$("#shareSearchPopup").click(function () {

        if (globalPopupInfo.bookId) {
            $('#ShareBookModal').modal('show');
            update_url('bookId');

        }
        if (globalSearchInfo.searchText) {

            $('#ShareSearchModal').modal('show');
            update_url('search');

        }

        if (globalPopupInfo.poiCatId) {
            $('#SharePoiModal').modal('show');
            update_url('poiCatId');

        }
        if (globalPopupInfo.src === "wms") {

            $('#ShareSearchModal').modal('show');
            update_url('wmsInfo');

        }


    }
);

$(function () {
    $("#routeFromTrain").click(function () {

            document.getElementById('route-to').value = globalPopupInfo.name;

            if(globalPopupInfo.src === 'wms' && globalPopupInfo.roomcode === null){
                // 27 is the id of poi_category UNDERGROUND
                routeToNearestPoi(objCenterCoords, floorNum, 27, 'true', routeFromValTemp, globalPopupInfo.poiId, false);
            }else{
                routeToNearestPoi(objCenterCoords, floorNum, 27, 'true', routeFromValTemp, globalPopupInfo.poiId, true);

            }


            $('#collapseRouting').collapse('show');
            $('#collapsePoi').collapse('hide');

        }
    )
});


$(function () {
    $("#routeFromBuildingEntrance").click(function () {
            document.getElementById('route-to').value = globalPopupInfo.name;

            if(globalPopupInfo.src === 'wms' && globalPopupInfo.roomcode === null){
                routeToNearestPoi(objCenterCoords, floorNum, 13, 'true', routeFromValTemp, globalPopupInfo.poiId, false);
            }else{
                routeToNearestPoi(objCenterCoords, floorNum, 13, 'true', routeFromValTemp, globalPopupInfo.poiId, true); // 13 is the id of poi_category Building Entrance

            }



            // document.getElementById('route-from').value = "foo";
            $('#collapseRouting').collapse('show');
            $('#collapsePoi').collapse('hide');
            // $("#enterRoute").trigger('click');

            // closeIndrzPopup();


        }
    )
});


$("#routeToDefi").click(function () {

    document.getElementById('route-from').value = routeFromValTemp;

            if(globalPopupInfo.src === 'wms' && globalPopupInfo.roomcode === null){
                // 71 is id of Defibralator poi category
                routeToNearestPoi(objCenterCoords, floorNum, 71, 'false', routeFromValTemp, globalPopupInfo.poiId, false);
            }else{
                routeToNearestPoi(objCenterCoords, floorNum, 71, 'false', routeFromValTemp, globalPopupInfo.poiId, true); // 13 is the id of poi_category Building Entrance

            }


    $('#collapseRouting').collapse('show');
    $('#collapsePoi').collapse('hide');
    // $("#enterRoute").trigger('click');


    // closeIndrzPopup();


});


