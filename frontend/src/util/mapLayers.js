import { get as getProjection } from 'ol/proj';
import TileGrid from 'ol/tilegrid/WMTS';
import WMTS from 'ol/source/WMTS';
import TileLayer from 'ol/layer/Tile';
import ImageLayer from 'ol/layer/Image';
import ImageWMS from 'ol/source/ImageWMS';

const createWmtsLayer = function (layerSrcName, type, isVisible, sourceName) {
  const sm = getProjection('EPSG:3857');
  const templatepng =
    '{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}' +
    type;
  const urlsbmappng = [
    'https://maps1.wien.gv.at/basemap/' + templatepng,
    'https://maps2.wien.gv.at/basemap/' + templatepng,
    'https://maps3.wien.gv.at/basemap/' + templatepng,
    'https://maps4.wien.gv.at/basemap/' + templatepng
  ];
  const tilegrid = new TileGrid({
    origin: [-20037508.3428, 20037508.3428],
    extent: [977650, 5838030, 1913530, 6281290],
    resolutions: [
      156543.03392811998,
      78271.51696419998,
      39135.758481959994,
      19567.879241008,
      9783.939620504,
      4891.969810252,
      2445.984905126,
      1222.9924525644,
      611.4962262807999,
      305.74811314039994,
      152.87405657047998,
      76.43702828523999,
      38.21851414248,
      19.109257071295996,
      9.554628535647998,
      4.777314267823999,
      2.3886571339119995,
      1.1943285669559998,
      0.5971642834779999,
      0.29858214174039993,
      0.14929107086936
    ],
    matrixIds: [
      '0',
      '1',
      '2',
      '3',
      '4',
      '5',
      '6',
      '7',
      '8',
      '9',
      '10',
      '11',
      '12',
      '13',
      '14',
      '15',
      '16',
      '17',
      '18',
      '19',
      '20'
    ]
  });

  const WmtsTileSource = new WMTS({
    tilePixelRatio: 1,
    projection: sm,
    layer: layerSrcName,
    style: 'normal',
    matrixSet: 'google3857',
    urls: urlsbmappng,
    crossOrigin: 'anonymous',
    requestEncoding: /** @type {ol.source.WMTSRequestEncoding} */ ('REST'),
    tileGrid: tilegrid,
    attributions:
      '<a href="https://www.basemap.at/' + '" style="font-size: 10pt;">© Basemap.at</a>'
  });

  const wmtsLayer = new TileLayer({
    name: layerSrcName,
    source: WmtsTileSource,
    minResolution: 0.298582141738,
    visible: isVisible,
    type: 'background'
  });
  return wmtsLayer;
}

const greyBmapat = createWmtsLayer(
  'bmapgrau',
  '.png',
  true,
  'basemap.at'
);

const myMapLayer = new ImageLayer({
  source: new ImageWMS({
    url: 'http://localhost/geoserver/wms',
    params: { LAYERS: 'indrz:zoneplan_0_0', TILED: true },
    serverType: 'geoserver',
    crossOrigin: ''
  }),
  visible: true,
  name: 'mytestLayerName',
  floorNum: 0.0,
  floorName: 'EG',
  type: 'floor',
  zIndex: 2,
  crossOrigin: 'anonymous'
});

export { greyBmapat, myMapLayer };
