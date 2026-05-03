<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import OlMap from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import VectorTileLayer from 'ol/layer/VectorTile'
import XYZ from 'ol/source/XYZ'
import VectorTileSource from 'ol/source/VectorTile'
import MVT from 'ol/format/MVT'
import { Fill, Stroke, Style, Text as OlText } from 'ol/style'

const container = ref(null)
let map = null

// Runtime config (Nuxt safe access)
const runtime =
  typeof globalThis.useRuntimeConfig === 'function'
    ? globalThis.useRuntimeConfig()
    : {}

const GEOSERVER =
  runtime?.public?.GEOSERVER_URL ??
  runtime?.public?.geoserverUrl ??
  runtime?.public?.GEOSERVER ??
  runtime?.public?.geoserver

const LAYER = runtime?.public?.LAYER ?? runtime?.public?.layer

// Build WMTS template for MVT
function mvtUrlTemplate (geoserverBase, layerName) {
  const base = String(geoserverBase || '').replace(/\/+$/, '')
  if (!base || !layerName) { return '' }
  return `${base}/gwc/service/wmts?service=WMTS&request=GetTile&version=1.0.0&layer=${encodeURIComponent(
    layerName
  )}&style=&tilematrixset=EPSG:3857&TileMatrix=EPSG:3857:{z}&TileRow={y}&TileCol={x}&format=application%2Fvnd.mapbox-vector-tile`
}

// Simple style: fill + outline + optional label from a property
function featureStyle () {
  return new Style({
    fill: new Fill({ color: 'rgba(0, 153, 255, 0.15)' }),
    stroke: new Stroke({ color: '#0099ff', width: 1 }),
    text: new OlText({
      font: '12px Inter, system-ui, sans-serif',
      fill: new Fill({ color: '#111' }),
      stroke: new Stroke({ color: '#fff', width: 3 }),
      overflow: true
    })
  })
}

onMounted(() => {
  if (!container.value) { return }

  const osm = new TileLayer({
    source: new XYZ({
      url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      attributions: '© OpenStreetMap contributors'
    })
  })

  const layers = [osm]

  if (GEOSERVER && LAYER) {
    const url = mvtUrlTemplate(GEOSERVER, LAYER)
    if (url) {
      const vectorTiles = new VectorTileLayer({
        source: new VectorTileSource({
          url,
          format: new MVT(),
          maxZoom: 22
        }),
        style: (feature, resolution) => {
          const s = featureStyle()
          const name = feature.get('name') || feature.get('label') || ''
          const t = s.getText()
          if (t) { t.setText(name && resolution < 10 ? String(name) : '') }
          return s
        },
        declutter: true
      })
      layers.push(vectorTiles)
    }
  }

  map = new OlMap({
    target: container.value,
    layers,
    view: new View({
      projection: 'EPSG:3857',
      center: [1589723, 5879830],
      zoom: 12,
      minZoom: 2,
      maxZoom: 22
    })
  })
})

onBeforeUnmount(() => {
  if (map) {
    map.setTarget(undefined)
    map = null
  }
})
</script>

<template>
  <div ref="container" class="map-root" />
</template>

<style scoped>
.map-root {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
