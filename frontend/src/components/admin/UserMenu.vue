<template>
  <v-menu location="bottom">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        variant="text"
      >
        {{ userEmail }}
      </v-btn>
    </template>
    <v-list>
      <v-list-item
        @click="signOut"
      >
        <template #prepend>
          <v-icon>mdi-logout</v-icon>
        </template>
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { useUserStore } from '~/stores/user';

export default {
  name: 'UserMenu',
  computed: {
    userEmail () {
      const userStore = useUserStore();
      return userStore.userEmail;
    }
  },
  methods: {
    signOut () {
      const userStore = useUserStore();
      userStore.SIGN_OUT();
    }
  }
};
</script>

<style scoped>

</style>
