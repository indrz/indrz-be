<template>
  <!-- OpenLayers Overlay anchor only (UI is rendered in the LeftPanel) -->
  <div
    id="indrz-popup"
    class="ol-popup indrz-popup"
    aria-hidden="true"
  />
</template>

<script>
export default {
  name: 'InfoOverlay',
  props: {
    // kept for backwards compatibility; not rendered here
    model: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
#indrz-popup{
  position: absolute;
  bottom: 0;
  left: -20px;
  z-index: 6;
}
</style>
