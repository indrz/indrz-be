<template>
  <div>
    <h1>POI Category Editor</h1>
    <poi-category-list />
    <snack-bar />
  </div>
</template>

<script>
import PoiCategoryList from '@/components/admin/poi/category/List';
import SnackBar from '@/components/SnackBar';
export default {
  name: 'PoiCategory',
  components: { PoiCategoryList, SnackBar },
  layout: 'admin'
}
</script>

<style scoped>

</style>
