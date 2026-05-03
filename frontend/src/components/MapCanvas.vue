<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import 'ol/ol.css'
import Map from 'ol/Map'
import View from 'ol/View'
import { Tile as TileLayer } from 'ol/layer'
import { OSM, TileWMS } from 'ol/source'

const props = defineProps({
  /** Initial center in EPSG:3857 */
  center: {
    type: Array,
    default: () => [1587876, 5879512]
  },
  /** Initial zoom */
  zoom: {
    type: Number,
    default: 18
  },
  /** If true, show the WMS floor overlay on top of OSM */
  showWms: {
    type: Boolean,
    default: true
  },
  /** Floor level number, e.g. 0, 1, -1.5 */
  selectedFloorLevel: {
    type: Number,
    default: 0
  },
  /** If true, fill the viewport height (100vh). */
  fullHeight: {
    type: Boolean,
    default: false
  }
})

const mapElement = ref(null)
let map = null
let wmsLayer = null

const WMS_BASE_URL = 'https://campusplan.aau.at/geoserver/wms'

function getWmsLayerName (floorLevel) {
  const level = Number(floorLevel)
  const safeLevel = Number.isFinite(level) ? level : 0
  const floorStr = safeLevel.toFixed(1).replace('.', '_')
  return `indrz:floor_${floorStr}`
}

function ensureWmsLayer () {
  if (!props.showWms) {
    if (wmsLayer && map) {
      map.removeLayer(wmsLayer)
    }
    wmsLayer = null
    return
  }

  if (!map) return

  if (!wmsLayer) {
    const wmsSource = new TileWMS({
      url: WMS_BASE_URL,
      params: {
        LAYERS: getWmsLayerName(props.selectedFloorLevel),
        TILED: true,
        FORMAT: 'image/png',
        TRANSPARENT: true,
        VERSION: '1.3.0'
      },
      serverType: 'geoserver',
      crossOrigin: 'anonymous'
    })

    wmsLayer = new TileLayer({
      source: wmsSource,
      zIndex: 1,
      opacity: 1
    })
    map.addLayer(wmsLayer)
  }

  // Update to the selected floor
  const source = wmsLayer.getSource()
  source && source.updateParams({
    LAYERS: getWmsLayerName(props.selectedFloorLevel)
  })
}

function buildMap () {
  if (!mapElement.value) return

  // Cleanup existing map if it exists (for HMR)
  if (map) {
    map.setTarget(undefined)
    map = null
    wmsLayer = null
  }

  map = new Map({
    target: mapElement.value,
    layers: [
      new TileLayer({
        source: new OSM(),
        zIndex: 0
      })
    ],
    view: new View({
      projection: 'EPSG:3857',
      center: props.center,
      zoom: props.zoom,
      minZoom: 2,
      maxZoom: 25
    }),
    controls: []
  })

  ensureWmsLayer()

  // Ensure correct initial render size.
  setTimeout(() => {
    map?.updateSize()
  }, 0)
}

onMounted(() => {
  buildMap()

  const onResize = () => map?.updateSize()
  window.addEventListener('resize', onResize)

  onUnmounted(() => {
    window.removeEventListener('resize', onResize)

    if (map) {
      map.setTarget(undefined)
      map = null
      wmsLayer = null
    }
  })
})

watch(() => props.selectedFloorLevel, () => {
  ensureWmsLayer()
})

watch(() => props.showWms, () => {
  ensureWmsLayer()
})
</script>

<template>
  <div class="map-canvas" :class="{ 'map-canvas--full': fullHeight }">
    <div ref="mapElement" class="map-canvas__inner" />
  </div>
</template>

<style scoped>
.map-canvas {
  width: 100%;
  height: 100%;
}

.map-canvas--full {
  height: 100vh;
}

.map-canvas__inner {
  width: 100%;
  height: 100%;
}
</style>
