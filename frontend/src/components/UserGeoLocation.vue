<template>
  <div>
    <div id="indrz-geolocation" class="ol-control ol-unselectable geolocation">
      <button class="default" title="Locate me" />
    </div>
    <div id="re-center-geolocation" class="ol-control ol-unselectable">
      <button @click="onRecenterButtonClick" title="Re-center me" class="inactive" />
    </div>
  </div>
</template>

<script>
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import Control from 'ol/control/Control';
import { fromLonLat } from 'ol/proj';
import Style from 'ol/style/Style';
import CircleStyle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';

export default {
  name: 'UserGeoLocation',
  props: {
    map: {
      type: Object,
      default: function () {
        return {};
      }
    }
  },
  data () {
    return {
      source: null,
      layer: null,
      watchId: null,
      userCenter: []
    };
  },
  computed: {
    locationButton () {
      const container = document.getElementById('indrz-geolocation');
      const button = container.getElementsByTagName('button');
      const classList = button[0].classList;
      return {
        container,
        button,
        classList
      }
    },
    reCenterButton () {
      const container = document.getElementById(('re-center-geolocation'));
      const button = container.getElementsByTagName('button');
      const classList = button[0].classList;
      return {
        container,
        button,
        classList
      }
    }
  },
  watch: {
    map: function (newValue) {
      this.addControl();
    }
  },
  mounted () {
    this.$root.$on('map-moved', (coOrdinate) => {
      if (this.userCenter.length &&
        (coOrdinate[0] !== this.userCenter[0] || coOrdinate[1] !== this.userCenter[1])
      ) {
        this.handleRecenterButtonVisibility();
      }
    })
  },
  methods: {
    addControl () {
      this.source = new VectorSource();
      this.layer = new VectorLayer({
        source: this.source
      });

      this.map.addLayer(this.layer);
      this.locationButton.container.addEventListener('click', () => {
        const isActiveButton = this.locationButton.classList.contains('active');

        this.clearWatch();
        if (!isActiveButton) {
          this.addToWatch();
        }
      });

      this.map.addControl(new Control({
        element: this.locationButton.container
      }));
    },

    hidRecenterButton () {
      this.reCenterButton.classList.add('inactive');
    },

    showRecenterButton () {
      this.reCenterButton.classList.remove('inactive');
    },

    handleRecenterButtonVisibility () {
      if (this.watchId) {
        this.showRecenterButton();
      }
    },

    clearWatch () {
      this.source.clear(true);
      this.locationButton.classList.remove('active');

      if (this.watchId) {
        navigator.geolocation.clearWatch(this.watchId);
        this.watchId = null;
      }

      this.hidRecenterButton();
    },

    addToWatch () {
      this.watchId = navigator.geolocation.watchPosition((pos) => {
        const coords = [pos.coords.longitude, pos.coords.latitude];

        this.userCenter = fromLonLat(coords);
        this.source.clear(true);
        this.source.addFeatures([
          this.getPositionFeature(this.userCenter)
        ]);
        this.map.getView().fit(this.source.getExtent(), {
          maxZoom: 18,
          duration: 500
        });

        this.locationButton.classList.add('active');
      }, (error) => {
        alert(`ERROR: ${error.message}`);
        this.locationButton.classList.remove('active');
      }, {
        enableHighAccuracy: true
      });
    },

    getPositionFeature (coordinates) {
      const positionFeature = new Feature();
      positionFeature.setStyle(
        new Style({
          image: new CircleStyle({
            radius: 6,
            fill: new Fill({
              color: '#3399CC'
            }),
            stroke: new Stroke({
              color: '#fff',
              width: 2
            })
          })
        })
      );
      positionFeature.setGeometry(coordinates ? new Point(coordinates) : null);
      return positionFeature;
    },

    onRecenterButtonClick () {
      this.map.getView().fit(this.source.getExtent(), {
        maxZoom: 18,
        duration: 500
      });
      this.hidRecenterButton();
    }
  }
}
</script>

<style lang="scss" scoped>
  .geolocation {
    right: 10px !important;
    bottom: 95px !important;
    button {
      background-image: url('~@/static/images/icons/mylocation-sprite-1x.png');
      background-repeat: no-repeat;
      background-color: rgba(255,255,255,0.5);
    }
    .default {
      background-position: 3px 3px;
    }
    .active {
      background-position: -159px 3px;
    }
  }

  #re-center-geolocation {
    right: 50px !important;
    bottom: 86px !important;
    button {
      background-image: url('~@/static/images/icons/re-center.png');
      background-repeat: no-repeat;
      background-size: 84px 33px;
      background-color: rgba(255,255,255,0.5);
      width: 84px;
      height: 33px;
    }
    .inactive {
      display: none;
    }
  }

</style>
