var searchLayer = null;


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


function setSearchFeatureStyle (feature, resolution){
        if (feature) {

        if (feature.get('short_name') !== null) {
            //info.innerHTML = feature.getId() + ': ' + feature.get('name');
            search_res_style.getText().setText(resolution < 0.1 ? feature.get('short_name') : '');
            return [search_res_style];

        }
    }

}


function searchIndrz() {
    var searchUrl = '/api/v1/buildings/space/1348.json';


    if (searchLayer) {
        map.removeLayer(searchLayer);
        console.log("removing search layer now");
        //map.getLayers().pop();
    }


    var searchSource = new ol.source.Vector();
    $.ajax(searchUrl).then(function (response) {
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);
        var searchFloorId = featuresSearch[0].getProperties().fk_building_floor.id;
        map.getView().setCenter(ol.extent.getCenter(searchSource.getExtent()));
        map.getView().setZoom(21);
        waitForFloors(searchFloorId);

    });

    var searchLayer = new ol.layer.Vector({
        source: searchSource,
        style: setSearchFeatureStyle,
        title: "SearchLayer",
        name: "SearchLayer",
        zIndex: 999
    });

    map.getLayers().push(searchLayer);
    console.log("setting search layer now");

}