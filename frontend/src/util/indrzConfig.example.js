const baseApiUrl = 'http://localhost:8000/api/v1/';

export default {
  baseApiUrl, // api base url to serve frontend
  baseWmsUrl: 'http://localhost:8080/geoserver/wms', // web map server geoserver base url
  defaultCenterXY: [1823820.8003225543, 6138685.150457315],
  searchUrl: baseApiUrl + 'search', // search api url
  token: 'Token 1234mumbojumbo1234', // your server generated token, keep privat
  layerNamePrefix: 'floor_', // geoserver layer names all start with this
  geoServerLayerPrefix: 'indrztu:', // geoserver layer workspace name
  defaultStartFloor: 'eg', // floor name that app should load on first page load
  debug: true,
  defaultLanguage: 'en'
}
