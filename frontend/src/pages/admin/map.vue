<template>
  <div style="height:100vh;">
    <OlVectorTileMap />
  </div>
</template>

<script setup lang="ts">
import OlVectorTileMap from '~/components/map/OlVectorTileMap.client.vue'

definePageMeta({
  layout: 'admin'
})
</script>
