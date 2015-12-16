  var space_source = new ol.source.Vector({
    url: 'http://localhost:8000/api/v1/buildings/spaces/'+ space_id +'.json',
    format: new ol.format.GeoJSON()
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
  var vectorLayer = new ol.layer.Vector({
    source: space_source,
    style: style
  });

  var view = map.getView()

  map.getLayers().push(vectorLayer);

  var feature = space_source.getFeatures()[0];
  var polygon = /** @type {ol.geom.SimpleGeometry} */ (feature.getGeometry());
  var size = /** @type {ol.Size} */ (map.getSize());
  view.fit(
      polygon,
      size,
      {
        padding: [170, 50, 30, 150],
        constrainResolution: false
      }
  );