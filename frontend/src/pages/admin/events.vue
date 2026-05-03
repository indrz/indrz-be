<template>
  <div>
    <v-row>
      <v-col>
        <events-list />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import EventsList from '@/components/admin/events/EventsList'

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped>
</style>
