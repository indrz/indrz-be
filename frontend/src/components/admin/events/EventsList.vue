<template>
  <div>
    <H1>BETA EVENTS MOCKUP</H1>
    <v-data-table
      :headers="headers"
      :items="indrzEvents"
      class="elevation-1"
    >
      <template v-slot:[`item.enabled`]="{ item }">
        <v-checkbox-btn
          v-model="item.raw.enabled"
          disabled
        />
      </template>
    </v-data-table>
  </div>
</template>

<script>

export default {
  name: 'EventList',
  data () {
    return {
      indrzEvents: [
        {
          name: 'SuperEvent',
          startDate: '01.09.2021',
          endDate: '01.09.2021',
          roomCode: 'EA01897, EA02456, EA0189, EA02456, EA0189, EA02456, EA0189, EA02456, EA0189, EA02456, EA0189, EA02456, EA0189, EA02456, EA0189',
          otherAreas: 'geom',
          enabled: true
        },
        {
          name: 'Opening Green Room',
          startDate: '12.08.2021',
          endDate: '01.09.2021',
          roomCode: 'EA02456, EA02455',
          otherAreas: 'geom',
          enabled: false
        },
        {
          name: 'Hackathon',
          startDate: '10.08.2021',
          endDate: '01.09.2021',
          roomCode: 'EA02456',
          otherAreas: 'geom',
          enabled: false
        },
        {
          name: 'Innovation day',
          startDate: '07.07.2021',
          endDate: '01.09.2021',
          roomCode: 'EA02456',
          otherAreas: 'geom',
          enabled: false
        }

      ],
      headers: [
        { title: 'Name', key: 'name' },
        { title: 'Start Date', key: 'startDate' },
        { title: 'End Date', key: 'endDate' },
        { title: 'Room Code(s)', key: 'roomCode' },
        { title: 'Map', key: 'otherAreas' },
        { title: 'Enabled', key: 'enabled' }
      ]
    }
  }
};

</script>

<style scoped>

</style>
