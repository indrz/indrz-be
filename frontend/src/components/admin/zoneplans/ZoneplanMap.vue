<template>
  <BaseMap />
</template>

<script>
import config from '~/util/indrzConfig';
import BaseMap from '~/components/BaseMap.vue';

const { env } = config;

export default {
  name: 'ZoneplanMap',
  components: {
    BaseMap
  },
  data () {
    return {
      map: null,
      center: env.DEFAULT_CENTER_XY, // Adjust center as needed
      zoom: 18
    };
  },
  mounted () {},
  methods: {}
};
</script>

<style>
#map {
  width: 100%;
  height: 500px;
}
#info {
  z-index: 1;
  opacity: 0;
  position: absolute;
  bottom: 0;
  left: 0;
  margin: 0;
  background: rgba(0, 60, 136, 0.7);
  color: white;
  border: 0;
  transition: opacity 100ms ease-in;
}
</style>
