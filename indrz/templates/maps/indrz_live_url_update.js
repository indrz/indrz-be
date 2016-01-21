map.on('moveend', function(e){
    update_url('map');
});

function update_url(mode) {
    var current_extent = map.getView().calculateExtent(map.getSize());
    var current_zoom = map.getView().getZoom();

    var center_crd = ol.extent.getCenter(current_extent);
    console.log(center_crd);

    var url = "/map/" + map_name + "/?buildingid=" + building_id +
        "&centerx=" + center_crd[0] + "&centery=" + center_crd[1] + "&zlevel=" + current_zoom +
        "&floor=" + active_floor_num;
    var data = {};

    if(mode == "route") {
        url = "/map/" + map_name + "/?buildingid=" + building_id + "&route_from=" + $("#route-from").val() + "&route_to=" + $("#route-to").val();
    } else if(mode == "search") {
        url = "/map/" + map_name + "/?buildingid=" + building_id + "&spaceid=" + space_id;
    }

    data.extent = current_extent;
    data.zoom = current_zoom;
    history.pushState(data, 'live_url_update', url);
}


window.addEventListener('popstate', function(event) {
    console.log("pop state");
    updateContent(event.state);
});

function updateContent(data) {
    if (data == null)
        return;
    console.log(data);
}
