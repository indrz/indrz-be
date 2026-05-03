<template>
  <div>
    <a class="skiplink" :href="'#' + mapId">Go to map</a>
    <!-- ensure the map div participates in layout immediately -->
    <div :id="mapId"></div>
    <div id="zoom-control" class="indrz-zoom-control" />
    <div id="id-map-switcher-widget">
      <v-btn
        id="id-map-switcher"
        min-width="95px"
        class="pa-2 map-switcher"
        size="small"
        aria-label="Switch background map between satellite and map"
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
        <img id="logo-on-map" :src="logo.file" alt="logo" style="width:auto; height:40px;">
      </a>
    </div>
    <info-overlay
      :model="popupModel"
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
import bus from '~/util/bus';
import { usePopupStore } from '~/stores/popup';

// WMS floor overlay (MapCanvas-style)
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import { createEmpty, extend as extendExtent, isEmpty as isEmptyExtent } from 'ol/extent'

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
      // "Satellite" should mean ortho is visible; default to map (grey) unless you want satellite by default.
      isSatelliteMap: false,
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
      routeHandler: RouteHandler(),
      headerId: 'indrz-header-container',
      footerId: 'indrz-footer-container',
      _onResize: null,
      _onMoveEnd: null,
      _onSingleClick: null,
      wmsLayer: null,
      wmsSource: null,
      WMS_BASE_URL: 'https://campusplan.aau.at/geoserver/wms',
      selectedFloorLevel: 0,
      pendingPoiCatZoomIds: null,
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
      if (typeof window === 'undefined') {
        return false
      }
      return window.innerWidth <= 768
    },
    defaultCenter () {
      return this.isMobile ? env.MOBILE_START_CENTER_XY : env.DEFAULT_CENTER_XY
    },
    defaultZoom () {
      return this.isMobile ? env.MOBILE_START_ZOOM : env.DEFAULT_START_ZOOM;
    },
    popupModel () {
      const popupStore = usePopupStore();
      return popupStore.model;
    },
    currentLocale () {
      const raw = this.$i18n?.locale
      return raw && typeof raw === 'object' && 'value' in raw ? raw.value : raw
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

    // Critical: size the container after DOM mount, then force OL to recompute size and render.
    this.$nextTick(() => {
      MapUtil.handleWindowResize(this.mapId);
      this.map.updateSize();
      this.map.renderSync();

      // Apply initial base-layer visibility consistent with isSatelliteMap.
      const { baseLayers } = this.layers;
      baseLayers.ortho30cmBmapat.setVisible(!!this.isSatelliteMap);
      baseLayers.greyBmapat.setVisible(!this.isSatelliteMap);
    });

    // Map event handlers (keep references for cleanup)
    this._onSingleClick = (evt) => this.onMapClick(evt);
    this.map.on('singleclick', this._onSingleClick);

    this._onMoveEnd = (e) => {
      bus.emit('map-moved', e.map.getView().getCenter());
    };
    this.map.on('moveend', this._onMoveEnd);

    this._onResize = () => {
      MapUtil.handleWindowResize(this.mapId);
      this.$nextTick(() => {
        this.map.updateSize();
      });
    };
    window.addEventListener('resize', this._onResize);

    bus.on('popupEntranceButtonClick', this.onPopupEntranceButtonClick);
    bus.on('popupMetroButtonClick', this.onPopupMetroButtonClick);
    bus.on('popupDefiButtonClick', this.onPopupDefiButtonClick);
    bus.on('shareClick', this.onShareButtonClick);
    bus.on('popupRouteClick', this.onPopupRouteClick);
    bus.on('closeInfoPopup', this.closeIndrzPopup);
  },

  beforeUnmount () {
    bus.off('popupEntranceButtonClick', this.onPopupEntranceButtonClick);
    bus.off('popupMetroButtonClick', this.onPopupMetroButtonClick);
    bus.off('popupDefiButtonClick', this.onPopupDefiButtonClick);
    bus.off('shareClick', this.onShareButtonClick);
    bus.off('popupRouteClick', this.onPopupRouteClick);
    bus.off('closeInfoPopup', this.closeIndrzPopup);

    if (this._onResize) {
      window.removeEventListener('resize', this._onResize);
      this._onResize = null;
    }

    if (this.map) {
      if (this._onSingleClick) {
        this.map.un('singleclick', this._onSingleClick);
        this._onSingleClick = null;
      }
      if (this._onMoveEnd) {
        this.map.un('moveend', this._onMoveEnd);
        this._onMoveEnd = null;
      }
    }
  },

  methods: {
    zoomToPoiCategories (poiCatIds, zoomLevel = 19) {
      if (!this.map || !Array.isArray(poiCatIds) || !poiCatIds.length) return;

      const groupLayer = this.map
        .getLayers()
        .getArray()
        .find(l => l?.getProperties && l.getProperties().id === 99999);

      const layers = groupLayer?.getLayers?.().getArray?.() || [];
      const extent = createEmpty();

      for (const catId of poiCatIds) {
        const layer = layers.find(l => l?.getProperties && l.getProperties().id === catId);
        const layerExtent = layer?.getSource?.()?.getExtent?.();
        if (layerExtent) {
          extendExtent(extent, layerExtent);
        }
      }

      if (isEmptyExtent(extent)) return;

      this.map.getView().fit(extent, {
        padding: [60, 30, 60, 30],
        maxZoom: zoomLevel,
        duration: 600
      });
    },
    getWmsLayerName (floorLevel) {
      const level = Number(floorLevel)
      const safeLevel = Number.isFinite(level) ? level : 0
      const floorStr = safeLevel.toFixed(1).replace('.', '_')
      return `indrz:floor_${floorStr}`
    },

    ensureWmsLayer () {
      if (!this.map) return

      if (!this.wmsSource) {
        this.wmsSource = new TileWMS({
          url: this.WMS_BASE_URL,
          params: {
            LAYERS: this.getWmsLayerName(this.selectedFloorLevel),
            TILED: true,
            FORMAT: 'image/png',
            TRANSPARENT: true,
            VERSION: '1.3.0'
          },
          serverType: 'geoserver',
          crossOrigin: 'anonymous'
        })
      }

      if (!this.wmsLayer) {
        this.wmsLayer = new TileLayer({
          source: this.wmsSource,
          zIndex: 3,
          opacity: 1
        })
        this.map.addLayer(this.wmsLayer)
      }

      this.wmsSource.updateParams({
        LAYERS: this.getWmsLayerName(this.selectedFloorLevel)
      })
    },

    setSelectedFloorLevelFromActiveFloorNum () {
      const prefix = env.LAYER_NAME_PREFIX || 'floor_'
      const raw = typeof this.activeFloorNum === 'string'
        ? this.activeFloorNum.replace(prefix, '')
        : this.activeFloorNum

      const parsed = Number(raw)
      this.selectedFloorLevel = Number.isFinite(parsed) ? parsed : 0
    },

    loadLayers (floors) {
      this.floors = floors;

      if (Array.isArray(this.floors) && this.floors.length) {
        const defaultStartFloor = Number(env.DEFAULT_START_FLOOR)

        const initialFloor =
          this.floors.find(f => Number(f.floor_num) === defaultStartFloor) ??
          this.floors[0]

        this.initialFloor = initialFloor

        this.activeFloorNum = `${env.LAYER_NAME_PREFIX}${initialFloor.floor_num}`
        this.selectedFloorLevel = Number(initialFloor.floor_num) || 0

        this.$emit('selectFloor', initialFloor.floor_num)
      }

      // Old behavior: create per-floor WMS ImageWMS layers via MapUtil.getWmsLayers.
      // New behavior: create ONE TileWMS layer and update its LAYERS param on floor switch.
      this.layers.switchableLayers = []

      this.ensureWmsLayer()

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
        this.popUpHomePage, this.currentPOIID, this.currentLocale, this.objCenterCoords, this.routeToValTemp,
        this.routeFromValTemp, this.activeFloorNum, this.popup, selectedItem, {
          searchUrl: env.SEARCH_URL,
          layerNamePrefix: env.LAYER_NAME_PREFIX
        });

      this.searchLayer = result.searchLayer;
      this.$emit('open-poi-drawer', {
        feature: properties,
        origin: 'user'
      })
      const featureCenter = !this.routeDrawer
        ? { data: { type: 'Feature', id: properties.id, properties: properties, geometry: { coordinates: this.objCenterCoords, type: 'MultiPolygon' } } }
        : { type: 'Feature', id: properties.id, ...{ properties, geometry: { coordinates: this.coordinates, type: 'MultiPolygon' } } }
      if (this.routeDrawer) {
        this.$nextTick(() => { bus.emit('goTo', featureCenter) })
      }
    },
    async loadMapWithParams (searchString) {
      const query = queryString.parse(searchString || location.search);

      // Deep-link: precompute category IDs to zoom once POI layers are added.
      if (query && query['poi-cat-id']) {
        const ids = String(query['poi-cat-id'])
          .split(',')
          .map(v => Number.parseInt(v, 10))
          .filter(v => Number.isFinite(v));
        this.pendingPoiCatZoomIds = ids.length ? ids : null;
      }

      const hasPoiIdDeepLink = !!(query && (query['poi-id'] || query.poiId || query.poi_id))

      const selectedItem = await MapUtil.loadMapWithParams(this, query);

      // Only open the POI panel during initial load if the URL explicitly targets a POI.
      if (hasPoiIdDeepLink && selectedItem) {
        this.$emit('open-poi-drawer', {
          feature: selectedItem && selectedItem.properties ? selectedItem.properties : selectedItem,
          origin: 'deeplink'
        })
      }
    },
    openIndrzPopup (properties, coordinate, feature) {
      this.$emit('open-poi-drawer', { feature: properties, origin: 'user' })
      bus.emit('setSearch', properties)

      const popupModel = MapHandler.openIndrzPopup(
        this.globalPopupInfo,
        this.popUpHomePage,
        this.currentLocale,
        this.objCenterCoords,
        this.routeToValTemp,
        this.routeFromValTemp,
        this.activeFloorNum,
        this.popup,
        properties,
        coordinate,
        feature,
        null
      );
      console.log('print this', popupModel);

      const popupStore = usePopupStore();
      popupStore.SET_POPUP(popupModel, 'user');

      this.objCenterCoords = properties.centerGeometry ? properties.centerGeometry.coordinates : coordinate;
      const featureCenter = !this.routeDrawer
        ? { data: { type: 'Feature', id: properties.id, properties: properties, geometry: { coordinates: this.objCenterCoords, type: 'MultiPolygon' } } }
        : { type: 'Feature', id: properties.id, ...{ properties, geometry: { coordinates: this.coordinates, type: 'MultiPolygon' } } }
      if (!this.routeDrawer) {
        if (this.isMobile) {
          const drawerEl =
            document.querySelector('[data-test="poiLeftPane"]') ||
            document.querySelector('.v-navigation-drawer--fixed') ||
            document.querySelector('.v-navigation-drawer')

          const drawerHeight = drawerEl ? drawerEl.offsetHeight : 0

          if (drawerHeight > 0) {
            const pixel = this.map.getPixelFromCoordinate(coordinate);
            pixel[1] += (drawerHeight - 70) / 2
            const mobileCoordinate = this.map.getCoordinateFromPixel(pixel);
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
        } else {
          this.map.getView().animate({
            center: coordinate,
            duration: 2000
          });
        }
      } else { this.$nextTick(() => { bus.emit('goTo', featureCenter) }) }
    },

    closeIndrzPopup (fromEvent) {
      MapHandler.closeIndrzPopup(this.popup, this.globalPopupInfo);
      const popupStore = usePopupStore();
      popupStore.CLEAR_POPUP();
      if (this.searchLayer) {
        this.map.removeLayer(this.searchLayer);
        this.searchLayer = null;
      }
      if (fromEvent) {
        this.$emit('clearSearch');
      }
      // keep a single clear emit (LeftPanel now owns UI)
      this.$emit('open-poi-drawer', {})
    },
    onShareButtonClick (isRouteShare) {
      const shareOverlay = this.$refs.shareOverlay;
      const url = MapHandler.handleShareClick(
        this,
        this.globalPopupInfo,
        this.globalRouteInfo,
        this.globalSearchInfo,
        this.activeFloorNum,
        isRouteShare
      );

      if (typeof url === 'object' && url.type === 'poi') {
        shareOverlay.setPoiShareLink(url);
      } else {
        shareOverlay.setShareLink(url);
      }
      shareOverlay.show();
    },
    loadSinglePoi (poiId, zlevel, origin = 'user') {
      POIHandler
        .showSinglePoi(
          poiId,
          this.globalPopupInfo,
          zlevel,
          this.map,
          this.popup,
          this.activeFloorNum,
          env.LAYER_NAME_PREFIX,
          this.$i18n?.locale || 'en'
        )
        .then(({ layer, feature, popupModel }) => {
          this.searchLayer = layer;

          const popupStore = usePopupStore();
          if (popupModel) {
            popupStore.SET_POPUP(popupModel, origin);
          }

          this.$emit('open-poi-drawer', {
            feature,
            origin
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
      const loadPromise = MapHandler.handlePoiLoad(this.map, this.activeFloorNum, { removedItems, newItems, oldItems }, {
        baseApiUrl: env.BASE_API_URL,
        token: env.TOKEN,
        layerNamePrefix: env.LAYER_NAME_PREFIX
      });

      if (this.pendingPoiCatZoomIds && this.pendingPoiCatZoomIds.length) {
        Promise.resolve(loadPromise).then(() => {
          this.zoomToPoiCategories(this.pendingPoiCatZoomIds);
          this.pendingPoiCatZoomIds = null;
        });
      }
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
      MapHandler.handleMapClick(this, evt);
    },
    onMapSwitchClick () {
      const { baseLayers } = this.layers;

      this.isSatelliteMap = !this.isSatelliteMap;

      // Satellite == ortho visible
      baseLayers.ortho30cmBmapat.setVisible(!!this.isSatelliteMap);
      baseLayers.greyBmapat.setVisible(!this.isSatelliteMap);
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
      if (floorNum && typeof floorNum === 'object') {
        const numericFloor = Number(floorNum.floor_num)
        this.activeFloorNum = `${env.LAYER_NAME_PREFIX}${numericFloor}`
        this.selectedFloorLevel = Number.isFinite(numericFloor) ? numericFloor : 0
      } else {
        this.activeFloorNum = floorNum;
        this.setSelectedFloorLevelFromActiveFloorNum()
      }
      this.ensureWmsLayer()

      // Preserve POI visibility updates that previously happened inside MapUtil.activateLayer
      POIHandler.setPoiFeatureVisibility(this.map, this.activeFloorNum, env.LAYER_NAME_PREFIX)
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
        locale: this.currentLocale
      });
      const { noRouteFound, error, routeUrl } = routeResult

      if (noRouteFound) {
        bus.emit('noRouteFound', true);
      } else if (error) {
        bus.emit('routeError', error);
      } else {
        this.globalRouteInfo.routeUrl = routeUrl;
        bus.emit('setRouteInfo', routeResult);
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
  .mapId {
    width: 100%;
    border-radius: 0;
  }
  #map:focus {
    outline: #4A74A8 solid 0.15em;
  }
  a.skiplink {
    position: absolute;
    clip: rect(1px, 1px, 1px, 1px);
    padding: 0;
    border: 0;
    height: 1px;
    width: 1px;
    overflow: hidden;
  }
  a.skiplink:focus {
    clip: auto;
    height: auto;
    width: auto;
    background-color: #fff;
    padding: 0.3em;
  }

  /* Critical: ensure OpenLayers target has non-zero size on first paint */
  #mapContainer {
    width: 100%;
    height: 100vh; /* baseline; JS resize will refine if header/footer are present */
  }
</style>
