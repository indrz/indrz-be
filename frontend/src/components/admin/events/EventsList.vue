<template>
  <div>
    <H1>BETA EVENTS MOCKUP</H1>
    <v-data-table
      :headers="headers"
      :items="indrzEvents"
      class="elevation-1"
    >
      <template v-slot: item.enabled="{ item }">
        <v-simple-checkbox
          v-model="item.enabled"
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
        { text: 'Name', value: 'name' },
        { text: 'Start Date', value: 'startDate' },
        { text: 'End Date', value: 'endDate' },
        { text: 'Room Code(s)', value: 'roomCode' },
        { text: 'Map', value: 'otherAreas' },
        { text: 'Enabled', value: 'enabled' }
      ]
    }
  }
};

</script>

<style scoped>

</style>
