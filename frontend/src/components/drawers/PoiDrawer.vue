<template>
  <div ref="drawerEl">
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
      location="bottom"
      :style="{ width: isMobile ? '100%' : '410px', height: drawerHeight + 'px', top: 'auto', bottom: 0, position:'fixed' }"
      :scrim="false"
      app
      fixed
      :permanent="shouldShowDrawer"
      data-test="poiLeftPane"
    >
      <div v-if="isMobile" class="draggable-handle" @mousedown="startDrag" @touchstart="startDrag" />
      <div v-if="!poiImages">
        <v-card
          style="margin-top: 10px"
          elevation="0"
        >
          <v-row justify="center">
            <v-img
              class="poi-hero-image"
              width="100%"
              :height="isMobile ? 240 : 220"
              cover
              :src="heroImageSrc"
              :lazy-src="defaultPoiImage"
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
                    color="primary-lighten-1"
                  />
                </v-row>
              </template>

              <!-- Search is handled by the main navigation/left panel; avoid duplicating it inside the POI drawer. -->

              <div
                v-if="poiImageList.length"
                class="image-button"
              >
                <v-btn
                  class="ma-2 text-white"
                  color="rgba(0,0,0,0.4)"
                  variant="tonal"
                  @click="poiImages = true"
                >
                  <v-icon start>
                    mdi-folder-multiple-image
                  </v-icon>
                  {{ poiImageList.length }} - {{ locale.labelPoiPictures }}
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
              <v-tab v-for="(tabInfo, index) in tabs" :key="index" :value="index" @click="onTabClick(index)">
                {{ tabInfo.text }}
                <v-icon>{{ tabInfo.icon }}</v-icon>
              </v-tab>
            </v-tabs>
            <v-window v-model="activeTabIndex">
              <v-window-item :value="0">
                <div />
              </v-window-item>

              <v-window-item :value="1">
                <v-divider class="my-3 my-lg-3" />
                <div class="row justify-center">
                  <div class="panel-section-items">
                    <v-list>
                      <v-list-item>
                        <template #prepend>
                          <v-img
                            v-if="data.icon"
                            :max-width="20"
                            :src="data.icon"
                            alt="icon image"
                          />
                          <v-img
                            v-else-if="data.src_icon"
                            :src="getIconUrl(data.src_icon)"
                            contain
                            max-height="24"
                            max-width="24"
                            alt="icon image"
                          />
                        </template>
                        <v-list-item-title data-test="searchTitle" class="text-h6 text-primary" v-text="searchTitle" />
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
                            size="small"
                            variant="text"
                            color="wu"
                            class="pl-0"
                            :aria-label="button.label"
                            @click.stop="button.handler"
                          >
                          <v-icon start>
                            {{ button.icon }}
                          </v-icon>
                          {{ button.label }}
                        </v-btn>
                      </v-list-item>
                    </v-list>
                  </div>
                </div>
              </v-window-item>
              <v-window-item :value="2">
                <div />
              </v-window-item>
              <v-window-item :value="3">
                <div />
              </v-window-item>
            </v-window>
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
              <span class="text-primary text-subtitle-1">{{ data.name_en }}</span>
            </v-col>
          </v-row>
          <v-row v-for="(image, index) in poiImageList" :key="image.id || index" justify="center">
            <v-img
              :max-width="410"
              :aspect-ratio="2"
              :src="getImageSrc(image, { preferThumbnail: true })"
              :lazy-src="defaultPoiImage"
              class="gallery-thumb"
              style="margin: 5px;"
              alt="image for poi"
              @click="onGalleryImageClick(index)"
            />
          </v-row>
        </v-container>
      </div>
      <photo-gallery :show="showGallery" :images="poiImageList" :selcted-index="galleryImageIndex" @gallery:show="showGallery=$event" />
    </v-navigation-drawer>
  </div>

</template>

<script>
import config from '../../util/indrzConfig';
import PhotoGallery from '../PhotoGallery';
import BaseDrawer from './BaseDrawer';
import MapHandler from '@/util/mapHandler';
import bus from '~/util/bus';

const { env } = config;

export default {
  name: 'PoiDrawer',
  components: {
    PhotoGallery
  },
  mixins: [BaseDrawer],
  data () {
    return {
      updateKey: 1,
      poiImages: false,
      showGallery: false,
      galleryImageIndex: 0,
      tabs: [
        { icon: 'mdi-directions', text: 'Routing' },
        { icon: 'mdi-information', text: 'Info' },
        { icon: 'mdi-share', text: 'Share' },
        { icon: 'mdi-close', text: 'Close' }
      ],
      activeTabIndex: 1,
      iconNames: ['book', 'department', 'person', 'poi', 'space'],
      iconPath: '/images/icons/search/'
    };
  },
  computed: {
    currentLocale () {
      const raw = this.$i18n?.locale
      return raw && typeof raw === 'object' && 'value' in raw ? raw.value : raw
    },
    locale () {
      // Keep labels reactive when the active locale changes.
      return {
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
        labelExternalId: this.$t('label_external_id'),
        labelPoiPictures: this.$t('poi_pictures'),
        share_button_tip: this.$t('share_button_tip'),
        entranceButtonTip: this.$t('entrance_button_tip'),
        metroButtonTip: this.$t('metro_button_tip'),
        defiButtonTip: this.$t('defi_button_tip'),
        shareButtonTip: this.$t('share_button_tip'),
        label_wing_name: this.$t('label_wing_name')
      }
    },
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
    poiData () {
      const candidate = this.data
      if (candidate && typeof candidate === 'object' && candidate.properties && typeof candidate.properties === 'object') {
        return candidate.properties
      }
      return candidate || {}
    },
    poiImageList () {
      const images = this.poiData?.images
      return Array.isArray(images) ? images : []
    },
    heroImageSrc () {
      const firstImage = this.poiImageList.length ? this.poiImageList[0] : null
      return this.getImageSrc(firstImage)
    },
    searchTitle () {
      const { data } = this;
      return MapHandler.getTitle(data, this.currentLocale)
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
      handler () {
        this.poiImages = false;
        this.activeTabIndex = 1;
        this.updateKey++;
      }
    }
  },
  methods: {
    getMediaBaseUrl () {
      const envBase = this.baseUrl

      if (typeof window === 'undefined') {
        return envBase || ''
      }

      const origin = window.location?.origin || ''
      const hostname = window.location?.hostname || ''

      const isLocalHost = hostname === 'localhost' || hostname === '127.0.0.1'
      if (isLocalHost) {
        return origin
      }

      return envBase || origin
    },
    getImageSrc (image, { preferThumbnail = false } = {}) {
      if (!image) return `${this.defaultPoiImage}`

      const raw = preferThumbnail
        ? (image.thumbnail || image.image || image.url || image.src)
        : (image.image || image.url || image.src)

      if (!raw) return `${this.defaultPoiImage}`

      if (typeof raw === 'string' && (raw.startsWith('http://') || raw.startsWith('https://'))) {
        return raw
      }

      const base = this.getMediaBaseUrl()
      try {
        return new URL(String(raw), base).toString()
      } catch {
        const safeBase = String(base || '').replace(/\/+$/, '')
        const safeRaw = String(raw || '').startsWith('/') ? String(raw) : `/${raw}`
        return `${safeBase}${safeRaw}`
      }
    },
    onEntranceButtonClick () {
      bus.emit('popupRouteClick', 'from');
      bus.emit('popupEntranceButtonClick');
    },
    onMetroButtonClick () {
      bus.emit('popupRouteClick', 'from');
      bus.emit('popupMetroButtonClick');
    },
    onDefiButtonClick () {
      bus.emit('popupRouteClick', 'from');
      bus.emit('popupDefiButtonClick');
    },
    onShareButtonClick () {
      bus.emit('shareClick');
    },
    onRouteClick (path) {
      bus.emit('popupRouteClick', path);
    },
    onTabClick (index) {
      if (index === 2) {
        this.onShareButtonClick()
      } else if (index === 0) {
        this.onRouteClick('from')
        // this.$emit('open-route-drawer');
      } else if (index === 3) {
        bus.emit('closeInfoPopup');
        this.$emit('hide-poi-drawer')
      }
    },
    onGalleryImageClick (index = 0) {
      this.galleryImageIndex = index;
      this.showGallery = true;
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
    }
  }
};
</script>

<style lang="scss" scoped>
.poi-hero-image {
  display: block;
}

.image-button {
  position: absolute;
  bottom: 10px;
}
.left-bar-logo {
    width: auto;
    height: 40px;
    left: 10px;
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
