import colors from 'vuetify/es5/util/colors';
const fs = require('fs')
const packageJson = fs.readFileSync('./package.json')
const appVersion = JSON.parse(packageJson).version || '1.0.0';

export default {
  ssr: false,
  /*
  ** Headers of the page
  */
  env: {
    BASE_API_URL: process.env.BASE_API_URL,
    TOKEN: process.env.TOKEN
  },
  head: {
    titleTemplate: process.env.TITLE || '',
    title: process.env.TITLE || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: process.env.FAVICON_ICON }
    ]
  },
  target: 'static',
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    // CSS file in the project
    '@/assets/css/main.css',
    // SCSS file in the project
    '@/assets/css/main.scss',
    '@/assets/css/ol.scss',
    '@/assets/css/popup.scss',
    '@/assets/css/draggable_drawer.scss',
    '@/assets/custom_css/floor_changer.scss'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  router: {
    middleware: [
      // 'i18n',
      'auth'
    ]
  },
  plugins: [
    '~/plugins/i18n.js',
    '~/plugins/env.js'
  ],
  // generate: {
  //   routes: ['/', '/about', '/fr', '/fr/about']
  // },
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    '@nuxtjs/vuetify'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  env: {
    APP_VERSION: appVersion,
    BASE_URL: process.env.BASE_URL,
    BASE_API_URL: process.env.BASE_API_URL,
    BASE_WMS_URL: process.env.BASE_WMS_URL,
    SEARCH_URL: process.env.SEARCH_URL,
    SHARE_SPACE_URL: process.env.SHARE_SPACE_URL,
    HOME_PAGE_URL: process.env.HOME_PAGE_URL,
    DEFAULT_CENTER_XY: process.env.DEFAULT_CENTER_XY,
    MOBILE_START_CENTER_XY: process.env.MOBILE_START_CENTER_XY,
    LAYER_NAME_PREFIX: process.env.LAYER_NAME_PREFIX,
    GEO_SERVER_LAYER_PREFIX: process.env.GEO_SERVER_LAYER_PREFIX,
    DEFAULT_START_FLOOR: process.env.DEFAULT_START_FLOOR,
    DEFAULT_START_ZOOM: process.env.DEFAULT_START_ZOOM,
    MOBILE_START_ZOOM: process.env.MOBILE_START_ZOOM,
    TITLE: process.env.TITLE,
    PDF_TITLE: process.env.PDF_TITLE,
    TOKEN: process.env.TOKEN,
    LOGO_FILE: process.env.LOGO_FILE,
    LOGO_ENABLED: process.env.LOGO_ENABLED,
    NEAREST_METRO_POIID: process.env.NEAREST_METRO_POIID,
    NEAREST_DEFI_POIID: process.env.NEAREST_DEFI_POIID,
    NEAREST_ENTRANCE_POIID: process.env.NEAREST_ENTRANCE_POIID,
    DEFAULT_POI_IMAGE: process.env.DEFAULT_POI_IMAGE
  },
  publicRuntimeConfig: {
    APP_VERSION: appVersion,
    BASE_URL: process.env.BASE_URL,
    BASE_API_URL: process.env.BASE_API_URL,
    BASE_WMS_URL: process.env.BASE_WMS_URL,
    SEARCH_URL: process.env.SEARCH_URL,
    SHARE_SPACE_URL: process.env.SHARE_SPACE_URL,
    HOME_PAGE_URL: process.env.HOME_PAGE_URL,
    DEFAULT_CENTER_XY: process.env.DEFAULT_CENTER_XY,
    MOBILE_START_CENTER_XY: process.env.MOBILE_START_CENTER_XY,
    LAYER_NAME_PREFIX: process.env.LAYER_NAME_PREFIX,
    GEO_SERVER_LAYER_PREFIX: process.env.GEO_SERVER_LAYER_PREFIX,
    DEFAULT_START_FLOOR: process.env.DEFAULT_START_FLOOR,
    DEFAULT_START_ZOOM: process.env.DEFAULT_START_ZOOM,
    MOBILE_START_ZOOM: process.env.MOBILE_START_ZOOM,
    TITLE: process.env.TITLE,
    PDF_TITLE: process.env.PDF_TITLE,
    TOKEN: process.env.TOKEN,
    LOGO_FILE: process.env.LOGO_FILE,
    LOGO_ENABLED: process.env.LOGO_ENABLED,
    NEAREST_METRO_POIID: process.env.NEAREST_METRO_POIID,
    NEAREST_DEFI_POIID: process.env.NEAREST_DEFI_POIID,
    NEAREST_ENTRANCE_POIID: process.env.NEAREST_ENTRANCE_POIID,
    DEFAULT_POI_IMAGE: process.env.DEFAULT_POI_IMAGE
  },
  privateRuntimeConfig: {
    TOKEN: process.env.TOKEN
  },
  axios: {
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    defaultAssets: {
      font: {
        family: process.env.FONT_FAMILY, // ROBOTO is default
        size: process.env.FONT_SIZE // 16 is default
      },
      icons: process.env.ICON_SET // mdi, md, fa, fa4
    },
    theme: {
      dark: false,
      default: 'light',
      themes: {
        light: {
          primary: '#1b9dc4',
          secondary: '#424242',
          accent: '#65dbf5',
          error: '#FF5252',
          info: '#65dbf5',
          success: '#4CAF50',
          warning: '#FB8C00'
        },
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    }
  }
};
