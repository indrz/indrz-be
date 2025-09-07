<template>
  <div>
    <v-row>
      <v-col>
        <book-shelf-list />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <shelf-data-list />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import BookShelfList from '@/components/admin/shelves/BookShelfList';
import ShelfDataList from '@/components/admin/shelves/ShelfDataList';
export default {
  layout: 'admin',
  components: {
    ShelfDataList,
    BookShelfList
  },
  mounted () {
    Promise.all([
      this.loadFloors(),
      this.loadBuildings()
    ])
  },
  methods: {
    ...mapActions({
      loadFloors: 'floor/LOAD_FLOORS',
      loadBuildings: 'building/LOAD_BUILDINGS'
    })
  }
};
</script>

<style scoped>
</style>
