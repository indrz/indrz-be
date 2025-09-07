<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        text
        dark
      >
        {{ userEmail }}
      </v-btn>
    </template>
    <v-list>
      <v-list-item
        @click="signOut"
      >
        <v-list-item-action>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-action>
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserMenu',
  computed: {
    ...mapGetters({
      userEmail: 'user/userEmail'
    })
  },
  methods: {
    signOut () {
      this.$store.dispatch('user/SIGN_OUT');
    }
  }
};
</script>

<style scoped>

</style>
