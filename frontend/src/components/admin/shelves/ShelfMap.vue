<template>
  <div class="fill-height">
    <div :id="mapId" :ref="map" class="fill-height fluid flat width='100%' style='border-radius: 0" />
    <div id="zoom-control" class="indrz-zoom-control" />
    <div id="id-map-switcher-widget">
      <v-btn
        id="id-map-switcher"
        color="rgba(0,60,136,0.5)"
        min-width="95px"
        class="pa-2"
        small
        @click="onMapSwitchClick"
      >
        {{ isSatelliteMap ? "Satellite" : "Map" }}
      </v-btn>
    </div>
    <div class="indrz-logo">
      <a href="https://www.indrz.com" target="_blank">
        <img id="indrz-logo" src="/images/indrz-powered-by-90px.png" alt="indrz logo">
      </a>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import 'ol/ol.css';
import { Circle as CircleStyle, Fill, Stroke, Text, Style } from 'ol/style';
import { Draw, Modify, Translate } from 'ol/interaction';
import { Point, LineString } from 'ol/geom';
import { Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer } from 'ol/layer';
import { getHeight, getWidth, getCenter } from 'ol/extent';
import Feature from 'ol/Feature';
import {
  never,
  platformModifierKeyOnly,
  primaryAction
} from 'ol/events/condition';
import config from '@/util/indrzConfig';
import MapUtil from '@/util/map';

const { env } = config;

export default {
  name: 'ShelfMap',
  props: {
  },
  data () {
    return {
      mapId: 'shelfMapContainer',
      map: null,
      view: null,
      popup: null,
      layers: [],
      isSatelliteMap: true,
      modify: null,
      shelf: null,
      dragHandle: null
    };
  },
  computed: {
    isMobile () {
      return this.$vuetify.breakpoint.mobile;
    },
    defaultCenter () {
      return this.isMobile ? env.MOBILE_START_CENTER_XY : env.DEFAULT_CENTER_XY
    },
    defaultZoom () {
      return this.isMobile ? env.MOBILE_START_ZOOM : env.DEFAULT_START_ZOOM;
    },
    env () {
      return {
        homePageUrl: env.HOME_PAGE_URL,
        logo: env.LOGO_FILE,
        baseApiUrl: env.BASE_API_URL,
        token: env.TOKEN,
        baseWmsUrl: env.BASE_WMS_URL,
        geoServerLayerPrefix: env.GEO_SERVER_LAYER_PREFIX,
        layerNamePrefix: env.LAYER_NAME_PREFIX,
        center: this.defaultCenter
      };
    },
    ...mapState({
      floors: state => state.floor.floors,
      selectedShelf: state => state.shelf.selectedShelf
    }),
    hasShelfGeometry () {
      return this.selectedShelf && this.selectedShelf.geometry && this.selectedShelf.geometry.coordinates.length;
    }
  },
  mounted () {
    this.initializeMap();
  },
  methods: {
    initializeMap () {
      const { view, map, layers, popup } = MapUtil.initializeMap({
        mapId: this.mapId,
        center: this.defaultCenter,
        zoom: this.defaultZoom
      });

      this.view = view;
      this.map = map;
      this.layers = layers;
      this.popup = popup;

      window.onresize = () => {
        this.map.updateSize();
        MapUtil.handleWindowResize(this.mapId);
      };
      if (this.floors && this.floors.length) {
        this.intitialFloor = this.floors.filter(floor => floor.floor_num === env.DEFAULT_START_FLOOR)[0];
        this.activeFloorNum = env.LAYER_NAME_PREFIX + this.intitialFloor.floor_num;

        this.$emit('floorChange', {
          floor: this.intitialFloor,
          floorNum: this.activeFloorNum
        });

        this.wmsLayerInfo = MapUtil.getWmsLayers(this.floors, this.env);
      }
      this.layers.layerGroups.push(this.wmsLayerInfo.layerGroup);
      this.layers.switchableLayers = this.wmsLayerInfo.layers;
      this.map.addLayer(this.wmsLayerInfo.layerGroup);

      this.$nextTick(() => {
        this.map.updateSize();
        this.initializeDrawing();
      });
    },
    onMapSwitchClick () {
      const { baseLayers } = this.layers;

      this.isSatelliteMap = !this.isSatelliteMap;

      if (this.isSatelliteMap) {
        baseLayers.ortho30cmBmapat.setVisible(false);
        baseLayers.greyBmapat.setVisible(true);
        return;
      }
      baseLayers.ortho30cmBmapat.setVisible(true);
      baseLayers.greyBmapat.setVisible(false);
    },
    calculateCenter (geometry) {
      let center, coordinates, minRadius;
      const type = geometry.getType();
      if (type === 'Polygon') {
        let x = 0;
        let y = 0;
        let i = 0;
        coordinates = geometry.getCoordinates()[0].slice(1);
        coordinates.forEach(function (coordinate) {
          x += coordinate[0];
          y += coordinate[1];
          i++;
        });
        center = [x / i, y / i];
      } else if (type === 'LineString') {
        center = geometry.getCoordinateAt(0.5);
        coordinates = geometry.getCoordinates();
      } else {
        center = getCenter(geometry.getExtent());
      }
      let sqDistances;
      if (coordinates) {
        sqDistances = coordinates.map(function (coordinate) {
          const dx = coordinate[0] - center[0];
          const dy = coordinate[1] - center[1];
          return dx * dx + dy * dy;
        });
        minRadius = Math.sqrt(Math.max.apply(Math, sqDistances)) / 3;
      } else {
        minRadius =
          Math.max(
            getWidth(geometry.getExtent()),
            getHeight(geometry.getExtent())
          ) / 3;
      }
      return {
        center: center,
        coordinates: coordinates,
        minRadius: minRadius,
        sqDistances: sqDistances
      };
    },
    getDrawingVectorLayer (source) {
      const style = new Style({
        geometry: function (feature) {
          const modifyGeometry = feature.get('modifyGeometry');
          return modifyGeometry ? modifyGeometry.geometry : feature.getGeometry();
        },
        stroke: new Stroke({
          color: '#ff0000',
          width: 4
        })
      });

      return new VectorLayer({
        source: source,
        zIndex: 10,
        style: (feature) => {
          const styles = [style];
          const modifyGeometry = feature.get('modifyGeometry');
          const geometry = modifyGeometry
            ? modifyGeometry.geometry
            : feature.getGeometry();
          const result = this.calculateCenter(geometry);
          const center = result.center;
          if (center) {
            styles.push(
              new Style({
                geometry: new Point(center),
                image: new CircleStyle({
                  radius: 4,
                  fill: new Fill({
                    color: '#ff3333'
                  })
                })
              })
            );
            const coordinates = result.coordinates;
            if (coordinates) {
              styles.push(
                new Style({
                  geometry: new Point(coordinates[0]),
                  image: new CircleStyle({
                    radius: 10,
                    stroke: new Stroke({
                      color: '#ff0000',
                      width: 1
                    }),
                    fill: new Fill({
                      color: '#ffffff'
                    })
                  })
                })
              );
              styles.push(
                new Style({
                  geometry: new Point(coordinates[0]),
                  text: new Text({
                    text: 'S',
                    font: '12px "Roboto", Helvetica Neue, Helvetica, Arial, sans-serif',
                    fill: new Fill({ color: '#ff0000' }),
                    stroke: new Stroke({ color: '#ff0000', width: 1 })
                  })
                })
              );
              styles.push(
                new Style({
                  geometry: new Point(coordinates[1]),
                  image: new CircleStyle({
                    radius: 10,
                    stroke: new Stroke({
                      color: '#ff0000',
                      width: 1
                    }),
                    fill: new Fill({
                      color: '#ffffff'
                    })
                  })
                })
              );
              styles.push(
                new Style({
                  geometry: new Point(coordinates[1]),
                  text: new Text({
                    text: 'E',
                    font: '12px "Roboto", Helvetica Neue, Helvetica, Arial, sans-serif',
                    fill: new Fill({ color: '#ff0000' }),
                    stroke: new Stroke({ color: '#ff0000', width: 1 })
                  })
                })
              );
            }
          }
          return styles;
        }
      });
    },
    addInteractions (source) {
      this.draw = new Draw({
        source: source,
        type: 'LineString',
        maxPoints: 2
      });
      this.map.addInteraction(this.draw);
      this.draw.on('drawend', (drawEvent) => {
        this.shelf = drawEvent.feature;
        this.map.removeInteraction(this.draw);
      });
    },
    getVectorSource () {
      if (this.hasShelfGeometry) {
        const coordinates = this.selectedShelf.geometry.coordinates[0];
        this.shelf = new Feature({
          geometry: new LineString(
            [[coordinates[0][0], coordinates[0][1]], [coordinates[1][0], coordinates[1][1]]]
          ).transform('EPSG:3857', this.map.getView().getProjection()),
          name: 'LineString'
        });

        return new VectorSource({
          features: [
            this.shelf
          ]
        });
      }
      return new VectorSource();
    },
    initializeDrawing () {
      const source = this.getVectorSource();
      const vector = this.getDrawingVectorLayer(source);

      this.map.addLayer(vector);

      if (this.hasShelfGeometry) {
        const extent = source.getExtent();
        this.map.getView().fit(extent);
      }

      const defaultStyle = new Modify({ source: source })
        .getOverlay()
        .getStyleFunction();

      const modify = new Modify({
        source: source,
        condition: function (event) {
          return primaryAction(event) && !platformModifierKeyOnly(event);
        },
        deleteCondition: never,
        insertVertexCondition: never,
        style: (feature) => {
          if (feature.get('features').length === 0) {
            const featureCoords = this.shelf.getGeometry().getCoordinates();
            const mouseCoords = feature.getGeometry().getCoordinates();

            if (!this.dragHandle) {
              this.dragHandle = mouseCoords;
            } else {
              const dx = this.dragHandle[0] - mouseCoords[0];
              const dy = this.dragHandle[1] - mouseCoords[1];

              featureCoords[0][0] = featureCoords[0][0] - dx;
              featureCoords[1][0] = featureCoords[1][0] - dx;
              featureCoords[0][1] = featureCoords[0][1] - dy;
              featureCoords[1][1] = featureCoords[1][1] - dy;
              this.shelf.getGeometry().setCoordinates([featureCoords[0], featureCoords[1]]);
              this.dragHandle = mouseCoords;
            }
          }
          feature.get('features').forEach((modifyFeature) => {
            const modifyGeometry = modifyFeature.get('modifyGeometry');
            if (modifyGeometry) {
              const point = feature.getGeometry().getCoordinates();
              let modifyPoint = modifyGeometry.point;
              if (!modifyPoint) {
                // save the initial geometry and vertex position
                modifyPoint = point;
                modifyGeometry.point = modifyPoint;
                modifyGeometry.geometry0 = modifyGeometry.geometry;
                // get anchor and minimum radius of vertices to be used
                const result = this.calculateCenter(modifyGeometry.geometry0);
                modifyGeometry.center = result.center;
                modifyGeometry.minRadius = result.minRadius;
              }

              const center = modifyGeometry.center;
              const minRadius = modifyGeometry.minRadius;
              let dx, dy;
              dx = modifyPoint[0] - center[0];
              dy = modifyPoint[1] - center[1];
              const initialRadius = Math.sqrt(dx * dx + dy * dy);
              if (initialRadius > minRadius) {
                const initialAngle = Math.atan2(dy, dx);
                dx = point[0] - center[0];
                dy = point[1] - center[1];
                const currentRadius = Math.sqrt(dx * dx + dy * dy);
                if (currentRadius > 0) {
                  const currentAngle = Math.atan2(dy, dx);
                  const geometry = modifyGeometry.geometry0.clone();
                  geometry.scale(currentRadius / initialRadius, undefined, center);
                  geometry.rotate(currentAngle - initialAngle, center);
                  modifyGeometry.geometry = geometry;
                }
              }
            }
          });
          return defaultStyle(feature);
        }
      });

      modify.on('modifystart', function (event) {
        event.features.forEach(function (feature) {
          feature.set(
            'modifyGeometry',
            { geometry: feature.getGeometry().clone() },
            true
          );
        });
      });

      modify.on('modifyend', (event) => {
        this.dragHandle = null;
        event.features.forEach(function (feature) {
          const modifyGeometry = feature.get('modifyGeometry');
          if (modifyGeometry) {
            feature.setGeometry(modifyGeometry.geometry);
            feature.unset('modifyGeometry', true);
          }
        });
      });

      this.map.addInteraction(modify);
      this.map.addInteraction(
        new Translate({
          condition: function (event) {
            return primaryAction(event) && platformModifierKeyOnly(event);
          },
          layers: [vector]
        })
      );

      !this.hasShelfGeometry && this.addInteractions(source);
    }
  }
};
</script>

<style scoped>
  .indrz-logo {
    position: absolute; /* or absolute */
    bottom: 80px;
    left: calc(50% - 45px);
    z-index: 5;
  }
  #shelfMapContainer {
    height: calc(100vh - 75px) !important;
  }
  .indrz-zoom-control {
    right: 50px !important;
    bottom: 170px !important;
    position: absolute;
  }
  #id-map-switcher-widget {
    position: absolute;
    right: 45px !important;
    bottom: 115px !important;
  }
</style>
