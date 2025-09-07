<template>
  <div>
    <poi-manager />
    <snack-bar />
  </div>
</template>

<script>
import PoiManager from '@/components/admin/poi/PoiManager';
import SnackBar from '@/components/SnackBar';
export default {
  layout: 'admin',
  components: {
    PoiManager,
    SnackBar
  }
};
</script>

<style scoped>
</style>
