<template>
  <div id="indrz-popup" :style="{'min-width': popupSize.width}" scrollable title="indrz info" class="ol-popup indrz-popup">
    <img  src="/images/selected-large.png" alt="Selected POI" />
  </div>

</template>

<script>
export default {
  name: 'InfoOverlay',
  data () {
    return {
      locale: {
        entranceButtonText: this.$t('entrance_button_text'),
        entranceButtonTip: this.$t('entrance_button_tip'),
        metroButtonText: this.$t('metro_button_text'),
        metroButtonTip: this.$t('metro_button_tip'),
        defiButtonTip: this.$t('defi_button_tip'),
        shareButtonTip: this.$t('share_button_tip'),
        routeFromHereText: this.$t('route_from_here'),
        routeToHereText: this.$t('route_to_here')
      }
    }
  },
  computed: {
    popupSize () {
      const size = {
        width: '354px',
        height: '366px'
      };

      switch (this.$vuetify.breakpoint.name) {
        case 'xs':
          size.width = '150px';
          size.height = '162px';
          break;
        case 'sm':
          size.width = '270px';
          size.height = '282px';
          break;
      }
      return size;
    },
    multiRowButton () {
      return !!this.$vuetify.breakpoint.smAndDown;
    }
  },
  methods: {
    onPopupCloseClick () {
      this.$emit('closeClick');
    },
    onShareButtonClick () {
      this.$emit('shareClick');
    },
    onRouteClick (path) {
      this.$emit('popupRouteClick', path);
    },
    onEntranceButtonClick () {
      this.$emit('popupRouteClick', 'from');
      this.$emit('popupEntranceButtonClick');
    },
    onMetroButtonClick () {
      this.$emit('popupRouteClick', 'from');
      this.$emit('popupMetroButtonClick');
    },
    onDefiButtonClick () {
      this.$emit('popupRouteClick', 'from');
      this.$emit('popupDefiButtonClick');
    }
  }
};
</script>

<style scoped>
  .xs-popup {
    display: flex;
    flex-direction: column;
    align-items: flex-start !important;
  }
  #indrz-popup{
    position: absolute;
    bottom: 0;
    left: -20px;
    z-index: 1;
  }
</style>
