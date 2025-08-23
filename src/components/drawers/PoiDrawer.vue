<template>
  <div>
    <!--    <drawer-search
      v-if="isMobile"
      :map="baseMap"
      :drawer="mainDrawer"
      :search-title="searchTitle"
      class="mt-4"
      id="drawer-search"
      @update:drawer="mainDrawer = $event"
      @hide-poi-drawer="onHidePoiDrawer()"
    />-->
    <!--    <v-navigation-drawer
      ref="drawer"
      v-model="shouldShowDrawer"
      class="resizable"
      :style="{ width: '410px', height: drawerHeight + 'px' }"
      hide-overlay
      app
      fixed
      bottom
      data-test="poiLeftPane"
    >-->
    <v-navigation-drawer
      ref="drawer"
      v-model="shouldShowDrawer"
      class="resizable"
      :style="{ width: isMobile ? '100%' : '410px', height: drawerHeight + 'px', top: 'auto', bottom: 0, position:'fixed' }"
      hide-overlay
      app
      fixed
      :permanent="shouldShowDrawer"
      stateless
      data-test="poiLeftPane"
    >
      <div v-if="isMobile" class="draggable-handle" @mousedown="startDrag" @touchstart="startDrag" />
      <div v-if="!poiImages">
        <v-card
          flat
          style="margin-top: 10px"
        >
          <v-row justify="center">
            <v-img
              :max-width="410"
              :aspect-ratio="3"
              :src="data.images ? `${baseUrl}${data.images[0].image}` : `${defaultPoiImage}`"
              lazy-src="`${defaultPoiImage}`"
              alt="image of poi"
            >
              <template v-slot:placeholder>
                <v-row
                  class="fill-height ma-0"
                  align="center"
                  justify="center"
                >
                  <v-progress-circular
                    indeterminate
                    color="primary lighten-1"
                  />
                </v-row>
              </template>
              <drawer-search
                v-if="!isMobile"
                :key="`drawer-search-${updateKey}`"
                :map="baseMap"
                :drawer="mainDrawer"
                :selected="data"
                class="mt-4"
                @update:drawer="mainDrawer = $event"
                @hide-poi-drawer="onHidePoiDrawer()"
              />
              <div
                v-if="data?.images?.length"
                class="image-button"
              >
                <v-btn
                  class="ma-2"
                  color="rgba(0,0,0,0.4)"
                  dark
                  tonal
                  @click="poiImages = !poiImages"
                >
                  <v-icon dark left>
                    mdi-folder-multiple-image
                  </v-icon>
                  {{ data.images.length }} - {{ locale.labelPoiPictures }}
                </v-btn>
              </div>
            </v-img>
          </v-row>
          <v-card-text class="pb-0">
            <v-tabs
              v-model="activeTabIndex"
              class="poi-tabs ma-0"
              centered
              color="primary"
              icons-and-text
              hide-slider
            >
              <v-tab v-for="(tabInfo, index) in tabs" :key="index" @click="onTabClick(index)">
                {{ tabInfo.text }}
                <v-icon>{{ tabInfo.icon }}</v-icon>
              </v-tab>
            </v-tabs>
            <v-tabs-items v-model="activeTabIndex">
              <v-tab-item>
                <div />
              </v-tab-item>

              <v-tab-item>
                <v-divider class="my-3 my-lg-3" />
                <div class="row justify-center">
                  <div class="panel-section-items">
                    <v-list>
                      <v-list-item>
                        <v-list-item-icon v-if="data.icon || data.src_icon">
                          <v-img
                            v-if="data.icon"
                            :max-width="20"
                            :src="data.icon"
                            alt="icon image"
                          />
                          <v-img
                            v-else
                            :src="getIconUrl(data.src_icon)"
                            contain
                            max-height="24"
                            max-width="24"
                            alt="icon image"
                          />
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title data-test="searchTitle" class="text-h6 primary--text" v-text="searchTitle" />
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </div>
                </div>

                <v-divider class="my-3 my-lg-5" />

                <div class="row justify-center">
                  <div class="panel-section-items">
                    <v-list class="list-label-value">
                      <v-list-item v-if="data.html_content">
                        <span v-html="data.html_content" />
                      </v-list-item>
                      <v-list-item v-if="data.src === 'wms_campus'">
                        <span>{{ locale.labelBuidingAdress }}</span>
                        <span>{{ data.description }}</span>
                      </v-list-item>
                      <template v-if="data.street">
                        <v-list-item>
                          <span>{{ locale.labelBuidingAdress }}</span>
                          <span>{{ data.street }}</span>
                        </v-list-item>
                        <v-list-item>
                          <span>{{ locale.labelBuildingCode }}</span>
                          <span>{{ data.name }}</span>
                        </v-list-item>
                        <v-list-item>
                          <span>{{ locale.labelBuidingPlz }}</span>
                          <span>{{ data.postal_code }}</span>
                        </v-list-item>
                        <v-list-item>
                          <span>{{ locale.labelBuildingCity }}</span>
                          <span>{{ data.city }}</span>
                        </v-list-item>
                      </template>
                      <v-list-item v-if="data.room_code" data-test="roomCode">
                        <span>{{ locale.labelRoomCode }}</span>
                        <span>{{ data.room_code }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.floor_name && !data.xy">
                        <span>{{ locale.labelFloorName }}</span>
                        <span>{{ data.floor_name }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.wing && !data.xy">
                        <span>{{ locale.label_wing_name }}</span>
                        <span>{{ data.wing }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.building_name || data.building">
                        <span>{{ locale.labelBuildingName }}</span>
                        <span>{{ data.building_name || data.building }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.category_en">
                        <span>{{ locale.labelCategory }}</span>
                        <span>{{ data.category_en }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.nearest_entrance">
                        <span>{{ locale.labelPoiName }}</span>
                        <span>{{ data.nearest_entrance }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.room_external_id">
                        <span>{{ locale.labelRoomId }}</span>
                        <span>{{ data.room_external_id }}</span>
                      </v-list-item>
                      <v-list-item v-if="data.capacity">
                        <span>{{ locale.labelCapacity }}</span>
                        <span>{{ data.capacity }}</span>
                      </v-list-item>

                      <v-list-item v-if="data.postal_code">
                        <span>{{ $t('label_building_plz') }}</span>
                        <span>{{ data.postal_code }}</span>
                      </v-list-item>

                      <v-list-item v-if="data.city">
                        <span>{{ $t('label_building_city') }}</span>
                        <span>{{ data.city }}</span>
                      </v-list-item>

                      <v-list-item v-if="data.xy">
                        <span>{{ $t('label_xy') }}</span>
                        <span>X: {{ data.xy[0] }}, Y: {{ data.xy[1] }}</span>
                      </v-list-item>
                      <template v-if="data.xy">
                        <v-list-item>
                          <span>{{ X }}</span>
                          <span>{{ data.xy[0].toFixed(3) }}</span>
                        </v-list-item>
                        <v-list-item>
                          <span>{{ Y }}</span>
                          <span>{{ data.xy[1].toFixed(3) }}</span>
                        </v-list-item>
                      </template>
                      <v-list-item v-if="data.external_id">
                        <span>{{ locale.labelExternalId }}</span>
                        <span>{{ data.external_id }}</span>
                      </v-list-item>
                    </v-list>
                  </div>
                </div>
                <v-divider class="my-3 my-lg-3" />
                <div class="row justify-center">
                  <div class="panel-section-items">
                    <v-list class="list-buttons">
                      <v-list-item v-for="(button, index) in listButtons" :key="index">
                        <v-btn
                          small
                          text
                          color="wu"
                          class="pl-0"
                          :aria-label="button.label"
                          @click.stop="button.handler"
                        >
                          <v-icon left>
                            {{ button.icon }}
                          </v-icon>
                          {{ button.label }}
                        </v-btn>
                      </v-list-item>
                    </v-list>
                  </div>
                </div>
              </v-tab-item>
              <v-tab-item>
                <div />
              </v-tab-item>
            </v-tabs-items>
          </v-card-text>
        </v-card>
      </div>

      <div v-if="poiImages">
        <v-container>
          <v-row no-gutters>
            <v-col cols="2">
              <v-btn
                icon
                @click="poiImages = !poiImages"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="1" class="title-items">
              <v-img
                :max-width="20"
                :src="data.icon"
                alt="icon image for title"
              />
            </v-col>
            <v-col cols="9" class="title-items">
              <span class="primary--text subtitle-1">{{ data.name_en }}</span>
            </v-col>
          </v-row>
          <v-row v-for="(image, index) in data.images" :key="index" justify="center">
            <v-img
              :max-width="410"
              :aspect-ratio="2"
              :src="`${baseUrl}${image.image}`"
              lazy-src="`${defaultPoiImage}`"
              class="gallery-thumb"
              style="margin: 5px;"
              alt="image for poi"
              @click="onGalleryImageClick(index)"
            />
          </v-row>
        </v-container>
      </div>
      <photo-gallery :show="showGallery" :images="data.images" :selcted-index="galleryImageIndex" @gallery:show="showGallery=$event" />
    </v-navigation-drawer>
  </div>
</template>

<script>
import config from '../../util/indrzConfig';
import CampusSearch from '../CampusSearch.vue';
import PhotoGallery from '../PhotoGallery';
import DrawerSearch from './DrawerSearch.vue';
import BaseDrawer from './BaseDrawer';
import MapHandler from '@/util/mapHandler';

const { env } = config;

export default {
  name: 'PoiDrawer',
  components: {
    CampusSearch,
    DrawerSearch,
    PhotoGallery
  },
  mixins: [BaseDrawer],
  data () {
    return {
      updateKey: 1,
      poiImages: false,
      showGallery: false,
      galleryImageIndex: 0,
      locale: {
        entranceButtonText: this.$t('entrance_button_text'),
        metroButtonText: this.$t('metro_button_text'),
        routeFromHereText: this.$t('route_from_here'),
        routeToHereText: this.$t('route_to_here'),
        labelRoomCode: this.$t('label_room_code'),
        labelFloorName: this.$t('label_floor_name'),
        labelBuildingName: this.$t('label_building_name'),
        labelCategory: this.$t('label_category'),
        labelPoiName: this.$t('label_nearest_entrance'),
        labelRoomId: this.$t('label_room_id'),
        labelCapacity: this.$t('label_capacity'),
        labelBuidingAdress: this.$t('label_building_adress'),
        labelBuildingCode: this.$t('label_building_code'),
        labelBuidingPlz: this.$t('label_building_plz'),
        labelBuildingCity: this.$t('label_building_city'),
        labelPoiPictures: this.$t('poi_pictures'),
        share_button_tip: this.$t('share_button_tip'),
        entranceButtonTip: this.$t('entrance_button_tip'),
        metroButtonTip: this.$t('metro_button_tip'),
        defiButtonTip: this.$t('defi_button_tip'),
        shareButtonTip: this.$t('share_button_tip'),
        label_wing_name: this.$t('label_wing_name')
      },
      tabs: [
        { icon: 'mdi-directions', text: 'Routing' },
        { icon: 'mdi-information', text: 'Info' },
        { icon: 'mdi-share', text: 'Share' },
        { icon: 'mdi-close', text: 'Close' }
      ],
      activeTabIndex: 1,
      iconNames: ['book', 'department', 'person', 'poi', 'space'],
      iconPath: '/images/icons/search/'
    }
  },
  computed: {
    logo () {
      return {
        file: env.LOGO_FILE,
        enabled: (env.LOGO_ENABLED === true)
      };
    },
    defaultPoiImage () {
      return env.DEFAULT_POI_IMAGE
    },
    baseUrl () {
      return env.BASE_URL
    },
    searchTitle () {
      const { data } = this;
      return MapHandler.getTitle(data, this.$i18n.locale)
    },
    listButtons () {
      return [
        {
          icon: 'mdi-map-marker',
          label: this.locale.routeFromHereText,
          handler: () => { return this.onRouteClick('from') }
        },
        {
          icon: 'mdi-map-marker',
          label: this.locale.routeToHereText,
          handler: () => { return this.onRouteClick('to') }
        },
        {
          icon: 'mdi-routes',
          label: this.locale.entranceButtonText,
          handler: this.onEntranceButtonClick
        },
        {
          icon: 'mdi-routes',
          label: this.locale.metroButtonText,
          handler: this.onMetroButtonClick
        },
        {
          icon: 'mdi-heart-flash',
          label: this.locale.defiButtonTip,
          handler: this.onDefiButtonClick
        },
        {
          icon: 'mdi-share',
          label: this.locale.share_button_tip,
          handler: this.onShareButtonClick
        }

      ]
    }
  },
  watch: {
    data: {
      deep: true,
      handler (val) {
        this.poiImages = false;
        this.activeTabIndex = 1;
        this.updateKey++;
      }
    }
  },
  methods: {
    onEntranceButtonClick () {
      this.$root.$emit('popupRouteClick', 'from');
      this.$root.$emit('popupEntranceButtonClick');
    },
    onMetroButtonClick () {
      this.$root.$emit('popupRouteClick', 'from');
      this.$root.$emit('popupMetroButtonClick');
    },
    onDefiButtonClick () {
      this.$root.$emit('popupRouteClick', 'from');
      this.$root.$emit('popupDefiButtonClick');
    },
    onShareButtonClick () {
      this.$root.$emit('shareClick');
    },
    onRouteClick (path) {
      this.$root.$emit('popupRouteClick', path);
    },
    onTabClick (index) {
      if (index === 2) {
        this.onShareButtonClick()
      } else if (index === 0) {
        this.onRouteClick('from')
        // this.$emit('open-route-drawer');
      } else if (index === 3) {
        this.$root.$emit('closeInfoPopup');
        this.$emit('hide-poi-drawer')
      }
    },
    onGalleryImageClick (index = 0) {
      this.galleryImageIndex = index;
      this.showGallery = !this.showGallery;
    },
    getIconUrl (iconName) {
      if (!iconName) {
        return '';
      }
      if (this.iconNames.includes(iconName)) {
        return `${this.iconPath}/${iconName}.png`;
      } else if (iconName.includes('.png')) {
        return `${iconName}`
      }
      return `${this.iconPath}/poi.png`;
    },
    onHidePoiDrawer () {
      if (!this.$vuetify.breakpoint.mobile) {
        this.$root.$emit('closeInfoPopup');
        this.$emit('hide-poi-drawer');
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.image-button {
  position: absolute;
  bottom: 10px;
}
.left-bar-logo {
    width: auto;
    height: 40px;
    left: 10px;
    vertical-align: middle;
    display: block;
    margin: 5px auto;
  }
  .v-tab {
    font-size: .7rem;
  }
  .title-items {
    display: flex;
    align-items: center;
  }
  .gallery-thumb {
    cursor: pointer;
  }
  .panel-section-items{
    width: 410px;
    padding: 5px 20px 5px 20px;
    .v-list {
      .v-list-item {
        padding: 0
      }
    }
  }
  .list-label-value {
    .v-list-item {
      min-height: 24px;
      span:first-child {
        width: 110px;
      }
      span:nth-child(2) {
        margin-left: 10px;
      }
    }
  }
  .list-buttons {
    .v-list-item {
      min-height: 28px;
    }
  }

  .v-window-item {
    width: 100%;
  }
  #drawer-search{
    max-width:70vw;
    @media(max-width:767.98px){
      position:fixed;
      width:70vw;
      z-index:5;
      padding-top:0;
      margin-top:0 !important;
      top:10px;
    }
  }
</style>
