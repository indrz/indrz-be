<template>
  <v-dialog :model-value="show" fullscreen transition="dialog-bottom-transition">
    <v-card v-if="show" class="ma-2">
      <v-card-text class="pa-0">
        <shelf-map ref="shelfMap" @floorChange="onFloorChange" />
        <floor-changer
          ref="floorChanger"
          @floorClick="onFloorClick"
        />
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <div class="text-h6">
          {{ title }}
        </div>
        <v-spacer />
        <v-btn :disabled="loading" @click="close" color="blue-darken-1" variant="text">
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading"
          :loading="loading"
          @click="save"
          color="blue-darken-1"
          variant="text"
        >
          <v-icon start>
            mdi-content-save
          </v-icon>
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import FloorChanger from '@/components/FloorChanger';
import ShelfMap from '@/components/admin/shelves/ShelfMap';
import MapUtil from '@/util/map';
import config from '@/util/indrzConfig';
import { useFloorStore } from '~/stores/floor';
import { useShelfStore } from '~/stores/shelf';
const { env } = config;

export default {
  name: 'DrawShelf',
  components: { ShelfMap, FloorChanger },
  props: {
    title: {
      type: String,
      default: function () {
        return '';
      }
    },
    show: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    currentShelf: {
      type: Object,
      default: function () {
        return {};
      }
    }
  },
  data () {
    return {
      loading: false,
      activeFloorNum: null
    }
  },
  computed: {
    floors () {
      const floorStore = useFloorStore();
      return typeof floorStore.floors === 'function' ? floorStore.floors() : floorStore.$state.floors;
    },
    selectedShelf () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelf;
    }
  },
  watch: {
    show (value) {
      if (value && this.selectedShelf?.building_floor) {
        this.$nextTick(() => {
          const floor = this.floors.find(floor => floor.id === this.selectedShelf.building_floor);
          if (floor) {
            this.$refs.floorChanger.onFloorClick(floor, false);
          }
        });
      }
    }
  },
  methods: {
    saveShelf (payload) {
      const shelfStore = useShelfStore();
      return shelfStore.SAVE_SHELF(payload);
    },
    onFloorChange ({ floor }) {
      if (floor) {
        this.$refs.floorChanger.onFloorClick(floor, false);
      }
    },
    onFloorClick (floorNum) {
      this.activeFloorNum = floorNum;
      const { map, layers } = this.$refs.shelfMap;
      MapUtil.activateLayer(this.activeFloorNum, layers.switchableLayers, map);
    },
    close () {
      this.$emit('close');
    },
    save () {
      const shelf = this.$refs.shelfMap.shelf;

      if (shelf && shelf.getGeometry().getCoordinates()) {
        const floorNum = Number.parseInt(this.activeFloorNum.split(env.LAYER_NAME_PREFIX)[1], 10);
        const floor = this.$refs.floorChanger.floors.find(floor => floor.floor_num === floorNum);

        this.$emit('save', {
          coordinates: shelf.getGeometry().getCoordinates(),
          floor: floor
        });
      }

      this.close();
    }
  }
}
</script>

<style scoped>
</style>
