<template>
  <div>
    <v-row>
      <v-col>
        <events-list />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import EventsList from '@/components/admin/events/EventsList';

export default {
  layout: 'admin',
  components: { EventsList
  },
  mounted () {

  },
  methods: {
  }
};
</script>

<style scoped>
</style>
