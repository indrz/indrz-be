<template>
  <v-navigation-drawer
    v-model="model"
    class="left-panel"
    location="left"
    :style="drawerStyle"
    app
    @transitionend="$emit('transitionend')"
  >
    <!-- Unified header for route/poi views -->
    <v-toolbar
      v-if="view === 'route' || view === 'poi'"
      class="left-panel-header"
      color="deep-purple-accent-4"
      theme="dark"
      density="comfortable"
    >
      <v-toolbar-title>{{ panelTitle }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon data-test="panelCloseBtn" @click="onCloseClick">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>

    <!-- Scrollable content -->
    <div class="left-panel-content">
      <!-- Panel content switches based on view -->
      <template v-if="view === 'route'">
        <route-panel
          @setGlobalRoute="$emit('setGlobalRoute', $event)"
          @routeGo="$emit('routeGo', $event)"
          @hide-poi-drawer="$emit('hide-poi-drawer')"
          @close="$emit('closeRoute')"
        />
      </template>

      <template v-else-if="view === 'poi'">
        <poi-panel
          :data="selected"
          @close="$emit('closePoi')"
          @openRoute="$emit('openRoute')"
          @routeFrom="$emit('routeFrom', $event)"
          @routeTo="$emit('routeTo', $event)"
        />
      </template>

      <template v-else>
        <sidebar
          ref="sideBar"
          :menu-items="menuItems"
          :opened-panels="openedPanels"
          :initial-poi-cat-id="initialPoiCatId"
          :initial-poi-id="initialPoiId"
          @menuButtonClick="$emit('menuButtonClick', $event)"
          @locationClick="forwardLocationClick"
          @setGlobalRoute="$emit('setGlobalRoute', $event)"
          @routeGo="$emit('routeGo', $event)"
          @clearRoute="$emit('clearRoute')"
          @shareClick="$emit('shareClick')"
          @poiLoad="$emit('poiLoad', $event)"
          @loadSinglePoi="$emit('loadSinglePoi', $event)"
          @hideSidebar="$emit('hideSidebar')"
        />
      </template>
    </div>
  </v-navigation-drawer>
</template>

<script>
import Sidebar from '@/components/Sidebar';
import DrawerSearch from '@/components/drawers/DrawerSearch';
import RoutePanel from '@/components/panels/RoutePanel';
import PoiPanel from '@/components/panels/PoiPanel';

export default {
  name: 'LeftPanel',
  components: {
    Sidebar,
    DrawerSearch,
    RoutePanel,
    PoiPanel
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    view: {
      type: String,
      default: 'menu'
    },
    map: {
      type: Object,
      required: true
    },
    selected: {
      type: Object,
      default: () => ({})
    },
    menuItems: {
      type: Array,
      default: () => ([])
    },
    openedPanels: {
      type: Array,
      default: () => ([])
    },
    initialPoiCatId: {
      type: Array,
      default: () => ([])
    },
    initialPoiId: {
      type: String,
      default: null
    },
    isMobile: {
      type: Boolean,
      default: false
    },
    drawerHeight: {
      type: Number,
      default: 422
    },
    shouldShowDrawer: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'update:modelValue',
    'transitionend',
    'dragStart',
    'hideSidebar',
    'hide-poi-drawer',
    'menuButtonClick',
    'locationClick',
    'setGlobalRoute',
    'routeGo',
    'clearRoute',
    'shareClick',
    'poiLoad',
    'loadSinglePoi',
    'closeRoute',
    'closePoi',
    'openRoute',
    'routeFrom',
    'routeTo'
  ],
  computed: {
    model: {
      get () {
        return this.modelValue;
      },
      set (v) {
        this.$emit('update:modelValue', v);
      }
    },
    drawerStyle () {
      // Left drawer should fill the viewport height.
      // On mobile we still keep it left (consistent UX), but allow full width if desired.
      const base = { height: '100vh' };
      if (this.isMobile) {
        return { ...base, width: '100%', maxWidth: '410px' };
      }
      return { ...base, width: '410px' };
    },
    panelTitle () {
      if (this.view === 'route') return this.$t('route');
      if (this.view === 'poi') return this.selected?.name || this.$t('poi_details');
      return '';
    }
  },
  methods: {
    forwardLocationClick (...args) {
      this.$emit('locationClick', ...args);
    },
    onCloseClick () {
      if (this.view === 'route') {
        this.$emit('closeRoute');
      } else if (this.view === 'poi') {
        this.$emit('closePoi');
      }
    }
  }
};
</script>

<style scoped>
.left-panel {
  /* Use flex layout to separate header from scrollable content */
  display: flex;
  flex-direction: column;
}

.left-panel-header {
  flex-shrink: 0;
}

.left-panel-content {
  flex: 1;
  overflow-y: auto;
}
</style>
