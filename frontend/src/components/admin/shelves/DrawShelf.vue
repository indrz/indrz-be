<template>
  <v-dialog :value="show" fullscreen transition="dialog-bottom-transition">
    <v-card v-if="show" class="ma-2">
      <!--<v-toolbar
        dense
        flat
      >
        <div class="headline">
          {{ title }}
        </div>
        <v-spacer />
        <v-btn @click="close" icon>
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </v-toolbar>-->
      <v-card-text class="pa-0">
        <template>
          <shelf-map ref="shelfMap" @floorChange="onFloorChange" />
          <floor-changer
            ref="floorChanger"
            @floorClick="onFloorClick"
          />
        </template>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <div class="headline">
          {{ title }}
        </div>
        <v-spacer />
        <v-btn :disabled="loading" @click="close" color="blue darken-1" text>
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading"
          :loading="loading"
          @click="save"
          color="blue darken-1"
          text
        >
          <v-icon left>
            mdi-content-save
          </v-icon>
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import FloorChanger from '@/components/FloorChanger';
import ShelfMap from '@/components/admin/shelves/ShelfMap';
import MapUtil from '@/util/map';
import config from '@/util/indrzConfig';
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
    ...mapState({
      floors: state => state.floor.floors,
      selectedShelf: state => state.shelf.selectedShelf
    })
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
    ...mapActions({
      saveShelf: 'shelf/SAVE_SHELF'
    }),
    onFloorChange ({ floor }) {
      this.$refs.floorChanger.onFloorClick(floor, false);
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
