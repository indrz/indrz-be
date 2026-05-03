<template>
  <div>
    <template v-if="isRoute">
      <div>
        <v-autocomplete
          ref="searchField"
          :key="`search-route-bar-${updateKey}`"
          v-model="model"
          v-model:search="search"
          :items="searchResult"
          :loading="isLoading"
          :prepend-icon="icon"
          :no-filter="true"
          :label="routeLabel"
          :hide-no-data="true"
          :item-title="getSearchTitle"
          item-value="id"
          variant="underlined"
          return-object
          hide-details
          @click:clear="onClearClick"
          @update:model-value="onSearchSelection"
          @focus="focused = true"
          @blur="focused = false"
        >
          <template v-slot:append-inner>
            <v-icon class="search-btn" aria-label="Search Button">
              mdi-magnify
            </v-icon>
          </template>
          <template v-slot:append>
            <v-icon :color="activeClearColor" aria-label="Close search button" @click.stop="onClearClick">
              mdi-close
            </v-icon>
          </template>
          <template v-slot:item="{ item, props }">
            <v-list-item v-bind="props" data-test="searchResult">
              <template #prepend>
                <v-img
                  :src="getIconUrl(item.raw.src_icon)"
                  max-height="24"
                  max-width="24"
                  alt="icon"
                  class="mr-4"
                />
              </template>
              <v-list-item-title v-text="getSearchTitle(item.raw)" />
              <v-list-item-subtitle v-text="`(${item.raw.code ? item.raw.code + ', ': ''}${searchResultFloorLabel} ${item.raw.floorNum})`" />
            </v-list-item>
          </template>
        </v-autocomplete>
      </div>
      <div v-if="focused">
        <div :style="{'text-align': (isLoading) ? 'center' : 'left'}" class="v-label no-data-text">
          <template v-if="!search || search.length < 3">
            <v-icon size="small" aria-label="information">
              mdi-information-outline
            </v-icon> {{ minSearchCharacterLengthMessage }}
          </template>
          <template v-else-if="search && search.length && !isLoading && !searchResult.length">
            <v-icon size="small" aria-label="information">
              mdi-information-outline
            </v-icon> {{ noResultText }}
          </template>
        </div>
      </div>
    </template>
    <template v-else>
      <div style="width: 350px;">
      <v-autocomplete
        ref="searchField"
        :key="`search-bar-${updateKey}`"
        v-model="model"
        v-model:search="search"
        :items="searchResult"
        :loading="isLoading"
        :no-filter="true"
        :label="searchLabel"
        :item-title="getSearchTitle"
        item-value="id"
        :variant="large ? 'outlined' : 'solo'"
        return-object
        hide-details
        @click:clear="onClearClick"
        @update:model-value="onSearchSelection"
      >
        <template v-slot:append-inner>
          <v-icon
            class="search-btn"
            aria-label="Search button search on campus"
          >
            mdi-magnify
          </v-icon>
        </template>
        <template v-slot:append>
          <v-icon
            v-if="showRoute && !search?.length"
            data-test="directionsShortcutBtn"
            color="primary"
            aria-label="Get directions button"
            @click.stop="onRouteButtonClick"
          >
            mdi-directions
          </v-icon>
          <v-icon v-else :color="activeClearColor" aria-label="Get directions" @click.stop="onClearClick">
            mdi-close
          </v-icon>
        </template>
        <template v-slot:no-data>
          <v-list-item>
            <v-list-item-title :style="{'text-align': (isLoading) ? 'center' : 'left'}">
              <template v-if="!search || search.length < 3">
                {{ minSearchCharacterLengthMessage }}
              </template>
              <v-progress-circular
                v-else-if="search && search.length && isLoading"
                indeterminate
                color="primary"
              />
              <template v-else-if="search && search.length && !isLoading && !searchResult.length">
                {{ noResultText }}
              </template>
            </v-list-item-title>
          </v-list-item>
        </template>
        <template v-slot:item="{ item, props }">
          <v-list-item v-bind="props">
            <template #prepend>
              <v-img
                v-if="item.raw.icon"
                :src="item.raw.icon"
                max-height="24"
                max-width="24"
                alt="icon"
                class="mr-4"
              />
              <v-img
                v-else
                :src="getIconUrl(item.raw.src_icon)"
                max-height="24"
                max-width="24"
                alt="icon"
                class="mr-4"
              />
            </template>
            <v-list-item-title v-text="getSearchTitle(item.raw)" />
            <v-list-item-subtitle v-text="`(${item.raw.code ? item.raw.code + ', ': ''}${searchResultFloorLabel} ${item.raw.floorNum})`" />
          </v-list-item>
          </template>
          </v-autocomplete>
          </div>
        </template>
  </div>
</template>

<script>
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';
import api from '../util/api';
import MapHandler from '~/util/mapHandler';
import bus from '~/util/bus';

export default {
  props: {
    isRoute: {
      type: Boolean,
      default: false
    },
    drawer: {
      type: Boolean,
      default: false
    },
    selected: {
      type: Object,
      default: () => ({})
    },
    showRoute: {
      type: Boolean,
      default: false
    },
    routeLabel: {
      type: String,
      default: ''
    },
    routeType: {
      type: String,
      default: 'from'
    },
    icon: {
      type: String,
      default: ''
    },
    shouldSearch: {
      type: Boolean,
      default: true
    },
    large: {
      type: Boolean,
      default: false
    }
  },
  emits: ['selectSearchResult', 'clearClicked', 'open-route-drawer', 'showSearch'],
  data () {
    return {
      updateKey: 1,
      searchLabel: this.$t('search_our_campus'),
      minSearchCharacterLengthMessage: this.$t('min_search_character_length_message'),
      noResultText: this.$t('no_result_found'),
      searchResultFloorLabel: this.$t('label_floor_name'),
      serachItemLimit: 100,
      searchResult: [],
      apiResponse: [],
      isLoading: false,
      isPristine: true,
      term$: new Subject(),
      model: null,
      search: null,
      stopSearch: false,
      focused: false,
      iconNames: ['book', 'department', 'person', 'poi', 'space'],
      iconPath: '/images/icons/search/'
    }
  },
  computed: {
      currentLocale () {
        const raw = this.$i18n?.locale
        return raw && typeof raw === 'object' && 'value' in raw ? raw.value : raw
      },
    activeClearColor () {
      return this.search && this.search.length ? 'blue-darken-2' : 'grey';
    }
  },
  watch: {
    search (text) {
      if (!text) {
        this.isPristine = true;
      }
      this.shouldSearch && (this.model?.name !== text) && this.term$.next(text);
      if (text && typeof text !== 'string' && this.selected) {
        const temp = text
        if (!text.name) {
          temp.name = text.room_code
        }
        this.searchResult = [temp]
        this.model = temp
        this.search = temp.room_code
        this.updateKey++;
      }
    }
  },
  created () {
    if (this.selected && this.selected.name && this.drawer) {
      const properties = this.selected;
      const code = properties.room_code
      const data = {
        ...properties,
        ...{
          floorNum: properties.floor_num,
          roomCode: properties.room_code,
          building: properties.building,
          src_icon: properties.src_icon || properties.icon,
          code,
          id: properties.id
        }
      };
        this.search = MapHandler.getTitle(data, this.currentLocale)
      this.searchResult = [data]
      this.model = data
    }
  },
  mounted () {
    this
      .term$
      .pipe(
        filter(term => (term && term.length > 2 && !this.stopSearch)),
        debounceTime(500),
        distinctUntilChanged((prevTerm, currentTerm) => {
          return prevTerm === currentTerm && !this.isPristine;
        }),
        switchMap((term) => {
          this.isLoading = true;
          this.isPristine = false;
          return api.request({
            endPoint: 'search/' + term
          }, {
            baseApiUrl: process.env.BASE_API_URL,
            token: process.env.TOKEN
          })
            .catch((err) => {
              console.log(err);
            })
            .finally(() => (this.isLoading = false));
        })
      ).subscribe(response => this.apiSearch(response));

    bus.on('load-search-query', this.onLoadSearchQuery);
  },
  methods: {
    apiSearch (response) {
      if (!response || !response.data) {
        return;
      }
      this.apiResponse = response.data.features.filter(feature => feature.properties && feature.properties.name);
      if (this.apiResponse.length > 100) {
        this.apiResponse = this.apiResponse.slice(0, this.serachItemLimit);
      }

      this.searchResult = this.apiResponse.map(({ id, properties }) => {
        let code = properties.room_code;

        if (code && code.toLowerCase() === this.search.toLowerCase()) {
          code = properties.room_category || properties.external_id || code;
        }

        const data = {
          ...properties,
          ...{
            floorNum: properties.floor_num,
            roomCode: properties.room_code,
            building: properties.building,
            src_icon: properties.src_icon || properties.icon,
            code,
            id: properties.id
          }
        };

        if (properties.category) {
          properties.poiId = id;
        }

        return data;
      });
    },
    onSearchSelection (selection) {
      let data = null;

      if (selection) {
        data = this.apiResponse.find(({ properties }) => properties.id === selection.id);
      }

      this.$emit('selectSearchResult', {
        data: data,
        routeType: this.routeType
      });
    },
    onClearClick () {
      this.$nextTick(() => {
        this.search = '';
        this.searchResult = [];
        this.$refs.searchField.blur();
        this.$emit('clearClicked');
      });
    },
    onRouteButtonClick () {
      this.$emit('open-route-drawer');
    },
    getValue () {
      return this.model;
    },
    clearSearch () {
      this.model = null;
      this.searchResult = [];
      this.apiResponse = [];
    },
    onLoadSearchQuery () {
      this.$emit('showSearch');
      /*      setTimeout(() => {
        const searchField = this.$refs.searchField;

        this.search = query;
        searchField.focus();
        searchField.activateMenu();
      }, 1000); */
    },
    getIconUrl (iconName) {
      if (!iconName) {
        return '';
      }
      if (this.iconNames.includes(iconName)) {
        return `${this.iconPath}/${iconName}.png`;
      } else if (iconName.includes('.png')) {
        return `${iconName}`
      }
      return `${this.iconPath}/poi.png`;
    },
    getSearchTitle (data) {
      // return name_*locale if available, name otherwise
        return data[`name_${this.currentLocale}`] || data.name || this.selected.name
    }
  }
};
</script>

<style scoped>
  .no-data-text {
    text-align: left;
    margin: 10px 0 0 30px;
  }
  .search-btn {
    border-right: 1px solid #d3d3d3;
    padding-right: 5px;
  }
</style>

