<template>
  <div data-test="sideBar">
    <div>
      <v-row class="sidebar-start mt-5 mt-lg-0" no-gutters>
        <v-col :cols="2" class="pa-2">
          <v-app-bar-nav-icon data-test="closeLeftPaneBtn" @click.stop="onNavbarClick" />
        </v-col>
        <v-col :cols="8" align-self="center">
          <img id="tu-logo" data-test="leftPaneLogo" :src="logo.file" alt="logo" class="left-bar-logo">
        </v-col>
      </v-row>
    </div>
    <v-expansion-panels v-model="expanded" multiple>
      <v-expansion-panel v-for="menuItem in menuItems" :key="menuItem.title">
        <v-expansion-panel-title class="sidebar-expansion-header" :data-test="menuItem.type+'Heading'">
          {{ menuItem.title }}
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <component
            :is="menuItem.type"
            :ref="menuItem.type"
            :initial-poi-cat-id="initialPoiCatId"
            :initial-poi-id="initialPoiId"
            :search-result="searchResult"
            :data-test="menuItem.type+'Content'"
            @locationClick="onLocationClick"
            @setGlobalRoute="onSetGlobalRoute"
            @routeGo="onRouteGo"
            @clearRoute="onClearRoute"
            @shareClick="onShareClick"
            @poiLoad="addPoi"
          />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-list
      class="mt-5"
      nav
      density="compact"
    >
      <v-list-item
        v-for="(item, i) in menuButtons"
        :key="i"
        :data-test="item.type+'Btn'"
        :aria-label="item.text"
        @click.stop="onMenuBUttonClick(item)"
      >
        <template #prepend>
          <v-icon :data-test="item.type+'Item'">
            mdi-{{ item.icon }}
          </v-icon>
        </template>
        <v-list-item-title v-text="item.text" />
      </v-list-item>
    </v-list>
    <div>
      <p class="font-weight-regular text-caption" style="padding: 8px 16px 0px">
        Powered by <a href="https://indrz.com/#contact" target="_blank">indrz.com</a>
      </p>
      <p class="font-weight-regular text-caption" style="padding: 0px 16px">
        Version: {{ appVersion }}
      </p>
    </div>
  </div>
</template>

<script>
import config from '../util/indrzConfig';
import CampusLocations from './CampusLocations';
import SearchResult from './SearchResult';
import PointsOfInterest from './poi/PointsOfInterest';
import bus from '~/util/bus';

const { env } = config;

export default {
  name: 'SideBar',
  components: {
    CampusLocations,
    PointsOfInterest,
    SearchResult
  },
  props: {
    openedPanels: {
      type: Array,
      default: function () {
        return [];
      }
    },
    initialPoiCatId: {
      type: Array,
      default: function () {
        return [];
      }
    },
    initialPoiId: {
      type: String,
      default: function () {
        return null;
      }
    }
  },
  data () {
    return {
      searchResult: []
    };
  },

  computed: {
    locale () {
      // Keep labels reactive when the active locale changes.
      return {
        campusLocations: this.$t('campus_locations'),
        searchResult: this.$t('search_result'),
        pointsOfInterest: this.$t('points_of_interest'),
        zooToHome: this.$t('zoom_to_home'),
        shareMap: this.$t('share_map'),
        download: this.$t('download'),
        pdf: this.$t('pdf'),
        helpLegendInfos: this.$t('help_legend_infos'),
        aboutTermsConditions: this.$t('about_terms_conditions'),
        scanQRShowMyLocation: this.$t('scan_qr_show_my_location'),
        directions: this.$t('route')
      };
    },
    logo () {
      return {
        file: env.LOGO_FILE,
        enabled: (env.LOGO_ENABLED === true)
      };
    },
    menuItems () {
      return [
        {
          type: 'CampusLocations',
          title: this.locale.campusLocations
        },
        {
          type: 'PointsOfInterest',
          title: this.locale.pointsOfInterest
        }
        /*,
        {
          type: 'SearchResult',
          title: this.locale.searchResult
        }
        */
      ];
    },
    menuButtons () {
      return [
        {
          icon: 'directions',
          type: 'directions',
          text: this.locale.directions
        },
        {
          icon: 'home',
          type: 'zoom-home',
          text: this.locale.zooToHome
        },
        {
          icon: 'share-variant',
          type: 'share-map',
          text: this.locale.shareMap
        },
        {
          icon: 'image-area-close',
          type: 'download',
          text: this.locale.download
        },
        {
          icon: 'map',
          type: 'pdf',
          text: this.locale.pdf
        },
        {
          icon: 'help-box',
          type: 'help',
          text: this.locale.helpLegendInfos
        },
        {
          icon: 'clipboard-text',
          type: 'terms',
          text: this.locale.aboutTermsConditions
        },
        {
          icon: 'qrcode-scan',
          type: 'qrcode',
          text: this.locale.scanQRShowMyLocation
        }
      ];
    },
    appVersion () {
      return env.APP_VERSION
    },
    expanded: {
      get () {
        return this.openedPanels;
      },
      set (value) {
        bus.emit('update-opened-panels', value)
      }
    }
  },

  methods: {
    onMenuBUttonClick (item) {
      this.$emit('menuButtonClick', item.type);
    },
    onLocationClick (centroid, zoom = 18) {
      this.$emit('locationClick', centroid, zoom);
    },
    onSetGlobalRoute (value) {
      this.$emit('setGlobalRoute', value);
    },
    onRouteGo (routeType) {
      this.$emit('routeGo', routeType);
    },
    onShareClick () {
      this.$emit('shareClick');
    },
    onClearRoute () {
      this.$emit('clearRoute');
    },
    addPoi (data) {
      this.$emit('poiLoad', data);
    },
    onNavbarClick () {
      this.$emit('hideSidebar');
    }
  }
};
</script>

<style lang="scss">
  .left-bar-logo {
    width: auto;
    height: 40px;
    left: 10px;
    vertical-align: middle;
    display: block;
    margin: 5px auto;
  }
  /*
  Style for Tree
   */
  :deep(.v-treeview-node__label) {
    /*
    font-family: "Roboto", sans-serif;
    font-size: .8125rem !important;
    */
  }
  /*
  Style for Menu items
   */
  :deep(.v-list-item__title) {
    /*
    font-family: "Roboto", sans-serif;
    font-size: .8125rem !important;
    */
  }
  /*
  Style for Menu expansion header
   */
  .sidebar-expansion-header {
    /*
    font-family: "Roboto", sans-serif;
    font-size: 0.9375rem !important;
    */
  }
  @media(max-width:767.98px) {
    .sidebar-start {
    margin-top:20px;
    }
  }
  .v-overlay{
    z-index:0 !important;
  }
</style>
