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
  <v-navigation-drawer
    ref="drawer"
    v-model="shouldShowDrawer"
    class="resizable"
    bottom
    :style="{ width: isMobile ? '100%' : '410px', height: drawerHeight + 'px', top: 'auto', bottom: 0, position:'fixed' }"
    app
    fixed
    :permanent="shouldShowDrawer"
    data-test="directionsPane"
    @transitionend="onTransitionEnd"
    stateless
  >
    <v-app-bar
      color="deep-purple accent-4"
      dark
    >
      <v-toolbar-title>{{ locale.routeLabel }}</v-toolbar-title>
      <v-btn icon @click="clearDirections">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-app-bar>
    <div v-if="isMobile" class="draggable-handle" @mousedown="startDrag" @touchstart="startDrag" />
    <div class="ma-2">
      <v-container justify="center" class="pa-0" style="margin-top: 20px; max-width: 410px">
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
                <v-checkbox v-model="barrierFree" :label="locale.barrierFreeLabel" data-test="barrierFreeCheckbox" @change="onBarrierFreeChange" />
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
                <span class="primary--text text-h5 font-weight-bold text-center">{{
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
                  class="white--text"
                  small
                  data-test="goButton"
                  @click="onGoButtonClick"
                >
                  <v-icon left dark>
                    mdi-run
                  </v-icon>
                  <span>{{ locale.goLabel }}!</span>
                </v-btn>
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      :disabled="!isRouteAvailable"
                      color="blue-grey"
                      class="white--text ml-1"
                      small
                      @click="onShareRoute"
                      v-on="on"
                    >
                      <v-icon dark>
                        mdi-share
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>{{ locale.shareRoute }}</span>
                </v-tooltip>
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      :disabled="!isRouteAvailable"
                      color="blue-grey"
                      class="white--text ml-1"
                      small
                      @click="onClearRoute"
                      v-on="on"
                    >
                      <v-icon dark>
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
</template>

<script>
import config from '../../util/indrzConfig';
import CampusSearch from '../CampusSearch.vue';
import BaseDrawer from './BaseDrawer';

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
    this.$root.$on('setRoute', this.setRoute);
    this.$root.$on('setRouteInfo', this.setRouteInfo);
    this.$root.$on('noRouteFound', this.setNoRouteFound);
    this.$root.$on('routeError', this.setRouteError);
    this.$root.$on('updateRouteFields', this.setSearchFieldRouteText)
  },

  methods: {
    clearDirections () {
      this.$root.$emit('clearSearch')
      this.$root.$emit('closeInfoPopup')
      this.$emit('hide-poi-drawer')
      this.$root.$emit('clearRoute')
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
      this.$root.$emit('shareClick', true);
    },
    onClearSearchField (routeType) {
      this[routeType + 'Route'] = null;
      this.setRouteError(null);
      this.$root.$emit('clearRoute')
    },
    onClearRoute () {
      this.$refs.fromRoute.clearSearch();
      this.fromRoute = null;
      this.toRoute = null;
      if (this.$refs.toRoute) { this.$refs.toRoute.clearSearch(''); }
      this.setRouteError(null);
      this.$root.$emit('clearRoute')
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
        names.start_name = fromData[`name_${this.$i18n.locale}`] || fromData.name
      }
      if (toData) {
        names.end_name = toData[`name_${this.$i18n.locale}`] || toData.name
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
