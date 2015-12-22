map.on('moveend', function(e){
    var current_extent = map.getView().calculateExtent(map.getSize());
    var current_zoom = map.getView().getZoom();

    var url = "/map/" + map_name + "/left=" + current_extent[0] + "&right=" + current_extent[2] +
        "&top=" + current_extent[3]+"&bottom=" + current_extent[1] + "&campusid=4&zlevel=" + current_zoom;
    var data = {};
    data.extent = current_extent;
    data.zoom = current_zoom;
    history.pushState(data, 'live_url_update', url);
});

window.addEventListener('popstate', function(event) {
    console.log("pop state");
    updateContent(event.state);
});

function updateContent(data) {
    if (data == null)
        return;
    console.log(data);
}
