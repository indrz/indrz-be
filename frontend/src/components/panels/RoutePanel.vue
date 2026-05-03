<template>
  <div class="route-panel">
    <!-- Header is now provided by LeftPanel -->

    <v-container class="pa-4" style="max-width: 410px">
      <v-row dense>
        <v-col cols="12">
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
        </v-col>

        <v-col cols="12">
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
        </v-col>

        <!-- Buttons directly below both search fields -->
        <v-col cols="12" class="d-flex flex-wrap ga-2">
          <v-btn
            :disabled="!isRouteAvailable"
            color="blue-grey"
            class="text-white"
            size="small"
            data-test="goButton"
            @click="onGoButtonClick"
          >
            <v-icon start class="text-white">mdi-run</v-icon>
            <span>{{ locale.goLabel }}!</span>
          </v-btn>

          <v-tooltip location="top">
            <template #activator="{ props }">
              <v-btn
                :disabled="!isRouteAvailable"
                color="blue-grey"
                class="text-white"
                size="small"
                @click="onShareRoute"
                v-bind="props"
              >
                <v-icon class="text-white">mdi-share</v-icon>
              </v-btn>
            </template>
            <span>{{ locale.shareRoute }}</span>
          </v-tooltip>

          <v-tooltip location="top">
            <template #activator="{ props }">
              <v-btn
                :disabled="!isRouteAvailable"
                color="blue-grey"
                class="text-white"
                size="small"
                @click="onClearRoute"
                v-bind="props"
              >
                <v-icon class="text-white">mdi-close</v-icon>
              </v-btn>
            </template>
            <span>{{ locale.clearRouteLabel }}</span>
          </v-tooltip>
        </v-col>

        <v-col cols="12">
          <v-checkbox v-model="barrierFree" :label="locale.barrierFreeLabel" data-test="barrierFreeCheckbox" @update:model-value="onBarrierFreeChange" />
          <div class="mt-2 routing-info-text">
            {{ $t('label_directions_only_routes_on_campus_supported') }}
            {{ $t('label_directions_routing_barrierfree_limitations') }}
          </div>
        </v-col>
      </v-row>

      <v-divider v-if="routeInfo" class="my-4" />

      <div v-if="routeInfo">
        <v-list class="list-label-value">
          <v-list-item v-if="routeInfo?.walk_time">
            <span class="text-primary text-h5 font-weight-bold text-center">{{ routeInfo.walk_time }} ({{ routeInfo.route_length }} m)</span>
          </v-list-item>
          <v-list-item v-if="routeInfo?.start_name">
            <v-icon class="search-btn">mdi-flag</v-icon>
            <span>{{ locale.startRouteLabel }} : {{ routeInfo.start_name }}</span>
          </v-list-item>
          <v-list-item v-if="routeInfo?.passes">
            <v-icon class="search-btn">mdi-map-marker</v-icon>
            <span>{{ locale.routePassessLabel }} </span>
          </v-list-item>
          <v-list-item v-if="routeInfo?.end_name">
            <v-icon class="search-btn">mdi-flag-checkered</v-icon>
            <span>{{ locale.endRouteLabel }} : {{ routeInfo.end_name }}</span>
          </v-list-item>
        </v-list>
      </div>

      <div v-if="noRouteFound || error" class="mt-2">
        <div v-if="noRouteFound" style="color: red">
          {{ locale.noRouteFoundText }}
        </div>
        <div v-if="error" style="color: red">
          {{ error }}
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
import CampusSearch from '@/components/CampusSearch.vue';
import bus from '~/util/bus';

export default {
  name: 'RoutePanel',
  components: {
    CampusSearch
  },
  emits: ['setGlobalRoute', 'routeGo', 'close', 'hide-poi-drawer'],
  data () {
    return {
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
  methods: {
    clearDirections () {
      bus.emit('clearSearch');
      bus.emit('closeInfoPopup');
      this.$emit('hide-poi-drawer');
      bus.emit('clearRoute');
      this.$emit('close');
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
      bus.emit('clearRoute');
    },
    onClearRoute () {
      if (this.$refs.fromRoute) {
        this.$refs.fromRoute.clearSearch();
      }
      this.fromRoute = null;
      this.toRoute = null;
      if (this.$refs.toRoute) {
        this.$refs.toRoute.clearSearch('');
      }
      this.setRouteError(null);
      bus.emit('clearRoute');
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
        if (!field) {
          return;
        }
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
      this.routeInfo = routeInfo;
      this.noRouteFound = false;
      this.setRouteError(null);
    },
    setRouteInfo (routeInfo) {
      this.routeInfo = routeInfo;
      this.noRouteFound = false;
      this.setRouteError(null);
    },
    setNoRouteFound (value) {
      this.noRouteFound = value;
    },
    setRouteError (error) {
      this.error = error;
    }
  }
};
</script>

<style scoped>
.route-panel {
  width: 100%;
}

.routing-info-text {
  font-size: 0.85rem;
  opacity: 0.9;
}

.search-btn {
  margin-right: 8px;
}
</style>

