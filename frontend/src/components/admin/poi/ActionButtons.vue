<template>
  <div class="speed-btn-panel">
    <v-speed-dial
      v-model="fab"
      :top="top"
      :bottom="bottom"
      :right="right"
      :left="left"
      :direction="direction"
      :open-on-hover="hover"
      :transition="transition"
    >
      <template v-slot:activator>
        <v-btn
          color="blue-darken-2"
          theme="dark"
          variant="fab"
        >
          <v-icon v-if="fab">
            mdi-close
          </v-icon>
          <v-icon v-else>
            mdi-map-marker
          </v-icon>
        </v-btn>
      </template>
      <v-btn
        aria-label="Edit POI"
        color="green"
        theme="dark"
        variant="fab"
        size="small"
        @click.stop.prevent="onEditPoiClick"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        aria-label="Add a new POI"
        color="indigo"
        theme="dark"
        variant="fab"
        size="small"
        @click.stop.prevent="onAddPoiClick"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-btn
        aria-label="Delete a POI"
        color="red"
        theme="dark"
        variant="fab"
        size="small"
        @click.stop.prevent="onDeletePoiClick"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>
  </div>
</template>

<script>
export default {
  name: 'ActionButtons',
  data: function () {
    return {
      direction: 'top',
      fab: false,
      fling: false,
      hover: false,
      tabs: null,
      top: false,
      right: true,
      bottom: true,
      left: false,
      transition: 'slide-y-reverse-transition'
    };
  },
  methods: {
    onAddPoiClick () {
      this.$emit('action', 'addPoiClick');
    },
    onEditPoiClick () {
      this.$emit('action', 'editPoiClick');
    },
    onDeletePoiClick () {
      this.$emit('action', 'deletePoiClick');
    }
  }
};
</script>

<style scoped>
  .speed-btn-panel {
    position: absolute;
    right: 45px !important;
    bottom: 100px !important;
  }
</style>
