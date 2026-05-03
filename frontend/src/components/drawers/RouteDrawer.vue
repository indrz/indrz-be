<template>
  <!--  <v-navigation-drawer
    ref="drawer"
    v-model="shouldShowDrawer"
    class="resizable"
    bottom
    :style="{ width: '410px', height: drawerHeight + 'px' }"
    fixed
    app
    data-test="directionsPane"
    @transitionend="onTransitionEnd"
  >-->
  <div ref="drawerEl">
  <v-navigation-drawer
    ref="drawer"
    v-model="shouldShowDrawer"
    class="resizable"
    location="bottom"
    :style="{ width: isMobile ? '100%' : '410px', height: drawerHeight + 'px', top: 'auto', bottom: 0, position:'fixed' }"
    app
    fixed
    :permanent="shouldShowDrawer"
    data-test="directionsPane"
    @transitionend="onTransitionEnd"
  >
    <v-app-bar
      color="deep-purple-accent-4"
      theme="dark"
    >
      <v-toolbar-title>{{ locale.routeLabel }}</v-toolbar-title>
      <v-btn icon @click="clearDirections">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-app-bar>
    <div v-if="isMobile" class="draggable-handle" @mousedown="startDrag" @touchstart="startDrag" />
    <div class="ma-2">
      <v-container class="pa-0 d-flex justify-center" style="margin-top: 20px; max-width: 410px">
        <div class="row justify-left ml-5">
          <div class="panel-section-items">
            <v-list class="list-label-value" style="height: 120px;">
              <v-list-item>
                <campus-search
                  ref="fromRoute"
                  :is-route="true"
                  :route-label="locale.startRouteLabel"
                  icon="mdi-flag"
                  route-type="from"
                  data-test="fromSearch"
                  @selectSearchResult="onSearchSelect"
                  @clearClicked="onClearSearchField('from')"
                />
              </v-list-item>
              <v-list-item>
                <campus-search
                  ref="toRoute"
                  :is-route="true"
                  :route-label="locale.endRouteLabel"
                  icon="mdi-flag-checkered"
                  route-type="to"
                  data-test="toSearch"
                  @selectSearchResult="onSearchSelect"
                  @clearClicked="onClearSearchField('to')"
                />
              </v-list-item>
            </v-list>
            <v-list class="list-label-value">
              <v-list-item>
                <v-checkbox v-model="barrierFree" :label="locale.barrierFreeLabel" data-test="barrierFreeCheckbox" @update:model-value="onBarrierFreeChange" />
              </v-list-item>
              <v-list-item>
                <div class="mt-3 routing-info-text">
                  {{ $t('label_directions_only_routes_on_campus_supported') }}
                {{  $t('label_directions_routing_barrierfree_limitations') }}</div>
              </v-list-item>
            </v-list>

          </div>
        </div>
        <v-divider v-if="routeInfo" class="mt-5 mb-5" />
        <div v-if="routeInfo" class="row justify-center">
          <div class="panel-section-items">
            <v-list class="list-label-value">
              <v-list-item v-if="routeInfo?.walk_time">
                <span class="text-primary text-h5 font-weight-bold text-center">{{
                  routeInfo.walk_time
                }} ({{ routeInfo.route_length }} m)</span>
              </v-list-item>
              <v-list-item v-if="routeInfo?.start_name">
                <v-icon class="search-btn">
                  mdi-flag
                </v-icon>
                <span>{{ locale.startRouteLabel }} : {{ routeInfo.start_name }}</span>
              </v-list-item>
              <v-list-item v-if="routeInfo?.passes">
                <v-icon class="search-btn">
                  mdi-map-marker
                </v-icon>
                <span>{{ locale.routePassessLabel }} </span>
              </v-list-item>
              <v-list-item v-if="routeInfo?.end_name">
                <v-icon class="search-btn">
                  mdi-flag-checkered
                </v-icon>
                <span>{{ locale.endRouteLabel }} : {{ routeInfo.end_name }}</span>
              </v-list-item>
            </v-list>
          </div>
        </div>
        <div v-if="noRouteFound || error" class="row justify-left ml-5">
          <div class="panel-section-items">
            <v-list class="list-label-value">
              <v-list-item v-if="noRouteFound">
                <span style="color: red">
                  {{ locale.noRouteFoundText }}
                </span>
              </v-list-item>
              <v-list-item v-if="error">
                <span style="color: red">
                  {{ error }}
                </span>
              </v-list-item>
            </v-list>
          </div>
        </div>
        <v-divider class="mt-5 mb-5" />
        <div class="row justify-left ml-5">
          <div class="panel-section-items">
            <v-list class="list-label-value">
              <v-list-item>
                <v-btn
                  :disabled="!isRouteAvailable"
                  color="blue-grey"
                  class="text-white"
                  size="small"
                  data-test="goButton"
                  @click="onGoButtonClick"
                >
                  <v-icon start class="text-white">
                    mdi-run
                  </v-icon>
                  <span>{{ locale.goLabel }}!</span>
                </v-btn>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      :disabled="!isRouteAvailable"
                      color="blue-grey"
                      class="text-white ml-1"
                      size="small"
                      @click="onShareRoute"
                      v-bind="props"
                    >
                      <v-icon class="text-white">
                        mdi-share
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>{{ locale.shareRoute }}</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      :disabled="!isRouteAvailable"
                      color="blue-grey"
                      class="text-white ml-1"
                      size="small"
                      @click="onClearRoute"
                      v-bind="props"
                    >
                      <v-icon class="text-white">
                        mdi-close
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>{{ locale.clearRouteLabel }}</span>
                </v-tooltip>
              </v-list-item>
            </v-list>
          </div>
        </div>
      </v-container>
    </div>
  </v-navigation-drawer>
  </div>
</template>

<script>
import config from '../../util/indrzConfig';
import CampusSearch from '../CampusSearch.vue';
import BaseDrawer from './BaseDrawer';
import bus from '~/util/bus';

const { env } = config;

// function getName (data, locale) {
//   if (data === null || data === undefined) {
//     return null;
//   }
//   const name = data[`name_${locale}`];
//   return name !== undefined && name !== null ? name : data.name;
// }

export default {
  name: 'RouteDrawer',
  components: {
    CampusSearch
  },
  mixins: [BaseDrawer],
  data () {
    return {
      poiRoute: false,
      barrierFree: false,
      fromRoute: null,
      toRoute: null,
      locale: {
        startRouteLabel: this.$t('route_from_here'),
        endRouteLabel: this.$t('route_to_here'),
        clearRouteLabel: this.$t('clear_route'),
        routePassessLabel: this.$t('route_passess'),
        barrierFreeLabel: this.$t('barrier_free_route'),
        routeLabel: this.$t('route'),
        noRouteFoundText: this.$t('no_route_found'),
        shareRoute: this.$t('shareRoute'),
        goLabel: this.$t('go')
      },
      routeInfo: null,
      noRouteFound: false,
      error: null
    }
  },
  computed: {
    logo () {
      return {
        file: env.LOGO_FILE,
        enabled: (env.LOGO_ENABLED === true)
      };
    },
    isRouteAvailable () {
      return this.fromRoute && this.toRoute;
    }
  },

  mounted () {
    bus.on('setRoute', this.setRoute);
    bus.on('setRouteInfo', this.setRouteInfo);
    bus.on('noRouteFound', this.setNoRouteFound);
    bus.on('routeError', this.setRouteError);
    bus.on('updateRouteFields', this.setSearchFieldRouteText);
  },
  beforeUnmount () {
    bus.off('setRoute', this.setRoute);
    bus.off('setRouteInfo', this.setRouteInfo);
    bus.off('noRouteFound', this.setNoRouteFound);
    bus.off('routeError', this.setRouteError);
    bus.off('updateRouteFields', this.setSearchFieldRouteText);
  },

  methods: {
    currentLocale () {
      const raw = this.$i18n?.locale
      return raw && typeof raw === 'object' && 'value' in raw ? raw.value : raw
    },
    clearDirections () {
      bus.emit('clearSearch')
      bus.emit('closeInfoPopup')
      this.$emit('hide-poi-drawer')
      bus.emit('clearRoute')
      this.$emit('on-close')
    },
    onSearchSelect (selectedItem) {
      if (!selectedItem || !selectedItem.data) {
        return;
      }
      const currentSelection = { ...selectedItem };
      const { id, properties } = selectedItem.data;

      if (!properties.space_id && properties.spaceid) {
        properties.space_id = properties.spaceid;
      } else if (properties?.src_icon === 'space' || properties?.space_type_id || properties?.space_type) {
        properties.space_id = id;
      }

      if (properties.shelfId) {
        properties.coords = currentSelection.data.geometry.coordinates;
      }
      this[selectedItem.routeType + 'Route'] = currentSelection.data;

      this.$emit('setGlobalRoute', selectedItem);
      if (this.fromRoute && this.toRoute) {
        this.onGoButtonClick();
      }
    },
    onGoButtonClick () {
      this.$emit('routeGo', this.barrierFree ? 1 : 0);
    },
    onShareRoute () {
      bus.emit('shareClick', true);
    },
    onClearSearchField (routeType) {
      this[routeType + 'Route'] = null;
      this.setRouteError(null);
      bus.emit('clearRoute')
    },
    onClearRoute () {
      this.$refs.fromRoute.clearSearch();
      this.fromRoute = null;
      this.toRoute = null;
      if (this.$refs.toRoute) { this.$refs.toRoute.clearSearch(''); }
      this.setRouteError(null);
      bus.emit('clearRoute')
    },
    clearMessages () {
      this.routeInfo = null;
      this.error = null;
    },
    onBarrierFreeChange () {
      if (this.fromRoute && this.toRoute) {
        this.onGoButtonClick();
      }
    },
    setSearchFieldRouteText (routeInfo) {
      const fieldExtensions = ['from', 'to'];
      fieldExtensions.forEach((extension) => {
        const field = this.$refs[extension + 'Route'];
        const model = { ...field.model || {}, ...routeInfo[extension + 'Data'] };

        field.stopSearch = true;
        field.searchResult = [model];
        field.model = model;
        setTimeout(() => {
          field.stopSearch = false;
        }, 1000);
      });
    },
    setRoute (routeInfo) {
      const routeData = { ...routeInfo.data, ...this.getInputFieldDisplayName() };
      const path = routeInfo.path && routeInfo.path !== undefined ? routeInfo.path : this.fromRoute ? 'to' : 'from'
      if (!routeData.name && routeData.room_code) {
        routeData.name = routeData.room_code;
      }
      if (!routeData.space_id && (routeData?.src_icon === 'space' || routeData?.space_type_id || routeData?.space_type)) {
        routeData.space_id = routeData.id;
      }
      const data = {
        properties: routeData,
        type: 'Feature',
        geometry: {}
      };
      const field = this.$refs[path + 'Route'];
      if (!field) {
        return;
      }
      const { properties } = data;
      const model = {
        ...properties,
        ...{
          floorNum: properties.floor_num || properties.floor,
          roomCode: properties.room_code
        }
      };

      field.stopSearch = true;
      field.apiResponse = [data];
      field.searchResult = [model];
      field.model = model;

      this[path + 'Route'] = data;
      this.$emit('setGlobalRoute', {
        data,
        routeType: path
      });

      setTimeout(() => {
        field.stopSearch = false;
        if (this.fromRoute && this.toRoute) {
          this.onGoButtonClick();
        }
      }, 1000);
    },

    setRouteInfo (routeInfo) {
      this.clearMessages();
      if (!routeInfo) {
        this.setNoRouteFound(true)
        return;
      }
      this.setNoRouteFound(false)

      const routeTime = routeInfo.walk_time;
      const minutes = Math.floor(routeTime / 60);
      const seconds = routeTime - minutes * 60;
      const mins = 'minutes';
      const secs = 'seconds';
      const walkTimeString = minutes + ' ' + mins + ' ' + Math.floor(seconds) + ' ' + secs;

      this.routeInfo = { ...routeInfo, walk_time: walkTimeString, ...this.getInputFieldDisplayName() };
    },
    getInputFieldDisplayName () {
      const fromData = this.$refs.fromRoute?.$data?.model;
      const toData = this.$refs.toRoute?.$data?.model;

      const names = {}

      if (fromData) {
        names.start_name = fromData[`name_${this.currentLocale()}`] || fromData.name
      }
      if (toData) {
        names.end_name = toData[`name_${this.currentLocale()}`] || toData.name
      }

      return names;
    },
    setNoRouteFound (state = true) {
      this.noRouteFound = state
      state && this.clearMessages()
    },
    setRouteError (error) {
      this.error = error;
      this.setNoRouteFound(false)
      this.routeInfo = null
    }
  }
};
</script>

<style scoped>
.routing-info-text {
  font-size: 12px;
  color: #898989;
}
</style>
