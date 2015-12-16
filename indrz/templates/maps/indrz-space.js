var spaceJSONURL = 'http://localhost:8000/api/v1/buildings/spaces/'+ space_id +'.json';

var space_source = new ol.source.Vector();
$.ajax(spaceJSONURL).then(function(response) {
    var geojsonFormat = new ol.format.GeoJSON();
    var features = geojsonFormat.readFeatures(response,
        {featureProjection: 'EPSG:4326'});
    space_source.addFeatures(features);
});
var style = new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(255, 255, 255, 0.6)'
    }),
    stroke: new ol.style.Stroke({
      color: '#319FD3',
      width: 1
    }),
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.6)'
      }),
      stroke: new ol.style.Stroke({
        color: '#319FD3',
        width: 1
      })
    })
});

var spaceLayer = new ol.layer.Vector({
    source: space_source,
    style:  style,
    title: "Space",
    name: "Space"
});

map.getLayers().push(spaceLayer);