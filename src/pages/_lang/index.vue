<template>
  <v-card
    :name="mapElName"
    :ripple="false"
    style="border-radius: 0"
    fluid
    flat
  >
    <template v-if="shouldShowPoiDrawer">
      <poi-drawer
        :key="`poi-drawer-${updateKey}`"
        :show="shouldShowPoiDrawer"
        :data="poiDrawerData"
        :base-map="currentMap"
        :navigation="drawer"
        @update:drawer="drawer = $event"
        @open-route-drawer="onOpenRouteDrawer(true)"
        @hide-poi-drawer="onHidePoiDrawer"
        @update:show="poiDrawer = $event"
      />
    </template>

    <route-drawer
      :v-show="shouldShowRouteDrawer"
      :show="shouldShowRouteDrawer"
      :data="routeDrawerData"
      :base-map="currentMap"
      :navigation="drawer"
      @on-close="routeDrawer = false"
      @update:drawer="drawer = $event"
      @update:show="routeDrawer = $event"
      @setGlobalRoute="onSetGlobalRoute"
      @routeGo="onRouteGo"
    />

    <template v-if="drawer">
      <v-navigation-drawer
        ref="drawer"
        v-model="drawer"
        class="resizable"
        bottom
        :style="isMobile ? { width: '275px', height: shouldShowDrawer ? drawerHeight + 'px' : '422px' } : {width: '275px'}"
        fixed
        app
        @transitionend="onTransitionEnd"
      >
        <div v-if="isMobile" class="draggable-handle" style="mb-2" @mousedown="startDrag" @touchstart="startDrag" />
        <sidebar
          ref="sideBar"
          :menu-items="items"
          :opened-panels="openedPanels"
          :initial-poi-cat-id="initialPoiCatId"
          :initial-poi-id="initialPoiId"
          @menuButtonClick="onMenuButtonClick"
          @locationClick="onLocationClick"
          @setGlobalRoute="onSetGlobalRoute"
          @routeGo="onRouteGo"
          @clearRoute="onClearRoute"
          @shareClick="onShareClick"
          @poiLoad="onPoiLoad"
          @loadSinglePoi="loadSinglePoi"
          @hideSidebar="drawer = false"
        />
      </v-navigation-drawer>
    </template>
    <v-toolbar
      v-if="!shouldShowPoiDrawer || isSmallScreen"
      data-test="searchToolbar"
      :max-width="toolbarWidth"
      dense
      rounded
      floating
      class="ma-2"
    >
      <v-app-bar-nav-icon
        v-if="!isSmallScreen || !showSearch"
        data-test="leftPaneToggleBtn"
        aria-label="Toggle navigation drawer"
        role="button"
        @click.stop="drawer = !drawer;"
      />
      <v-expand-transition>
        <campus-search
          id="searchComp"
          ref="searchComp"
          data-test="searchInput"
          show-route
          @selectSearchResult="onSearchSelect"
          @showSearch="onShowSearch"
          @open-route-drawer="onOpenRouteDrawer(true)"
        />
      </v-expand-transition>
    </v-toolbar>
    <indrz-map
      ref="map"
      data-test="map"
      :route-drawer="routeDrawer"
      @selectFloor="onFloorSelect"
      @clearSearch="onClearSearch"
      @popupRouteClick="onPopupRouteClick"
      @openPoiTree="onOpenPoiTree"
      @openPoiToPoiRoute="onOpenPoiToPoiRoute"
      @showSearchResult="onShowSearchResult"
      @open-poi-drawer="onOpenPoiDrawer"
      @open-route-drawer="onOpenRouteDrawer(true)"
    />
    <floor-changer ref="floorChanger" @floorClick="onFloorClick" />
    <snack-bar />
  </v-card>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import IndrzMap from '../../components/IndrzMap';
import Sidebar from '../../components/Sidebar';
import FloorChanger from '../../components/FloorChanger';
import CampusSearch from '../../components/CampusSearch';
import SnackBar from '../../components/SnackBar';
import mapHandler from '../../util/mapHandler';
import PoiDrawer from '@/components/drawers/PoiDrawer';
import RouteDrawer from '@/components/drawers/RouteDrawer.vue';
import BaseDrawer from '@/components/drawers/BaseDrawer'

export default {
  components: {
    Sidebar,
    IndrzMap,
    FloorChanger,
    CampusSearch,
    SnackBar,
    PoiDrawer,
    RouteDrawer
  },
  mixins: [BaseDrawer],
  data () {
    return {
      updateKey: 1,
      clipped: false,
      drawer: false,
      poiDrawer: false,
      routeDrawer: false,
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
      currentMap: {}
    };
  },

  computed: {
    ...mapState({
      floors: state => state.floor.floors
    }),
    map () {
      return this.$refs.map;
    },
    isSmallScreen () {
      return this.$vuetify.breakpoint.smAndDown;
    },
    toolbarWidth () {
      return this.isSmallScreen ? '280px' : '320px';
    },
    shouldShowPoiDrawer: {
      get () {
        return this.poiDrawer && !this.drawer && !this.routeDrawer;
      },
      set () {
      }
    },
    shouldShowRouteDrawer () {
      return this.routeDrawer && !this.poiDrawer && !this.drawer
    }
  },

  watch: {
    search (text) {
      if (!text || text.length < 3) {
        return;
      }
      this.term$.next(text);
    }
  },

  async mounted () {
    const mapComponent = this.map;

    mapHandler.setI18n(this.$i18n);
    await this.loadFloors();
    mapComponent.loadLayers(this.floors);
    this.currentMap = mapComponent;
    this.loading = false;
    if (this.setSelection) {
      this.selectFloorWithCss(this.setSelection);
    }
    this.$root.$on('poiLoad', this.onPoiLoad);
    this.$root.$on('clearRoute', this.onClearRoute);
    this.$root.$on('update-opened-panels', (openedPanels) => {
      this.openedPanels = openedPanels
    })
    this.$bus.$on('goTo', (feature) => {
      /*      const featureCenter = feature
      featureCenter.type = 'Feature'
      this.onSearchSelect(featureCenter) */
      const data = feature.properties
      this.onPopupRouteClick({ data: data })
      const data2 = { id: feature.properties.id, properties: feature.properties, geometry: { coordinates: feature.coordinates } }
      this.map.setGlobalRoute(data2)
    })
  },
  methods: {
    ...mapActions({
      loadFloors: 'floor/LOAD_FLOORS'
    }),
    onDrawerClick () {
      this.$emit('onDrawerClick');
    },
    onMenuButtonClick (type) {
      this.map.onMenuButtonClick(type);
    },
    onLocationClick (centroid, zoom = 18) {
      this.map.onLocationClick(centroid, zoom);
    },
    onFloorClick (floor) {
      this.map.onFloorClick(floor);
    },
    onFloorSelect (floor) {
      this.$refs.floorChanger.selectFloorWithCss(floor);
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
        /* routeInfo?.path && */this.$root.$emit('setRoute', routeInfo);
      }, 500);
    },
    onOpenPoiTree (poiCatId, isPoiId = false) {
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
    onOpenPoiToPoiRoute (startPoiId, endPoiId) {
      this.map.loadPoiToPoiroute(startPoiId, endPoiId);
    },
    onShowSearchResult (searchResult) {
      this.drawer = true;
      this.openedPanels = [3];
      this.$refs.sideBar.searchResult = searchResult;
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
      const { feature } = model
      if (feature && !feature.name) {
        feature.name = feature.room_code
      }
      this.poiDrawerData = feature || { name_en: '', name: '' }
      this.$nextTick(() => {
        this.poiDrawer = !!feature;
        if (this.poiDrawer) {
          this.drawer = false;
          this.routeDrawer = false;
          this.poiDrawerData.floorNum = feature.floor_num;
          const field = this.$refs.searchComp;
          this.$bus.$emit('setSearch', feature)
          if (this.isMobile) {
            if (field) {
              field.stopSearch = true;
              field.searchResult = [feature];
              field.model = feature;
              field.search = this.poiDrawerData.room_code || this.poiDrawerData.short_name || this.poiDrawerData.name || this.poiDrawerData.building_name;
              setTimeout(() => {
                field.stopSearch = false;
              }, 1000);
            }
          } else {
            this.updateKey++;
          }
        }
      })
    },
    onOpenRouteDrawer (alter = false) {
      if (this.routeDrawer && alter) {
        this.routeDrawer = false;
        return;
      }
      this.drawer = false;
      this.poiDrawer = false;
      this.routeDrawer = true;
      this.routeDrawerData = {};
    },
    onHidePoiDrawer () {
      this.poiDrawerData = {};
      this.poiDrawer = false;
    }
  }
};
</script>

<style scoped>
  header {
    position: absolute;
    z-index: 6;
  }
</style>
