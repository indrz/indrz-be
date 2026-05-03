<template>
  <div>
    <poi-manager />
    <snack-bar />
  </div>
</template>

<script setup>
import PoiManager from '@/components/admin/poi/PoiManager'
import SnackBar from '@/components/SnackBar'

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped>
</style>
