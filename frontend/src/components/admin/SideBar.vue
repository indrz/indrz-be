<template>
  <v-navigation-drawer
    v-model="drawerState"
    fixed
    app
    clipped
    data-test="sideBarAdmin"
  >
    <v-list dense>
      <v-list-item-group
        v-model="selectedMenuIndex"
        color="primary"
      >
        <template v-for="menuItem in menuItems">
          <v-list-item
            :key="menuItem.text"
            @click="onMenuItemClick(menuItem.route)"
          >
            <template v-slot:default="{}">
              <v-list-item-action>
                <v-icon>
                  mdi-{{ menuItem.icon }}
                </v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-text="menuItem.text" />
              </v-list-item-content>
            </template>
          </v-list-item>
        </template>
      </v-list-item-group>
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
