<template>
  <v-card
    id="floorList"
    :max-height="containerHeight"
    class="mx-auto floor-changer"
  >
    <v-list v-if="!isSmallScreen" dense>
      <v-list-item-group mandatory>
        <v-list-item
          v-for="(floor, i) in floors"
          :key="i"
          @click.stop="onFloorClick(floor, true)"
        >
          <v-list-item-content>
            <v-list-item-title v-text="floor.short_name" />
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <div v-else>
      <v-select
        v-model="selectedFloor"
        :items="floors"
        item-text="short_name"
        item-value="id"
        flat
        hide-details
        solo
        dense
        return-object
        @change="(selectedFloor) => {onFloorClick(selectedFloor, true)}"
      />
    </div>
  </v-card>
</template>

<script>
import { mapState } from 'vuex';
import config from '../util/indrzConfig';

const { env } = config;

export default {
  data () {
    return {
      selectedFloor: null,
      setSelection: null
    };
  },

  computed: {
    ...mapState({
      floors: state => state.floor.floors
    }),
    isSmallScreen () {
      return this.$vuetify.breakpoint.smAndDown;
    },
    containerHeight () {
      return this.isSmallScreen ? '100px' : '400px';
    }
  },

  watch: {
    isSmallScreen (isSmall) {
      if (this.selectedFloor) {
        this.selectFloorWithCss(this.selectedFloor.floor_num, false);
      }
    },
    floors () {
      if (this.setSelection) {
        this.selectFloorWithCss(this.setSelection);
      }
    }
  },

  mounted () {
    this.$bus.$on('searchResponse', this.handleSearchQuery)
  },

  methods: {
    handleSearchQuery (queryData) {
      const floorNum = queryData.features && queryData.features.length && queryData.features[0].properties ? queryData.features[0].properties.floor_num : queryData.type === 'Feature' ? queryData.properties.floor_num : process.env.DEFAULT_START_FLOOR;
      if (typeof floorNum === 'number' && !isNaN(floorNum)) {
        this.selectedFloor = floorNum
        this.selectFloorWithCss(floorNum)
      }
    },
    onFloorClick (floor, isEvent) {
      const floorNum = env.LAYER_NAME_PREFIX + floor.floor_num;
      this.$emit('floorClick', floorNum);
      this.selectFloorWithCss(floor.floor_num, isEvent);
    },
    selectFloorWithCss (floorNum, isEvent) {
      this.setSelectedFloor(floorNum);
      setTimeout(() => {
        if (!this.isSmallScreen) {
          this.selectOnListComponent(floorNum, isEvent);
        }
      }, 500);
    },
    selectOnListComponent (floorNum, isEvent) {
      const activeClass = 'v-list-item--active';
      const linkClass = 'v-list-item--link';
      const listItems = this.$el.querySelectorAll('.v-list-item');
      const floorNumToFind = Number(floorNum).toFixed(1);
      const floorIndex = this.floors.findIndex(floor => floor.floor_num.toFixed(1) === floorNumToFind);

      listItems.forEach((item) => {
        item.classList.remove(activeClass, linkClass);
      });
      if (listItems.length && floorIndex > -1) {
        listItems[floorIndex].classList.add(activeClass, linkClass);
        if (!isEvent) {
          const list = document.getElementById('floorList');
          list.scrollTo({ top: (40 * floorIndex), behavior: 'smooth' });
        }
      }
    },
    setSelectedFloor (floorNum) {
      const floorToSelect = this.floors.find(floor => floor.floor_num === floorNum);

      if (floorToSelect) {
        this.selectedFloor = floorToSelect;
      }
    },
    getFloorByFloorNum (floorNameWithPrefix) {
      const floorNum = env.LAYER_NAME_PREFIX ? floorNameWithPrefix.split(env.LAYER_NAME_PREFIX)[1] : floorNameWithPrefix;
      if (!floorNum) {
        return null;
      }
      const foundFloors = this.floors.filter(floor => floor.floor_num.toFixed(1) === Number(floorNum).toFixed(1));
      if (foundFloors && foundFloors.length) {
        return foundFloors[0];
      }
      return {};
    }
  }
};
</script>

<style scoped lang="scss">
  .floor-changer {
    position: absolute;
    right: 10px;
    top: 70px;
    overflow-y: auto;
    scrollbar-width: none;
    background-color: transparent;
    .v-list-item__title {
      text-align: center;
    }
    .v-list-item__content {
      min-width: 30px;
    }
    .v-select {
      max-width: 100px;
    }
  }
  .v-list-item--active{
    background-color: #0048ff;
  }
  .theme--dark.floor-changer {
    background-color: #1E1E1E;
  }
  @-moz-document url-prefix() {
    .floor-changer {
      scrollbar-width: thin;
    }
  }
</style>
