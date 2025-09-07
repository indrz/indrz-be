<template>
  <v-app>
    <v-main>
      <div class="box">
        <div :id="headerId" class="box-row header">
          <!-- Any code below will show up on Header -->
        </div>
        <v-container class="box-row content">
          <nuxt />
        </v-container>
        <div :id="footerId" class="box-row footer">
          <!-- Any code below will show up on Footer -->
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import mapHandler from '~/util/mapHandler';

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
  created: function () {
    const currentLocale = this.getLocale();
    let defaultLocale = 'en';

    if (currentLocale.includes('de')) {
      defaultLocale = 'de';
    }
    this.$i18n.locale = defaultLocale;

    mapHandler.setI18n(this.$i18n);
  },
  methods: {
    getLocale () {
      return (
        navigator.language ||
        navigator.browserLanguage ||
        (navigator.languages || ['en'])[0]
      );
    }
  }
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
