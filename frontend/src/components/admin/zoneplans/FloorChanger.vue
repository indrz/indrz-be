<template>
  <v-list id="floor-list" dense class="floor-changer-list">
    <v-list-item
      v-for="floor in floors"
      :key="floor.id"
      :class="{ 'floor-item-selected': floor.floor_num === currentFloorNum }"
      @click="selectFloor(floor.floor_num)"
    >
      <v-list-item-content>
        <v-list-item-title>{{ floor.short_name }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>
<script>
import config from '@/util/indrzConfig'
import { fetchFloors } from '@/util/adminApi'

const { env } = config;

export default {
  name: 'FloorChanger',
  data () {
    return {
      floors: [],
      currentFloorNum: env.DEFAULT_START_FLOOR
    };
  },
  created () {
    this.fetchFloorsWrapper();
  },
  methods: {
    async fetchFloorsWrapper () {
      // fetch floors
      try {
        const floors = await fetchFloors();
        this.floors = floors;
        // after floors are fetch & assigned, select default floor with scroll to function
        this.$nextTick(() => { this.selectDefaultFloor(); })
      } catch (error) {
        // Handle error appropriately
      }
    },
    selectFloor (floorNum) {
      // Existing method to select a floor
      this.currentFloorNum = floorNum;
      this.$emit('floor-selected', floorNum);
    },
    selectDefaultFloor () {
      const defaultFloor = env.DEFAULT_START_FLOOR
      const list = document.getElementById('floor-list');
      if (this.floors) {
        // Find Default Floor
        const floorIndex = this.floors.findIndex(floor => floor.floor_num === defaultFloor)
        // Scroll To Default Floor On Page Load
        list.scrollTo({ top: (35 * floorIndex), behavior: 'smooth' });
        this.selectFloor(defaultFloor);
      }
    }
  }
};
</script>

<style>
.floor-changer-list {
  position: absolute;
  top: 30px;
  right: 20px;
  width: 100px;
  max-height: 300px;
  overflow-y: auto; /* Enables vertical scrolling */
  scrollbar-width: thin;
}
.floor-item-selected {
  background-color: #456e8d; /* or any other color to indicate selection */
}
</style>
