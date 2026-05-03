<template>
  <div>
    <h1>POI Category Editor</h1>
    <poi-category-list />
    <snack-bar />
  </div>
</template>

<script setup>
import PoiCategoryList from '@/components/admin/poi/category/List'
import SnackBar from '@/components/SnackBar'

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped>

</style>
