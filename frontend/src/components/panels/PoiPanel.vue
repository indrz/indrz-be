<template>
  <div class="poi-panel">
    <v-container class="pa-0" style="max-width: 410px">
      <div v-if="isEmptyPayload" class="pa-4 text-body-2">
        {{ $t('no_result_found') }}
      </div>
    

      <template v-else>
        <v-img
          class="poi-hero-image"
          width="100%"
          :height="isMobile ? 240 : 220"
          cover
          :src="heroImageSrc"
          :lazy-src="defaultPoiImage"
          alt="image of poi"
        >
          <div v-if="poiImages.length" class="image-button">
            <v-btn
              class="ma-2 text-white"
              color="rgba(0,0,0,0.4)"
              variant="tonal"
              @click="showThumbnails = !showThumbnails"
            >
              <v-icon start>
                mdi-folder-multiple-image
              </v-icon>
              {{ poiImages.length }} - {{ $t('poi_pictures') }}
            </v-btn>
          </div>
        </v-img>

        <div v-if="showThumbnails && poiImages.length" class="pa-2">
          <v-row dense>
            <v-col
              v-for="(image, index) in poiImages"
              :key="image.id || index"
              cols="4"
              class="pa-1"
            >
              <v-img
                class="gallery-thumb"
                height="90"
                cover
                :src="getImageSrc(image, { preferThumbnail: true })"
                :lazy-src="defaultPoiImage"
                alt="poi image thumbnail"
                @click="onGalleryImageClick(index)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Title and info section -->
        <div class="pa-4">
          <div class="text-h6 text-primary" data-test="poiTitle">{{ title }}</div>

          <v-list v-if="attributeRows.length" class="list-label-value mt-2">
            <v-list-item v-for="(row, idx) in attributeRows" :key="idx">
              <span>{{ row.label }}</span>
              <span>{{ row.value }}</span>
            </v-list-item>
          </v-list>
        </div>

        <v-divider />

        <!-- Primary actions -->
        <div class="pa-4">
          <div class="d-flex ga-2 mb-3">
            <v-btn color="primary" variant="tonal" @click="$emit('openRoute')">
              <v-icon start>mdi-directions</v-icon>
              {{ $t('directions') }}
            </v-btn>
            <v-btn variant="outlined" @click="onShare">
              <v-icon start>mdi-share</v-icon>
              {{ $t('share') }}
            </v-btn>
          </div>

          <v-divider class="mb-3" />

          <!-- Routing options -->
          <v-list class="list-buttons pa-0" density="compact">
            <v-list-item @click.stop="$emit('routeFrom', poiData)">
              <template #prepend><v-icon color="primary">mdi-map-marker</v-icon></template>
              {{ $t('route_from_here') }}
            </v-list-item>
            <v-list-item @click.stop="$emit('routeTo', poiData)">
              <template #prepend><v-icon color="primary">mdi-map-marker</v-icon></template>
              {{ $t('route_to_here') }}
            </v-list-item>
            <v-list-item @click.stop="onEntranceButtonClick">
              <template #prepend><v-icon color="primary">mdi-routes</v-icon></template>
              {{ $t('entrance_button_text') }}
            </v-list-item>
            <v-list-item @click.stop="onMetroButtonClick">
              <template #prepend><v-icon color="primary">mdi-routes</v-icon></template>
              {{ $t('metro_button_text') }}
            </v-list-item>
            <v-list-item @click.stop="onDefiButtonClick">
              <template #prepend><v-icon color="primary">mdi-heart-flash</v-icon></template>
              {{ $t('defi_button_tip') }}
            </v-list-item>
          </v-list>
        </div>

        <photo-gallery
          :show="showGallery"
          :images="poiImages"
          :selcted-index="galleryImageIndex"
          @gallery:show="showGallery = $event"
        />
      </template>
    </v-container>
  </div>
</template>

<script>
import MapHandler from '@/util/mapHandler';
import config from '@/util/indrzConfig';
import PhotoGallery from '@/components/PhotoGallery';
import bus from '~/util/bus';

const { env } = config;

export default {
  name: 'PoiPanel',
  components: { PhotoGallery },
  props: {
    data: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['close', 'openRoute', 'routeFrom', 'routeTo'],
  data () {
    return {
      showThumbnails: false,
      showGallery: false,
      galleryImageIndex: 0
    }
  },
  computed: {
    isEmptyPayload () {
      const payload = this.poiData
      return !payload || typeof payload !== 'object' || Object.keys(payload).length === 0
    },
    isMobile () {
      if (typeof window === 'undefined') return false
      return window.innerWidth <= 768
    },
    poiData () {
      // Sometimes we receive a GeoJSON Feature { properties: {...} }.
      // Sometimes we receive an OpenLayers Feature instance (no enumerable keys).
      // Normalize so the UI works for both shapes.
      const candidate = this.data

      // OpenLayers Feature: prefer getProperties() (includes geometry, id, etc)
      if (candidate && typeof candidate === 'object' && typeof candidate.getProperties === 'function') {
        const props = candidate.getProperties()
        if (props && typeof props === 'object') return props
      }

      // OpenLayers Feature internal storage (fallback; not ideal but works if getProperties isn't present)
      if (candidate && typeof candidate === 'object' && candidate.values_ && typeof candidate.values_ === 'object') {
        return candidate.values_
      }

      // Most common
      if (candidate && typeof candidate === 'object' && candidate.properties && typeof candidate.properties === 'object') {
        return candidate.properties
      }

      // Sometimes wrapped (e.g. { data: { properties: ... } } or { feature: { properties: ... } })
      const nestedProps = candidate?.data?.properties || candidate?.feature?.properties
      if (nestedProps && typeof nestedProps === 'object') {
        return nestedProps
      }

      return candidate || {}
    },
    poiImages () {
      const images = this.poiData?.images
      return Array.isArray(images) ? images : []
    },
    title () {
      try {
        const rawLocale = this.$i18n?.locale;
        const locale = rawLocale && typeof rawLocale === 'object' && 'value' in rawLocale
          ? rawLocale.value
          : rawLocale;
        return MapHandler.getTitle(this.poiData || {}, locale) || this.poiData?.name || '';
      } catch (e) {
        return this.poiData?.name || '';
      }
    },
    baseUrl () {
      return env.BASE_URL
    },
    defaultPoiImage () {
      return env.DEFAULT_POI_IMAGE
    },
    heroImageSrc () {
      const firstImage = this.poiImages.length ? this.poiImages[0] : null
      return this.getImageSrc(firstImage)
    },
    attributeRows () {
      const rows = []

      const roomCode = this.poiData?.room_code || this.poiData?.roomcode
      const floor = this.poiData?.floor_name || (this.poiData?.floor_num !== undefined && this.poiData?.floor_num !== null ? String(this.poiData.floor_num) : null)
      const wing = this.poiData?.wing
      const capacity = this.poiData?.capacity

      if (roomCode) rows.push({ label: this.$t('label_room_code'), value: roomCode })
      if (floor) rows.push({ label: this.$t('label_floor_name'), value: floor })
      if (wing) rows.push({ label: this.$t('label_wing_name'), value: wing })
      if (capacity) rows.push({ label: this.$t('label_capacity'), value: capacity })

      return rows
    }
  },
  watch: {
    data: {
      handler () {
        this.showThumbnails = false
        this.showGallery = false
        this.galleryImageIndex = 0

        this.debugLogPoiPayload('data changed')
      },
      immediate: true
    }
  },
  methods: {
    isPoiImageDebugEnabled () {
      if (typeof window === 'undefined') return false

      // Enable by setting in DevTools console:
      //   localStorage.setItem('debugPoiImages', '1')
      // Disable:
      //   localStorage.removeItem('debugPoiImages')
      try {
        return window.localStorage?.getItem('debugPoiImages') === '1'
      } catch {
        return false
      }
    },
    debugLogPoiPayload (reason) {
      if (!this.isPoiImageDebugEnabled()) return

      const raw = this.data
      const normalized = this.poiData
      const images = this.poiImages

      // Keep logs compact but actionable.
      // eslint-disable-next-line no-console
      console.log('[PoiPanel images]', reason, {
        rawKeys: raw && typeof raw === 'object' ? Object.keys(raw) : typeof raw,
        normalizedKeys: normalized && typeof normalized === 'object' ? Object.keys(normalized) : typeof normalized,
        poiId: normalized?.id || normalized?.poiId || normalized?.external_id,
        name: normalized?.name || normalized?.name_en || normalized?.room_code,
        imagesCount: images.length,
        firstImageRaw: images[0]?.image || images[0]?.url || images[0]?.src,
        baseUrl: this.baseUrl,
        mediaBaseUrl: this.getMediaBaseUrl(),
        heroImageSrc: this.heroImageSrc
      })

      if (images.length) {
        // eslint-disable-next-line no-console
        console.log('[PoiPanel images] computed image srcs', images.map((img) => this.getImageSrc(img)))
      }
    },
    getMediaBaseUrl () {
      const envBase = this.baseUrl

      if (typeof window === 'undefined') {
        return envBase || ''
      }

      const origin = window.location?.origin || ''
      const hostname = window.location?.hostname || ''

      // Local dev should default to the local origin even if env.BASE_URL is set to production.
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
        // Handles leading/trailing slashes correctly.
        return new URL(String(raw), base).toString()
      } catch {
        const safeBase = String(base || '').replace(/\/+$/, '')
        const safeRaw = String(raw || '').startsWith('/') ? String(raw) : `/${raw}`
        return `${safeBase}${safeRaw}`
      }
    },
    onShare () {
      bus.emit('shareClick')
    },
    onEntranceButtonClick () {
      bus.emit('popupRouteClick', 'from')
      bus.emit('popupEntranceButtonClick')
    },
    onMetroButtonClick () {
      bus.emit('popupRouteClick', 'from')
      bus.emit('popupMetroButtonClick')
    },
    onDefiButtonClick () {
      bus.emit('popupRouteClick', 'from')
      bus.emit('popupDefiButtonClick')
    },
    onGalleryImageClick (index = 0) {
      this.galleryImageIndex = index
      this.showGallery = true

      this.debugLogPoiPayload(`open gallery index=${index}`)
    }
  }
};
</script>

<style scoped>
.poi-hero-image {
  display: block;
}

.image-button {
  position: absolute;
  bottom: 10px;
}

.gallery-thumb {
  cursor: pointer;
}

.list-label-value .v-list-item {
  min-height: 24px;
}
.list-label-value .v-list-item span:first-child {
  width: 110px;
}
.list-label-value .v-list-item span:nth-child(2) {
  margin-left: 10px;
}
.list-buttons .v-list-item {
  min-height: 28px;
}
</style>
