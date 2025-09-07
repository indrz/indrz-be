<template>
  <div>
    <div id="map" class="map">
      <pre id="info" />
    </div>

    <v-data-table
      v-if="featureProperties.length > 0"
      dense
      hide-default-footer
      :headers="tableHeaders"
      :items="featureProperties"
      class="elevation-1"
    />

    <div id="mouse-position" />
  </div>
</template>

<script>
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import MousePosition from 'ol/control/MousePosition';
import { createStringXY } from 'ol/coordinate';
import { defaults as defaultControls } from 'ol/control';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { greyBmapat } from '~/util/mapLayers';

export default {
  name: 'BaseMap',
  data () {
    return {
      map: null,
      center: [1822139.88, 6139957.53],
      zoom: 18,
      layers: {},
      activeLayers: [],
      selected: null,
      status: '',
      featureProperties: [],
      tableHeaders: [
        { text: 'Property', align: 'start', value: 'key' },
        { text: 'Value', value: 'value' }
      ]

    };
  },
  mounted () {
    this.initMap();
  },
  methods: {
    initMap () {
      const mousePositionControl = new MousePosition({
        coordinateFormat: createStringXY(4),
        projection: 'EPSG:3857',
        // comment the following two lines to have the mouse position
        // be placed within the map.
        className: 'custom-mouse-position',
        target: document.getElementById('mouse-position')
      });

      this.map = new Map({
        controls: defaultControls().extend([mousePositionControl]),
        target: 'map',
        layers: [
          // greyBmapat, myMapLayer
          greyBmapat
        ],
        view: new View({
          projection: 'EPSG:3857',
          center: this.center,
          zoom: this.zoom
        })
      });

      let selected = null;
      const selectStyle = new Style({
        fill: new Fill({
          color: '#f5ea2e'
        }),
        stroke: new Stroke({
          color: 'rgba(255, 255, 255, 0.7)',
          width: 2
        })
      });

      this.map.on('pointermove', (e) => {
        if (selected !== null) {
          selected.setStyle(undefined);
          selected = null;
        }

        this.map.forEachFeatureAtPixel(e.pixel, (f) => {
          if (selected !== f) {
            if (selected) {
              selected.setStyle(undefined);
            }
            selected = f;
            selectStyle.getFill().setColor(f.get('COLOR') || '#f5dd49');
            f.setStyle(selectStyle);
          }
          return true;
        });

        if (selected) {
          this.featureProperties = [
            { key: 'Code', value: selected.get('orgcode') },
            { key: 'Organization', value: selected.get('name') },
            { key: 'Main Use', value: selected.get('mainuse') },
            { key: 'Room Code', value: selected.get('room_code') }
          ];
        } else {
          this.featureProperties = [];
        }
      });
    },

    addLayer (layerName, color, geojsonData) {
      const defaultStyle = new Style({
        fill: new Fill({
          color: color
        }),
        stroke: new Stroke({
          color: '#575757',
          width: 1
        })
      });

      if (!this.layers[layerName]) {
        const vectorLayer = new VectorLayer({
          source: new VectorSource({
            features: new GeoJSON().readFeatures(geojsonData, {
              dataProjection: 'EPSG:3857',
              featureProjection: 'EPSG:3857'
            })
          }),
          style: defaultStyle
        });
        this.layers[layerName] = vectorLayer;
        this.map.addLayer(vectorLayer);
      }
    },
    removeLayer (layerName) {
      const layer = this.layers[layerName];
      if (layer) {
        this.map.removeLayer(layer);
        delete this.layers[layerName];
      }
    },
    toggleLayerVisibility (layerName, isVisible) {
      const layer = this.layers[layerName];
      if (layer) {
        layer.setVisible(isVisible);
      }
    }
  }
};
</script>

<style>
#map {
  width: 100%;
  height: 900px;
}
#info {
  z-index: 1;
  opacity: 0;
  position: absolute;
  bottom: 0;
  left: 0;
  margin: 0;
  background: rgba(0, 60, 136, 0.7);
  color: white;
  border: 0;
  transition: opacity 100ms ease-in;
}
</style>
