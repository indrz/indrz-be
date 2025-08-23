<template>
  <div>
    <template v-if="isRoute">
      <div>
        <v-autocomplete
          ref="searchField"
          :key="`search-route-bar-${updateKey}`"
          v-model="model"
          :items="searchResult"
          :loading="isLoading"
          :search-input.sync="search"
          :prepend-icon="icon"
          :no-filter="true"
          :label="routeLabel"
          :hide-no-data="true"
          :item-text="getSearchTitle"
          item-value="id"
          append-icon=""
          single-line
          return-object
          flat
          hide-details
          @click:clear="onClearClick"
          @change="onSearchSelection"
          @focus="focused = true"
          @blur="focused = false"
        >
          <template v-slot:append>
            <v-icon class="search-btn" aria-label="Search Button">
              mdi-magnify
            </v-icon>
          </template>
          <template v-slot:append-outer>
            <v-icon :color="activeClearColor" aria-label="Close search button" @click.stop="onClearClick">
              mdi-close
            </v-icon>
          </template>
          <template v-slot:item="{ item }">
            <v-list-item-icon data-test="searchResult" style="margin-right: 16px" aria-label="Show icon">
              <v-img
                :src="getIconUrl(item.src_icon)"
                contain
                max-height="24"
                max-width="24"
                alt="icon"
              />
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="getSearchTitle(item)" />
              <v-list-item-subtitle v-text="`(${item.code ? item.code + ', ': ''}${searchResultFloorLabel} ${item.floorNum})`" />
            </v-list-item-content>
          </template>
        </v-autocomplete>
      </div>
      <div v-if="focused">
        <div :style="{'text-align': (isLoading) ? 'center' : 'left'}" class="v-label no-data-text theme--light">
          <template v-if="!search || search.length < 3">
            <v-icon small aria-label="information">
              mdi-information-outline
            </v-icon> {{ minSearchCharacterLengthMessage }}
          </template>
          <template v-else-if="search && search.length && !isLoading && !searchResult.length">
            <v-icon small aria-label="information">
              mdi-information-outline
            </v-icon> {{ noResultText }}
          </template>
        </div>
      </div>
    </template>
    <template v-else>
      <v-autocomplete
        ref="searchField"
        :key="`search-bar-${updateKey}`"
        v-model="model"
        :items="searchResult"
        :loading="isLoading"
        :search-input.sync="search"
        :no-filter="true"
        :label="searchLabel"
        :item-text="getSearchTitle"
        item-value="id"
        append-icon=""
        single-line
        return-object
        solo
        flat
        hide-details
        @click:clear="onClearClick"
        @change="onSearchSelection"
      >
        <template v-slot:append>
          <v-icon
            class="search-btn"
            aria-label="Search button search on campus"
          >
            mdi-magnify
          </v-icon>
        </template>
        <template v-slot:append-outer>
          <v-icon
            v-if="showRoute && !search?.length"
            data-test="directionsShortcutBtn"
            color="blue darken-2"
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
          <div class="v-list-item">
            <div class="v-list-item__content">
              <div :style="{'text-align': (isLoading) ? 'center' : 'left'}" class="v-list-item__title">
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
              </div>
            </div>
          </div>
        </template>
        <template v-slot:item="{ item }">
          <v-list-item-icon style="margin-right: 16px" aria-label="image icon">
            <v-img
              v-if="item.icon"
              :src="item.icon"
              contain
              max-height="24"
              max-width="24"
              alt="icon"
            />
            <v-img
              v-else
              :src="getIconUrl(item.src_icon)"
              contain
              max-height="24"
              max-width="24"
              alt="icon"
            />
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="getSearchTitle(item)" />
            <v-list-item-subtitle v-text="`(${item.code ? item.code + ', ': ''}${searchResultFloorLabel} ${item.floorNum})`" />
          </v-list-item-content>
        </template>
      </v-autocomplete>
    </template>
  </div>
</template>

<script>
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, switchMap } from 'rxjs/operators';
import api from '../util/api';
import MapHandler from '~/util/mapHandler';

export default {
  props: {
    isRoute: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    drawer: {
      type: Boolean,
      default: false
    },
    selected: {
      type: Object,
      default: function () {
        return {};
      }
    },
    showRoute: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    routeLabel: {
      type: String,
      default: function () {
        return '';
      }
    },
    routeType: {
      type: String,
      default: function () {
        return 'from';
      }
    },
    icon: {
      type: String,
      default: function () {
        return '';
      }
    },
    shouldSearch: {
      type: Boolean,
      default: function () {
        return true;
      }
    }
  },
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
    activeClearColor () {
      return this.search && this.search.length ? 'blue darken-2' : 'grey';
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
      this.search = MapHandler.getTitle(data, this.$i18n.locale)
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

    this.$root.$on('load-search-query', this.onLoadSearchQuery);
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
    onLoadSearchQuery (query) {
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
      return data[`name_${this.$i18n.locale}`] || data.name || this.selected.name
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
    padding-right: 5px
  }
  ::v-deep .v-input__slot {
    padding-right: 0px !important;
  }
</style>
