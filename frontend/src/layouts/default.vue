<template>
  <v-app>
    <v-main>
      <div class="box">
        <div :id="headerId" class="box-row header">
          <!-- Any code below will show up on Header -->
        </div>
        <v-container class="box-row content">
          <NuxtPage />
        </v-container>
        <div :id="footerId" class="box-row footer">
          <!-- Any code below will show up on Footer -->
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      headerId: 'indrz-header-container',
      footerId: 'indrz-footer-container',
      items: [
        {
          icon: 'mdi-apps',
          title: 'Home',
          to: '/'
        }
      ],
      miniVariant: false
    };
  },
  // Locale detection/redirect is handled by @nuxtjs/i18n (see nuxt.config.js).
};
</script>

<style>
.box {
  display: flex;
  flex-flow: column;
  height: 100%;
}

.box .header {
  flex: 0 1 auto;
}

.box .content {
  flex: 1 1 auto;
  max-width: 100%;
  padding: 0px;
  margin: 0px;
}

.box .footer {
  flex: 0 1 auto;
}
</style>
