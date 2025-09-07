<template>
  <v-card-title>
    <v-toolbar
      :max-width="toolbarWidth"
      dense
      rounded
      floating
    >
      <v-app-bar-nav-icon v-if="!isSmallScreen || !shouldShow" @click.stop="attachedDrawer = !attachedDrawer;" />
      <template v-if="isSmallScreen">
        <v-btn icon @click="shouldShow = !shouldShow">
          <v-icon v-if="!shouldShow">
            mdi-magnify
          </v-icon>
          <v-icon v-if="shouldShow">
            mdi-chevron-left
          </v-icon>
        </v-btn>
      </template>
      <v-expand-transition>
        <campus-search
          v-show="!isSmallScreen || shouldShow"
          ref="searchComp"
          :key="`search-comp-${updateKey}`"
          :selected="search"
          :drawer="true"
          :should-search="shouldSearch"
          @selectSearchResult="onSearchSelect"
          @showSearch="shouldShow = true"
          @clearClicked="onClearClick"
        />
      </v-expand-transition>
    </v-toolbar>
  </v-card-title>
</template>

<script>
import CampusSearch from '@/components/CampusSearch'
import MapHandler from '~/util/mapHandler';

export default {
  name: 'DrawerSearch',
  components: {
    CampusSearch
  },
  props: {
    drawer: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    map: {
      type: Object,
      required: true
    },
    selected: {
      type: Object
    }
  },
  data () {
    return {
      shouldShow: false,
      shouldSearch: true,
      search: this.selected,
      updateKey: 1
    };
  },
  mounted () {
    const temp = this.selected
    if (!temp.name) {
      temp.name = this.selected.room_code;
      this.search = temp
      this.updateKey++;
    }
  },
  computed: {
    isSmallScreen () {
      return this.$vuetify.breakpoint.smAndDown;
    },
    toolbarWidth () {
      return this.isSmallScreen ? '280px' : '320px';
    },
    attachedDrawer: {
      get: function () {
        return this.drawer;
      },
      set: function (newValue) {
        this.$emit('update:drawer', newValue);
      }
    },
    searchField () {
      return this.$refs.searchComp;
    }
  },
  watch: {
    selected (properties) {
      this.shouldSearch = false;
      const code = properties.room_code;
      const data = {
        ...properties,
        ...{
          floorNum: properties.floor_num,
          roomCode: properties.room_code,
          building: properties.building,
          src_icon: properties.src_icon || properties.icon,
          code,
          id: properties.id
        }
      };
      this.searchField.search = MapHandler.getTitle(data, this.$i18n.locale)
      this.updateKey++;
      setTimeout(() => {
        this.shouldSearch = true;
      }, 1000)
    }
  },
  methods: {
    onSearchSelect (selectedItem) {
      this.map.onSearchSelect(selectedItem);
    },
    onClearClick () {
      this.$emit('hide-poi-drawer')
    }
  }

};
</script>

<style scoped>

</style>
