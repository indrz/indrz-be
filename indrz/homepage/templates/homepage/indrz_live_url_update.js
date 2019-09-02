// map.on('moveend', function (e) {
//     update_url('map');
// });

function update_url(mode) {

    var current_extent2 = map.getView().calculateExtent(map.getSize());
    var current_zoom2 = map.getView().getZoom();
    var center_crd = map.getView().getCenter();
    var centerx2 = center_crd[0];
    var centery2 = center_crd[1];

    var url = "/?campus=" + building_id + "&centerx=" + centerx2 + "&centery=" + centery2 +
        "&zlevel=" + current_zoom2 + "&floor=" + active_floor_num;

    var data = {};

    if (mode === "route") {

        if(globalRouteInfo.routeUrl){
            // globalRouteInfo.routerUrl = false   is default
            // if some string in this property then use it
            url = globalRouteInfo.routeUrl;


        }else if(route_from_xyz !== ''){
            url = hostUrl + req_locale + "/?start-xyz=" + route_from_xyz + "&end-xyz=" + route_to_xyz;

        }else if(globalRouteInfo.startPoiId !== 'noid' && globalRouteInfo.endPoiId !== 'noid' || globalPopupInfo.poiId !== "noid"){
            url = globalRouteInfo.routeUrl;
        }else if (globalPopupInfo.poiId === 'undefined' && globalPopupInfo.poiId === "" && globalPopupInfo.poiId !== "noid"){
            url = "/?campus=" + building_id + "&startstr=" + globalRouteInfo.startName + "&endstr=" + globalRouteInfo.endName;
        }else{
            url = "/?campus=" + building_id + "&startstr=" + globalRouteInfo.startName + "&endstr=" + globalRouteInfo.endName;
        }


    } else if (mode === "search") {
        var popupData = createPopupData();

        if (globalPopupInfo.hasOwnProperty('external_id')){
            if(globalPopupInfo.external_id === globalPopupInfo.name){
                url = "/?campus=" + building_id + "&q=" + globalPopupInfo.external_id;

            }else{
                url = "/?campus=" + building_id + "&q=" + globalPopupInfo.name;

            }

        }

        if(globalSearchInfo.searchText){
            url = "/?campus=" + building_id + "&q=" + globalSearchInfo.searchText;
        }else {
            url = "/?campus=" + building_id + "&q=" + globalPopupInfo.name;
        }

        if (popupData.poiId ) {

            // http://localhost:8000/indrz/api/v1/campus/1/poi/251/
            // returns geojson feature of single poi location
            url = "/?poi-id=" + popupData.poiId +"&floor=" + popupData.floor_num;

        }
        // else{
        //     url = "/?campus=" + building_id + "&centerx=" + popupData.coords[0] + "&centery=" + popupData.coords[1] + "&zlevel=" + 21 + "&floor=" + active_floor_num;
        // }

    } else if (mode === "map") {
        url = "/?campus=" + building_id + "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 + "&floor=" + active_floor_num;
    }else if (mode === "bookId") {
        // url = hostUrl + "?campus=1&key=" + globalPopupInfo.bookId;
        url = hostUrl + globalRouteInfo.routeUrl;
        $(".share-link").val(url);
        $(".share-link").focus();
        $(".share-link").select();
    }else if (mode === "poiCatId"){

        url = hostUrl + globalPopupInfo.poiCatShareUrl;
        var urlSinglePoi = hostUrl + "?poi-id=" +  globalPopupInfo.poiId + "&floor=" + globalPopupInfo.floor;


        $(".share-link").val(url);
        $(".share-link-single-poi").val(urlSinglePoi);

        $(".share-link").focus();
        $(".share-link").select();


    }else if (mode === "wmsInfo"){

        url = hostUrl + "?campus=1&q=" + globalPopupInfo.wmsInfo;
        //
        // /?campus=1&q=Z.0.10

        $(".share-link").val(url);
        $(".share-link").focus();
        $(".share-link").select();

    }else{
        url = "woops"
    }

    data.extent = current_extent2;
    data.zoom = current_zoom2;
    history.pushState(data, 'live_url_update', url);
}


window.addEventListener('popstate', function (event) {
    updateContent(event.state);
});

function updateContent(data) {
    if (data == null)
        return;
}
