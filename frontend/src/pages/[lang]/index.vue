<template>
  <v-card
    :name="mapElName"
    :ripple="false"
    style="border-radius: 0"
    fluid
    elevation="0"
  >
    <!-- Left panel is the single host for menu/search/route/poi -->
    <template v-if="drawer">
      <left-panel
        ref="leftPanel"
        v-model="drawer"
        :view="leftPanel.view"
        :map="currentMap"
        :selected="poiDrawerData"
        :menu-items="items"
        :opened-panels="openedPanels"
        :initial-poi-cat-id="initialPoiCatId"
        :initial-poi-id="initialPoiId"
        :is-mobile="isMobile"
        :drawer-height="drawerHeight"
        :should-show-drawer="shouldShowDrawer"
        @transitionend="onTransitionEnd"
        @dragStart="startDrag"
        @menuButtonClick="onMenuButtonClick"
        @locationClick="onLocationClick"
        @setGlobalRoute="onSetGlobalRoute"
        @routeGo="onRouteGo"
        @clearRoute="onClearRoute"
        @shareClick="onShareClick"
        @poiLoad="onPoiLoad"
        @loadSinglePoi="loadSinglePoi"
        @hideSidebar="closeLeftPanel"
        @hide-poi-drawer="onHidePoiDrawer"
        @closeRoute="onCloseRoutePanel"
        @closePoi="onClosePoiPanel"
        @openRoute="onOpenRouteDrawer(true)"
        @routeFrom="onRouteFromPoi"
        @routeTo="onRouteToPoi"
      />
    </template>

    <v-toolbar
      v-if="showFloatingToolbar"
      data-test="searchToolbar"
      :max-width="toolbarWidth"
      rounded
      floating
      class="ma-2 search-toolbar"
    >
      <v-app-bar-nav-icon
        v-if="!isSmallScreen || !showSearch"
        data-test="leftPaneToggleBtn"
        aria-label="Toggle navigation drawer"
        role="button"
        @click.stop="onHamburgerClick"
      />
      <v-expand-transition>
        <campus-search
          id="searchComp"
          ref="searchComp"
          data-test="searchInput"
          show-route
          :large="!isSmallScreen"
          @selectSearchResult="onNavSearchSelect"
          @showSearch="onShowSearch"
          @open-route-drawer="onOpenRouteDrawer(true)"
        />
      </v-expand-transition>
    </v-toolbar>

    <indrz-map
      ref="map"
      data-test="map"
      :route-drawer="leftPanel.view === 'route'"
      @selectFloor="onFloorSelect"
      @clearSearch="onClearSearch"
      @popupRouteClick="onPopupRouteClick"
      @openPoiTree="onOpenPoiTree"
      @openPoiToPoiRoute="onOpenPoiToPoiRoute"
      @showSearchResult="onShowSearchResult"
      @open-poi-drawer="onOpenPoiDrawer"
      @open-route-drawer="onOpenRouteDrawer(true)"
    />

   <!-- Full-height OpenLayers demo map 
    <div class="mapcanvas-host">
      <map-canvas :selected-floor-level="selectedFloorLevel" full-height />
    </div>
    -->

    <floor-changer ref="floorChanger" @floorClick="onFloorClick" />
    <snack-bar />
  </v-card>
</template>

<script>
import IndrzMap from '../../components/IndrzMap';
// import MapCanvas from '../../components/MapCanvas';
import LeftPanel from '../../components/LeftPanel';
import FloorChanger from '../../components/FloorChanger';
import CampusSearch from '../../components/CampusSearch';
import SnackBar from '../../components/SnackBar';
import BaseDrawer from '@/components/drawers/BaseDrawer'
import { useFloorStore } from '~/stores/floor';
import { usePopupStore } from '~/stores/popup';
import bus from '~/util/bus';
import config from '~/util/indrzConfig'

const { env } = config

export default {
  components: {
    LeftPanel,
    IndrzMap,
    // MapCanvas,
    FloorChanger,
    CampusSearch,
    SnackBar
  },
  mixins: [BaseDrawer],
  data () {
    return {
      updateKey: 1,
      clipped: false,
      drawer: false,
      poiDrawerData: {},
      routeDrawerData: {},
      fixed: false,
      loading: true,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Home',
          to: '/'
        }
      ],
      picker: new Date().toISOString().substr(0, 10),
      miniVariant: false,
      mapId: 'mapContainer',
      mapElName: 'mapCard',
      openedPanels: [],
      initialPoiCatId: null,
      initialPoiId: null,
      showSearch: false,
      currentMap: {},
      selectedFloorLevel: 0,

      // Single source of truth for what the user is doing in the left panel
      leftPanel: {
        view: 'menu' // 'menu' | 'search' | 'route' | 'poi'
      },

      // Guards against opening the left panel from non-user-triggered events during initial app bootstrap
      hasUserInteracted: false,
    };
  },

  computed: {
    floors () {
      const floorStore = useFloorStore();
      return typeof floorStore.floors === 'function' ? floorStore.floors() : floorStore.$state.floors;
    },
    map () {
      return this.$refs.map;
    },
    isSmallScreen () {
      return this.$vuetify.display.smAndDown;
    },
    showFloatingToolbar () {
      // Requirement: anytime the left panel is open, the floating toolbar should be hidden.
      return !this.drawer;
    },
    toolbarWidth () {
      // Give desktop/tablet more room so typing is easier.
      return this.isSmallScreen ? '340px' : '520px';
    },
    popupModel () {
      const popupStore = usePopupStore();
      return popupStore.model;
    }
  },

  watch: {
    popupModel: {
      deep: true,
      handler (val) {
        const popupStore = usePopupStore();

        // Only open the LeftPanel for user-triggered popups.
        if (!val || popupStore.origin !== 'user') {
          return;
        }

        // Do not auto-open on initial bootstrap.
        // Map clicks/search explicitly mark interaction (via onOpenPoiDrawer).
        if (!this.hasUserInteracted) {
          return;
        }

        this.leftPanel.view = 'poi';
        this.poiDrawerData =
          val?.properties ||
          val?.feature?.properties ||
          val?.feature ||
          val ||
          {};
        this.drawer = true;
      }
    }
  },

  async mounted () {
    const mapComponent = this.map;
    const floorStore = useFloorStore();
    await floorStore.LOAD_FLOORS();

    // Initialize MapCanvas floor from first loaded floor.
    if (Array.isArray(this.floors) && this.floors.length) {
      this.selectedFloorLevel = Number(this.floors[0].floor_num) || 0;
    }

    // Only call IndrzMap methods if it exists on the page.
    if (mapComponent && typeof mapComponent.loadLayers === 'function') {
      mapComponent.loadLayers(this.floors);
      this.currentMap = mapComponent;
    }

    this.loading = false;
    if (this.setSelection) {
      this.selectFloorWithCss(this.setSelection);
    }
    bus.on('poiLoad', this.onPoiLoad);
    bus.on('clearRoute', this.onClearRoute);
    this.updateOpenedPanelsHandler = (openedPanels) => {
      this.openedPanels = openedPanels;
    };
    this.goToHandler = (feature) => {
      /*      const featureCenter = feature
      featureCenter.type = 'Feature'
      this.onSearchSelect(featureCenter) */
      const data = feature.properties
      this.onPopupRouteClick({ data: data })
      const data2 = { id: feature.properties.id, properties: feature.properties, geometry: { coordinates: feature.coordinates } }
      this.map.setGlobalRoute(data2)
    }
    bus.on('update-opened-panels', this.updateOpenedPanelsHandler);
    bus.on('goTo', this.goToHandler);
  },

  methods: {
    noteUserInteraction () {
      this.hasUserInteracted = true;
    },

    openLeftPanel (view) {
      // Only auto-open the left panel on explicit user actions.
      if (!this.hasUserInteracted) {
        return;
      }
      this.leftPanel.view = view;

      // Stage 2: keep a single actual drawer open and switch the view inside it.
      this.drawer = true;
    },

    closeLeftPanel () {
      this.drawer = false;
      this.leftPanel.view = 'menu';
    },

    onHamburgerClick () {
      this.noteUserInteraction();
      if (this.drawer && (this.leftPanel.view === 'menu' || this.leftPanel.view === 'search')) {
        this.closeLeftPanel();
        return;
      }
      this.leftPanel.view = 'search';
      this.drawer = true;
    },

    onNavSearchSelect (selectedItem) {
      this.noteUserInteraction();
      this.leftPanel.view = 'poi';
      this.drawer = true;
      this.onSearchSelect(selectedItem);
    },

    onMenuButtonClick (type) {
      // Route any menu action that belongs in the left panel.
      if (type === 'directions') {
        this.onOpenRouteDrawer(true);
        return;
      }
      this.map.onMenuButtonClick(type);
    },
    onLocationClick (centroid, zoom = 18) {
      this.map.onLocationClick(centroid, zoom);
    },
    onFloorClick (floor) {
      // FloorChanger emits the full floor object
      if (floor && typeof floor.floor_num === 'number') {
        this.selectedFloorLevel = Number(floor.floor_num);

        // Persist active floor globally (used for share links)
        const floorStore = useFloorStore()
        floorStore.SET_ACTIVE_FLOOR({
          floorLevel: this.selectedFloorLevel,
          floorNum: `${env.LAYER_NAME_PREFIX}${this.selectedFloorLevel}`
        })
      }

      // If IndrzMap is present, forward the click to it.
      if (this.map && typeof this.map.onFloorClick === 'function') {
        this.map.onFloorClick(floor);
      }
    },
    onFloorSelect (floor) {
      // Backward compat (called by IndrzMap): floor is a number
      this.selectedFloorLevel = Number(floor);

      const floorStore = useFloorStore()
      floorStore.SET_ACTIVE_FLOOR({
        floorLevel: this.selectedFloorLevel,
        floorNum: `${env.LAYER_NAME_PREFIX}${this.selectedFloorLevel}`
      })

      if (this.$refs.floorChanger?.selectFloorWithCss) {
        this.$refs.floorChanger.selectFloorWithCss(floor);
      }
    },
    onSearchSelect (selectedItem) {
      this.map.onSearchSelect(selectedItem);
    },
    onSetGlobalRoute (selectedItem) {
      this.map.setGlobalRoute(selectedItem);
    },
    onRouteGo (routeType) {
      this.map.routeGo(routeType);
    },
    onClearSearch () {
      if (this.$refs.searchComp) { this.$refs.searchComp.clearSearch(); }
    },
    onPopupRouteClick (routeInfo) {
      this.onOpenRouteDrawer()
      setTimeout(() => {
        /* routeInfo?.path && */bus.emit('setRoute', routeInfo);
      }, 500);
    },
    onOpenPoiTree (poiCatId, isPoiId = false) {
      // Opening POI tree may be triggered programmatically (e.g. deep link). Do not treat as user interaction.
      // Opening POI tree is a left-panel action.
      // Deep links must be able to open the drawer even before user interaction.
      this.leftPanel.view = 'menu';
      this.drawer = true;
      this.openedPanels = [1];
      if (isPoiId) {
        this.initialPoiId = poiCatId;
      } else {
        this.initialPoiCatId = poiCatId.split(',').map(id => Number.parseInt(id, 10)).filter(id => !Number.isNaN(id));
      }
      setTimeout(() => {
        this.initialPoiId = null;
        this.initialPoiCatId = null;
      }, 2000)
    },
    onShowSearchResult (searchResult) {
      // May be triggered programmatically. Do not treat as user interaction.
      // Deep links must be able to open the drawer even before user interaction.
      this.leftPanel.view = 'menu';
      this.drawer = true;
      this.openedPanels = [3];
      const sidebar = this.$refs.leftPanel?.$refs?.sideBar;
      if (sidebar) {
        sidebar.searchResult = searchResult;
      }
    },
    onClearRoute () {
      this.map.clearRouteData();
    },
    onShareClick () {
      this.map.onShareButtonClick(true);
    },
    onPoiLoad (data) {
      this.map.onPoiLoad(data);
    },
    loadSinglePoi (poiId) {
      this.map.loadSinglePoi(poiId);
    },
    onShowSearch () {
      this.showSearch = true;
    },
    onOpenPoiDrawer (model) {
      // Called by IndrzMap (map click, deep links, search selection, close).
      // Accept multiple payload shapes and ensure we always pass POI properties (incl. images).
      if (!model || (typeof model === 'object' && Object.keys(model).length === 0)) {
        this.onClosePoiPanel();
        return;
      }

      const origin = model?.origin || null

      // Avoid opening the POI panel on initial page load.
      // Allow: real user actions (origin==='user') and explicit deep links (origin==='deeplink').
      if (!this.hasUserInteracted && origin !== 'user' && origin !== 'deeplink') {
        return
      }

      if (origin === 'user') {
        this.noteUserInteraction()
      }

      const candidate = model?.feature || model?.properties || model

      // If it's a GeoJSON-ish feature, prefer its properties.
      const poiPayload = candidate?.properties && typeof candidate.properties === 'object'
        ? candidate.properties
        : candidate

      if (poiPayload && !poiPayload.name) {
        poiPayload.name = poiPayload.room_code
      }

      this.poiDrawerData = poiPayload || { name_en: '', name: '' }
      this.leftPanel.view = 'poi'
      this.drawer = true
    },
    onOpenRouteDrawer (alter = false) {
      this.noteUserInteraction();
      if (this.leftPanel.view === 'route' && alter) {
        this.leftPanel.view = 'menu';
        return;
      }
      this.leftPanel.view = 'route';
      this.drawer = true;
      this.routeDrawerData = {};
    },
    onCloseRoutePanel () {
      this.closeLeftPanel();
    },
    onClosePoiPanel () {
      this.closeLeftPanel();
      this.poiDrawerData = {};
    },
    onRouteFromPoi () {
      this.noteUserInteraction();
      // keep existing behavior: emit route click via bus (RoutePanel listens)
      bus.emit('popupRouteClick', 'from');
      this.leftPanel.view = 'route';
      this.drawer = true;
    },
    onRouteToPoi () {
      this.noteUserInteraction();
      bus.emit('popupRouteClick', 'to');
      this.leftPanel.view = 'route';
      this.drawer = true;
    },
    onHidePoiDrawer () {
      this.onClosePoiPanel();
    },
  }
};
</script>

<style scoped>
header {
  position: absolute;
  z-index: 6;
}

.search-toolbar {
  /* Make the floating search bar easier to use */
  min-height: 60px;
  padding-left: 8px;
  padding-right: 8px;
}

</style>
