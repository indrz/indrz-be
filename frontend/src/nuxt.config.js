import fs, { glob } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'
import { defineNuxtConfig } from 'nuxt/config'

const __dirname = dirname(fileURLToPath(import.meta.url))
const packageJson = JSON.parse(fs.readFileSync(resolve(__dirname, 'package.json'), 'utf-8'))
const appVersion = packageJson.version || '1.0.0'

const lightTheme = {
  dark: false,
  colors: {
    primary: '#1b9dc4',
    secondary: '#424242',
    accent: '#65dbf5',
    error: '#FF5252',
    info: '#65dbf5',
    success: '#4CAF50',
    warning: '#FB8C00'
  }
}

const darkTheme = {
  dark: true,
  colors: {
    primary: '#1565c0',
    accent: '#424242',
    secondary: '#ffa000',
    info: '#26a69a',
    warning: '#ffc107',
    error: '#ff3d00',
    success: '#00e676'
  }
}



export default defineNuxtConfig({
    // Nuxt 4 compatibility
  future: {
    compatibilityVersion: 4
  },
  ssr: false,
  srcDir: './',
  modules: [
    '@pinia/nuxt',
    'vuetify-nuxt-module',
    '@nuxtjs/i18n'
  ],
  buildModules: ['@nuxtjs/pwa', ],
  runtimeConfig: {
    TOKEN: process.env.TOKEN,
    public: {
      TOKEN: process.env.TOKEN,
      apiBase: process.env.API_BASE || 'http://localhost:8000/api/v1/',
      mapboxToken: process.env.MAPBOX_TOKEN || '',
      baseUrl: process.env.BASE_URL || 'http://localhost:3000',
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
      LOGO_FILE: process.env.LOGO_FILE,
      LOGO_ENABLED: process.env.LOGO_ENABLED,
      NEAREST_METRO_POIID: process.env.NEAREST_METRO_POIID,
      NEAREST_DEFI_POIID: process.env.NEAREST_DEFI_POIID,
      NEAREST_ENTRANCE_POIID: process.env.NEAREST_ENTRANCE_POIID,
      DEFAULT_POI_IMAGE: process.env.DEFAULT_POI_IMAGE,
      GEOSERVER_URL: process.env.NUXT_PUBLIC_GEOSERVER_URL,
      LAYER: process.env.NUXT_PUBLIC_LAYER,
      FONT_FAMILY: process.env.FONT_FAMILY,
      FONT_SIZE: process.env.FONT_SIZE,
      ICON_SET: process.env.ICON_SET
    }
  },
  app: {
    head: {
      titleTemplate: process.env.TITLE || '',
      title: process.env.TITLE || '',
      htmlAttrs: {
        lang: 'en'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'indrz indoor navigation and wayfinding' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: process.env.FAVICON_ICON || '/favicon.ico' }
      ]
    }
  },
  css: [
    'vuetify/styles',
    '~/assets/css/main.css',
    '~/assets/variables.scss',
    '@/assets/css/main.css',
    '@/assets/css/main.scss',
    '@/assets/css/ol.scss',
    '@/assets/css/popup.scss',
    '@/assets/css/draggable_drawer.scss',
    '@/assets/custom_css/floor_changer.scss'
  ],
  // Pinia configuration
  pinia: {
    storesDirs: ['./stores/**']
  },

  // i18n configuration
  i18n: {
    // Keep locale files in-place under assets/locale
    // and avoid moving them under an /i18n/ subdirectory so
    // Nitro looks for /app/assets/locale/*.json instead of /app/i18n/assets/locale/*.json.
    restructureDir: '',
    locales: [
      { code: 'en', iso: 'en-US', file: 'en.json', name: 'English' },
      { code: 'de', iso: 'de-DE', file: 'de.json', name: 'Deutsch' }
    ],
    defaultLocale: 'en',
    strategy: 'prefix_except_default',
    langDir: 'assets/locale',
    lazy: true,
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    }
  },

    // Components auto-import
  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],
  // TypeScript
  typescript: {
    strict: false,
    typeCheck: false,
    shim: false
  },
  // Build configuration
  build: {
    transpile: ['vuetify']
  },
  // Nitro configuration
  nitro: {
    preset: 'node-server',
    compressPublicAssets: true
  },
  // Dev server configuration
  devServer: {
    port: 3000,
    host: '0.0.0.0'
  },
  vuetify: {
    styles: {
      configFile: 'assets/variables.scss'
    },
    vuetifyOptions: {
      defaults: {
        global: {
          ripple: false
        }
      },
      theme: {
        defaultTheme: 'light',
        themes: {
          light: lightTheme,
          dark: darkTheme
        }
      },
      icons: {
        defaultSet: process.env.ICON_SET || 'mdi'
      }
    }
  },
  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: process.env.TITLE || 'Indrz',
      short_name: process.env.TITLE || 'Indrz',
      start_url: '/',
      display: 'standalone',
      background_color: '#ffffff',
      theme_color: '#1b9dc4',
      icons: [
        {
          src: '/icon.png',
          sizes: '512x512',
          type: 'image/png'
        },
        {
          src: '/favicon.ico',
          sizes: '64x64 32x32 16x16',
          type: 'image/x-icon'
        }
      ]
    },
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,jpg,jpeg,svg,gif,ico,json}']
    },
    client: {
      installPrompt: true
    },
}
})
