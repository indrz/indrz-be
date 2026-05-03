<template>
  <v-navigation-drawer
    v-model="drawerState"
    app
    location="left"
    data-test="sideBarAdmin"
  >
    <v-list density="compact">
      <template v-for="(menuItem, index) in menuItems" :key="menuItem.text">
        <v-list-item
          @click="onMenuItemClick(menuItem.route)"
          :class="{ 'v-list-item--active': selectedMenuIndex === index }"
        >
          <template #prepend>
            <v-icon>
              mdi-{{ menuItem.icon }}
            </v-icon>
          </template>
          <v-list-item-title v-text="menuItem.text" />
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'SideBar',
  components: {
  },
  props: {
    drawer: {
      type: Boolean,
      default: false
    },
    menuItems: {
      type: Array,
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      selectedMenuIndex: 0
    }
  },
  computed: {
    drawerState: {
      get () {
        return this.drawer;
      },
      set (value) {
        this.$emit('drawerClick', value);
      }
    },
    showPoi () {
      return this.$route.name === 'admin-poi';
    }
  },
  watch: {
    '$route' (to) {
      const matchedMenuIndex = this
        .menuItems
        .findIndex(menuItem => menuItem.route.name && to.name.includes(menuItem.route.name));
      if (matchedMenuIndex === -1) {
        this.selectedMenuIndex = 0;
      } else {
        this.selectedMenuIndex = matchedMenuIndex;
      }
    }
  },
  methods: {
    onMenuItemClick (route) {
      if (route && route.path && route.path !== this.$route.path) {
        this.$router.push(route.path);
      }
    }
  }
};
</script>

<style scoped>

</style>
