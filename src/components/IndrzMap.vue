<template>
  <div>
    <div :id="mapId" class="width='100%' style='border-radius: 0" />
    <div id="zoom-control" class="indrz-zoom-control" />
    <div id="id-map-switcher-widget">
      <v-btn
        id="id-map-switcher"
        min-width="95px"
        class="pa-2 map-switcher"
        small
        @click="onMapSwitchClick"
      >
        {{ isSatelliteMap ? "Satellite" : "Map" }}
      </v-btn>
    </div>
    <div class="indrz-powered-logo">
      <a href="https://www.indrz.com" target="_blank">
        <img id="indrz-powered-logo" src="/images/powered-by-indrz-blue-transparent-text+logo.png" alt="indrz logo">
      </a>
    </div>
    <div class="logo-on-map">
      <a :href="homePageUrl" target="_blank">
        <img id="logo-on-map" :src="logo.file" alt="logo" style="width:auto; height:40px; ">
      </a>
    </div>
    <info-overlay
      @closeClick="closeIndrzPopup(true)"
      @shareClick="onShareButtonClick"
      @popupRouteClick="onPopupRouteClick"
      @popupEntranceButtonClick="onPopupEntranceButtonClick"
      @popupMetroButtonClick="onPopupMetroButtonClick"
      @popupDefiButtonClick="onPopupDefiButtonClick"
    />
    <share-overlay ref="shareOverlay" />
    <terms :show="showTerms" @termsShow="onTermShowChange" />
    <help :show="showHelp" @helpShow="onHelpShowChange" />
    <QRCode :show="showQrCode" @qrCodeShow="onQrCodeShow" @qrCodeScanned="loadMapWithParams" />
    <UserGeoLocation :map="map" class="indrz-geolocation" />
  </div>
</template>

<script>
import queryString from 'query-string';
import MapUtil from '../util/map';
import MapHandler from '../util/mapHandler';
import RouteHandler from '../util/RouteHandler';
import POIHandler from '../util/POIHandler';
import InfoOverlay from '../components/infoOverlay';
import 'ol/ol.css';
import menuHandler from '../util/menuHandler';
import config from '../util/indrzConfig';
import ShareOverlay from './share-overlay/shareOverlay';
import Terms from './Terms';
import Help from './Help';
import UserGeoLocation from './UserGeoLocation';
import QRCode from './QRCode';

const { env } = config;

export default {
  components: {
    QRCode,
    Help,
    InfoOverlay,
    ShareOverlay,
    Terms,
    UserGeoLocation
  },
  props: {
    routeDrawer: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      mapId: 'mapContainer',
      map: null,
      view: null,
      showTerms: false,
      showHelp: false,
      showQrCode: false,
      isSatelliteMap: true,
      layers: [],
      popup: null,
      activeFloorNum: '',
      initialFloor: {},
      globalPopupInfo: {},
      globalSearchInfo: {},
      globalRouteInfo: {},
      objCenterCoords: '',
      popUpHomePage: '',
      currentPOIID: 0,
      selectedPoiCatIds: [],
      routeToValTemp: '',
      routeFromValTemp: '',
      hostUrl: window.location.href,
      routeHandler: RouteHandler(this.$store, this.$t, this),
      headerId: 'indrz-header-container',
      footerId: 'indrz-footer-container'
    };
  },

  computed: {
    logo () {
      return {
        file: env.LOGO_FILE,
        enabled: (env.LOGO_ENABLED === true)
      };
    },
    homePageUrl () {
      return env.HOME_PAGE_URL
    },
    isMobile () {
      return this.$vuetify.breakpoint.mobile;
    },
    defaultCenter () {
      return this.isMobile ? env.MOBILE_START_CENTER_XY : env.DEFAULT_CENTER_XY
    },
    defaultZoom () {
      return this.isMobile ? env.MOBILE_START_ZOOM : env.DEFAULT_START_ZOOM;
    }
  },

  mounted () {
    const query = queryString.parse(location.search);
    this.showHideHeaderFooter(query);

    const { view, map, layers, popup } = MapUtil.initializeMap({
      mapId: this.mapId,
      center: this.defaultCenter,
      zoom: this.defaultZoom
    });

    this.view = view;
    this.map = map;
    this.layers = layers;
    this.popup = popup;

    this.map.on('singleclick', this.onMapClick, this);
    window.onresize = () => {
      MapUtil.handleWindowResize(this.mapId);
      this.$nextTick(() => {
        this.map.updateSize();
      });
    };
    this.map.on('moveend', (e) => {
      this.$root.$emit('map-moved', e.map.getView().getCenter());
    });

    this.$root.$on('popupEntranceButtonClick', this.onPopupEntranceButtonClick);
    this.$root.$on('popupMetroButtonClick', this.onPopupMetroButtonClick);
    this.$root.$on('popupDefiButtonClick', this.onPopupDefiButtonClick);
    this.$root.$on('shareClick', this.onShareButtonClick);
    this.$root.$on('popupRouteClick', this.onPopupRouteClick);
    this.$root.$on('closeInfoPopup', this.closeIndrzPopup);
  },
  methods: {
    loadLayers (floors) {
      this.floors = floors;
      if (this.floors && this.floors.length) {
        this.intitialFloor = this.floors.filter(floor => floor.floor_num === env.DEFAULT_START_FLOOR)[0];
        this.activeFloorNum = env.LAYER_NAME_PREFIX + this.intitialFloor.floor_num;
        this.$emit('selectFloor', this.intitialFloor.floor_num);
      }
      this.wmsLayerInfo = MapUtil.getWmsLayers(this.floors, {
        baseWmsUrl: env.BASE_WMS_URL,
        geoServerLayerPrefix: env.GEO_SERVER_LAYER_PREFIX,
        layerNamePrefix: env.LAYER_NAME_PREFIX
      });
      this.layers.layerGroups.push(this.wmsLayerInfo.layerGroup);
      this.layers.switchableLayers = this.wmsLayerInfo.layers;
      this.map.addLayer(this.wmsLayerInfo.layerGroup);
      this.loadMapWithParams();
      this.onFloorClick(this.activeFloorNum);
    },
    getFloorName (data) {
      let floorName = '';

      if (data.floor_name) {
        floorName = data.floor_name;
      } else if (data.floor_num) {
        const foundFloor = this.floors.find(floor => floor.floor_num.toFixed(1) === Number(data.floor_num).toFixed(1));
        if (foundFloor) {
          floorName = foundFloor.short_name;
        }
      }
      return floorName;
    },
    async onSearchSelect (selection) {
      if (!selection || !selection.data) {
        this.closeIndrzPopup();
        return;
      }
      const selectedItem = selection.data;
      const { properties } = selectedItem;
      if (!properties.floor_name) {
        properties.floor_name = this.getFloorName(properties);
      }
      this.activeFloorNum = env.LAYER_NAME_PREFIX + properties.floor_num;

      this.$emit('selectFloor', properties.floor_num);

      const campusId = selectedItem.properties.building;
      const searchText = properties?.room_code || properties.name;
      const zoomLevel = 20;

      this.globalSearchInfo.selectedItem = selectedItem;
      this.globalSearchInfo.searchText = searchText;
      this.objCenterCoords = properties.centerGeometry ? properties.centerGeometry.coordinates : selectedItem.geometry.coordinates;

      const result = await MapUtil.searchIndrz(this.map, this.layers, this.globalPopupInfo, this.searchLayer, campusId, searchText, zoomLevel,
        this.popUpHomePage, this.currentPOIID, this.$i18n.locale, this.objCenterCoords, this.routeToValTemp,
        this.routeFromValTemp, this.activeFloorNum, this.popup, selectedItem, {
          searchUrl: env.SEARCH_URL,
          layerNamePrefix: env.LAYER_NAME_PREFIX
        });

      this.searchLayer = result.searchLayer;
      this.$emit('open-poi-drawer', {
        feature: properties
      })
      const featureCenter = !this.routeDrawer
        ? { data: { type: 'Feature', id: properties.id, properties: properties, geometry: { coordinates: this.objCenterCoords, type: 'MultiPolygon' } } }
        : { type: 'Feature', id: properties.id, ...{ properties, geometry: { coordinates: this.coordinates, type: 'MultiPolygon' } } }
      if (this.routeDrawer) {
        this.$nextTick(() => { this.$bus.$emit('goTo', featureCenter) })
      }
    },
    async loadMapWithParams (searchString) {
      const query = queryString.parse(searchString || location.search);
      const selectedItem = await MapUtil.loadMapWithParams(this, query);
      this.$emit('open-poi-drawer', {
        feature: selectedItem && selectedItem.properties ? selectedItem.properties : selectedItem
      })
    },
    openIndrzPopup (properties, coordinate, feature) {
      this.$emit('open-poi-drawer', {
        feature: properties
      })
      this.$bus.$emit('setSearch', properties)
      this.$root.$emit('')
      !this.isSmallScreen && MapHandler.openIndrzPopup(
        this.globalPopupInfo, this.popUpHomePage, this.currentPOIID,
        this.$i18n.locale, this.objCenterCoords, this.routeToValTemp,
        this.routeFromValTemp, this.activeFloorNum, this.popup,
        properties, coordinate, feature, null, env.LAYER_NAME_PREFIX
      );
      this.objCenterCoords = properties.centerGeometry ? properties.centerGeometry.coordinates : coordinate;
      const featureCenter = !this.routeDrawer
        ? { data: { type: 'Feature', id: properties.id, properties: properties, geometry: { coordinates: this.objCenterCoords, type: 'MultiPolygon' } } }
        : { type: 'Feature', id: properties.id, ...{ properties, geometry: { coordinates: this.coordinates, type: 'MultiPolygon' } } }
      if (!this.routeDrawer) {
        const elm = document.querySelector('.v-navigation-drawer--fixed');
        const drawerHeight = elm.offsetHeight;
        const pixel = this.map.getPixelFromCoordinate(coordinate);
        pixel[1] += (drawerHeight - 70) / 2
        const mobileCoordinate = this.map.getCoordinateFromPixel(pixel);
        if (this.isMobile) {
          this.map.getView().animate({
            duration: 2000,
            center: mobileCoordinate
          });
        } else {
          this.map.getView().animate({
            center: coordinate,
            duration: 2000
          });
        }
      } else { this.$nextTick(() => { this.$bus.$emit('goTo', featureCenter) }) }
    },
    closeIndrzPopup (fromEvent) {
      MapHandler.closeIndrzPopup(this.popup, this.globalPopupInfo);
      if (this.searchLayer) {
        this.map.removeLayer(this.searchLayer);
        this.searchLayer = null;
      }
      if (fromEvent) {
        this.$emit('clearSearch');
      }
      this.$emit('open-poi-drawer', {})
      this.$emit('open-poi-drawer', {})
    },
    onShareButtonClick (isRouteShare) {
      const shareOverlay = this.$refs.shareOverlay;
      const url = MapHandler.handleShareClick(this, this.globalPopupInfo, this.globalRouteInfo, this.globalSearchInfo, this.activeFloorNum, isRouteShare);

      if (typeof url === 'object' && url.type === 'poi') {
        shareOverlay.setPoiShareLink(url);
      } else {
        shareOverlay.setShareLink(url);
      }
      shareOverlay.show();
    },
    loadSinglePoi (poiId, zlevel) {
      POIHandler
        .showSinglePoi(poiId, this.globalPopupInfo, zlevel, this.map, this.popup, this.activeFloorNum, env.LAYER_NAME_PREFIX)
        .then(({ layer, feature }) => {
          this.searchLayer = layer;
          this.$emit('open-poi-drawer', {
            feature
          })
        });
    },
    loadPoiToPoiroute (startPoiId, endPoiId) {
      POIHandler
        .addPoisToMap([startPoiId, endPoiId], this.map, this.activeFloorNum, 'RouteFromPoiToPoi')
    },
    onPoiLoad ({ removedItems, newItems, oldItems }) {
      if (newItems) {
        newItems.forEach((itemToAdd) => {
          const index = this.selectedPoiCatIds.indexOf(itemToAdd.id);
          index === -1 && this.selectedPoiCatIds.push(itemToAdd.id);
        })
      }
      if (removedItems) {
        removedItems.forEach((itemToRemvoe) => {
          const index = this.selectedPoiCatIds.indexOf(itemToRemvoe.id);
          index > -1 && this.selectedPoiCatIds.splice(index, 1);
        });
      }
      MapHandler.handlePoiLoad(this.map, this.activeFloorNum, { removedItems, newItems, oldItems }, {
        baseApiUrl: env.BASE_API_URL,
        token: env.TOKEN,
        layerNamePrefix: env.LAYER_NAME_PREFIX
      });
    },
    onTermShowChange (value) {
      this.showTerms = value;
    },
    onHelpShowChange (value) {
      this.showHelp = value;
    },
    onQrCodeShow (value) {
      this.showQrCode = value;
    },
    onPopupRouteClick (path) {
      let data = null;

      if (this.globalSearchInfo.selectedItem) {
        data = this.globalSearchInfo.selectedItem.properties;
        if (data.shelfId) {
          data.coords = this.globalSearchInfo.selectedItem.geometry.coordinates;
        }
      } else {
        data = this.globalPopupInfo;
      }
      this.$emit('popupRouteClick', {
        path,
        data
      });
    },
    onMapClick (evt) {
      MapHandler.handleMapClick(this, evt, env.LAYER_NAME_PREFIX);
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
    onMenuButtonClick (type) {
      switch (type) {
        case 'directions':
          this.$emit('open-route-drawer');
          break;
        case 'zoom-home':
          menuHandler.handleZoomToHome(this, this.defaultCenter, this.defaultZoom);
          break;
        case 'download':
          menuHandler.handleDownLoad(this);
          break;
        case 'pdf':
          menuHandler.handlePdf(this);
          break;
        case 'share-map':
          menuHandler.handleShare(this);
          break;
        case 'help':
          this.showHelp = true;
          break;
        case 'terms':
          this.showTerms = true;
          break;
        case 'qrcode':
          this.showQrCode = true;
          break;
        default:
          break;
      }
    },
    onLocationClick (centroid, zoom = 18) {
      if (!centroid) {
        return;
      }
      this.view.animate({
        center: centroid.coordinates,
        duration: 2000,
        zoom: zoom
      });
    },
    onFloorClick (floorNum) {
      this.activeFloorNum = floorNum;
      MapUtil.activateLayer(this.activeFloorNum, this.layers.switchableLayers, this.map);
    },
    async onPopupEntranceButtonClick () {
      const nearestEntrance = await this.routeHandler.getNearestEntrance(this.globalPopupInfo);

      if (nearestEntrance) {
        this.$emit('popupRouteClick', {
          path: 'to',
          data: nearestEntrance
        });
      }
    },
    async onPopupMetroButtonClick () {
      const nearestMetro = await this.routeHandler.getNearestMetro(this.globalPopupInfo);

      if (nearestMetro) {
        this.$emit('popupRouteClick', {
          path: 'to',
          data: nearestMetro
        });
      }
    },
    async onPopupDefiButtonClick () {
      const nearestDefi = await this.routeHandler.getNearestDefi(this.globalPopupInfo);

      if (nearestDefi) {
        this.$emit('popupRouteClick', {
          path: 'to',
          data: nearestDefi
        });
      }
    },
    setGlobalRoute (selectedItem) {
      this.globalRouteInfo[selectedItem.routeType] = selectedItem.data;
    },
    async routeGo (routeType = 0) {
      const routeResult = await this.routeHandler.routeGo(this, this.layers, this.globalRouteInfo, routeType, {
        baseApiUrl: env.BASE_API_URL,
        layerNamePrefix: env.LAYER_NAME_PREFIX,
        token: env.TOKEN,
        locale: this.$i18n.locale
      });
      const { noRouteFound, error, routeUrl } = routeResult

      if (noRouteFound) {
        this.$root.$emit('noRouteFound', true);
      } else if (error) {
        this.$root.$emit('routeError', error)
      } else {
        this.globalRouteInfo.routeUrl = routeUrl;
        this.$root.$emit('setRouteInfo', routeResult);
      }
    },
    clearRouteData () {
      this.routeHandler.clearRouteData(this.map, true);
    },
    showHideHeaderFooter (query) {
      if (query.hideHeader && query.hideHeader === 'true') {
        document.getElementById(this.headerId).style.display = 'none';
      }
      if (query.hideFooter && query.hideFooter === 'true') {
        document.getElementById(this.footerId).style.display = 'none';
      }
    }
  }
};
</script>

<style scoped>
  .indrz-zoom-control {
    right: 50px !important;
    bottom: 100px !important;
    position: absolute;
  }
  #id-map-switcher-widget {
    position: absolute;
    right: 45px !important;
    bottom: 37px !important;
  }
</style>
