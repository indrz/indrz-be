<template>
  <v-container class="bg-grey-lighten-5">
    <v-row no-gutters>
      <v-col
        cols="6"
        md="4"
      >
        <ZoneplanLayerPanel @layer-toggled="handleLayerToggle" @layer-mainuse-toggled="handleMainUseLayerToggle" />
      </v-col>
      <v-col
        cols="6"
        sm="6"
        md="8"
      >
        <BaseMap ref="baseMap" />
        <FloorChanger class="custom-floor-changer" @floor-selected="onFloorSelected" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import ZoneplanLayerPanel from '@/components/admin/zoneplans/ZoneplanLayerPanel'
import BaseMap from '@/components/BaseMap'
import FloorChanger from '@/components/admin/zoneplans/FloorChanger'
import { fetchOrgcodeData, fetchMainUseData } from '@/util/adminApi'

definePageMeta({
  layout: 'admin'
})

const baseMap = ref(null)
const activeLayers = ref([])
const currentFloorNum = ref(0.0)

async function handleLayerToggle (layerInfo) {
  const baseMapComponent = baseMap.value
  if (layerInfo.active) {
    try {
      activeLayers.value.push(layerInfo)
      const layerData = await fetchOrgcodeData(layerInfo.orgcode, currentFloorNum.value)
      if (layerData) {
        baseMapComponent.addLayer(layerInfo.name, layerInfo.color, layerData)
      } else {
        console.log('No features found for layer:', layerInfo.name)
      }
    } catch (error) {
      console.error('Error fetching GeoJSON:', error)
    }
  } else {
    baseMapComponent.removeLayer(layerInfo.name)
    activeLayers.value = activeLayers.value.filter(layer => layer.name !== layerInfo.name)
  }
}

async function handleMainUseLayerToggle (layerInfo) {
  const baseMapComponent = baseMap.value
  if (layerInfo.active) {
    try {
      activeLayers.value.push(layerInfo)
      const layerData = await fetchMainUseData(layerInfo.name, currentFloorNum.value)
      if (layerData) {
        baseMapComponent.addLayer(layerInfo.name, layerInfo.color, layerData)
      } else {
        console.log('No features found for layer:', layerInfo.name)
      }
    } catch (error) {
      console.error('Error fetching GeoJSON:', error)
    }
  } else {
    baseMapComponent.removeLayer(layerInfo.name)
    activeLayers.value = activeLayers.value.filter(layer => layer.name !== layerInfo.name)
  }
}

async function refreshLayers (fetchData, getParam) {
  const baseMapComponent = baseMap.value
  activeLayers.value.forEach(layer => baseMapComponent.removeLayer(layer.name))

  for (const layerInfo of activeLayers.value) {
    try {
      const param = getParam(layerInfo)
      const layerData = await fetchData(param, currentFloorNum.value)
      if (layerData) {
        baseMapComponent.addLayer(layerInfo.name, layerInfo.color, layerData)
      } else {
        console.log('No features found for layer:', layerInfo.name)
      }
    } catch (error) {
      console.error('Error refreshing layer:', layerInfo.name, error)
    }
  }
}

function onFloorSelected (floorNum) {
  currentFloorNum.value = floorNum
  refreshLayers(fetchOrgcodeData, layerInfo => layerInfo.orgcode)
  refreshLayers(fetchMainUseData, layerInfo => layerInfo.name)
}
</script>
<style scoped>
</style>
