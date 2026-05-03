<template>
  <v-dialog :model-value="dialog" persistent scrollable max-width="500px">
    <v-card>
      <v-toolbar density="compact" elevation="0">
        <div class="text-h6">
          {{ title }}
        </div>
        <v-spacer />
        <v-btn icon @click="close">
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-divider />
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-container>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="selectedCategory.cat_name"
                  :rules="requiredRule"
                  label="Category name"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-autocomplete
                  v-model="selectedCategory.fk_poi_icon"
                  :items="poiIcons"
                  :rules="requiredRule"
                  item-title="name"
                  item-value="id"
                  label="Icon"
                  clearable
                >
                  <template v-slot:selection="{ item }">
                    <v-avatar class="mr-2">
                      <v-img
                        :src="item.raw.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="avatar left icon"
                      />
                    </v-avatar>
                    {{ item.raw.name }}
                  </template>
                  <template v-slot:item="{ item, props }">
                    <v-list-item v-bind="props">
                      <template #prepend>
                        <v-avatar class="mr-2">
                          <v-img
                            :src="item.raw.icon"
                            contain
                            max-height="24"
                            max-width="24"
                            alt="item icon"
                          />
                        </v-avatar>
                      </template>
                      <v-list-item-title v-text="item.raw.name" />
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-autocomplete
                  v-model="selectedCategory.parent"
                  :items="categoryOptions"
                  :rules="requiredRule"
                  item-title="text"
                  item-value="value"
                  label="Parent"
                  clearable
                >
                  <template v-slot:selection="{ item }">
                    <v-avatar class="mr-2">
                      <v-img
                        :src="item.raw.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="avatar icon"
                      />
                    </v-avatar>
                    {{ item.raw.text }}
                  </template>
                  <template v-slot:item="{ item, props }">
                    <v-list-item v-bind="props">
                      <template #prepend>
                        <v-avatar class="mr-2">
                          <v-img
                            :src="item.raw.icon"
                            contain
                            max-height="24"
                            max-width="24"
                            alt="avatar icon"
                          />
                        </v-avatar>
                      </template>
                      <v-list-item-title v-text="item.raw.text" />
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="selectedCategory.cat_name_en"
                  label="Category name EN"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-text-field
                  v-model="selectedCategory.cat_name_de"
                  label="Category name DE"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-row no-gutters>
                  <v-col cols="3">
                    <label class="v-label">Activated</label>
                  </v-col>
                  <v-col cols="8">
                    <v-switch
                      v-model="selectedCategory.enabled"
                      inset
                      style="padding: 0; margin: 0"
                    />
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="loading" color="blue-darken-1" variant="text" @click="close">
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading || !valid"
          :loading="loading"
          color="blue-darken-1"
          variant="text"
          @click="save"
        >
          <v-icon start>
            mdi-content-save
          </v-icon>
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { usePoiStore } from '~/stores/poi';
import { useRootStore } from '~/stores/root';

export default {
  name: 'AddEditCategory',
  props: {
    title: {
      type: String,
      default: function () {
        return '';
      }
    },
    dialog: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    propsCategory: {
      type: Object,
      default: function () {
        return {
          id: null
        };
      }
    }
  },
  data () {
    return {
      loading: false,
      valid: true,
      requiredRule: [v => !!v || 'This field is required.'],
      selectedCategory: {
        type: Object,
        default: function () {
          return {
            id: null,
            cat_name: null,
            fk_poi_icon: null,
            icon: null,
            parent: null,
            cat_name_en: null,
            cat_name_de: null,
            enabled: true
          };
        }
      }
    };
  },
  computed: {
    poiData () {
      const poiStore = usePoiStore();
      return poiStore.poiData;
    },
    poiIcons () {
      const poiStore = usePoiStore();
      return poiStore.poiIcons;
    },
    categoryOptions () {
      let options = [];
      this.poiData.forEach((category) => {
        options = options.concat(this.prepareCategoryOptions(category, 0));
      });

      return [
        {
          text: '--------',
          value: -1
        }
      ].concat(options);
    }
  },
  watch: {
    dialog: async function (newValue) {
      if (newValue === true) {
        this.selectedCategory = { ...this.propsCategory };
        if (this.propsCategory.id) {
          this.selectedCategory = await this.getCatgory(this.propsCategory.id);
          if (this.selectedCategory.parent === null) {
            this.selectedCategory.parent = -1;
          }
        }
        if (this.$refs?.form) {
          this.$refs.form.resetValidation();
          if (!this.propsCategory.id) {
            this.selectedCategory.enabled = true;
          }
        }
      } else {
        this.selectedCategory = {};
      }
    }
  },
  mounted () {
    this.loadPOIIcons();
  },
  methods: {
    async loadPOIIcons () {
      const poiStore = usePoiStore();
      await poiStore.LOAD_POI_ICONS();
    },
    async getCatgory (id) {
      const poiStore = usePoiStore();
      return await poiStore.GET_POI_CATGORY({}, id);
    },
    async saveCategory (formData) {
      const poiStore = usePoiStore();
      return await poiStore.SAVE_POI_CATEGORY({}, formData);
    },
    prepareCategoryOptions (category, level) {
      let categoryOptions = [
        {
          text: `${'-'.repeat(level * 2)} ${category.name}`,
          value: category.id,
          icon: category.icon
        }
      ];

      if (category.children) {
        category.children.forEach((childCategory) => {
          categoryOptions = categoryOptions.concat(
            this.prepareCategoryOptions(childCategory, level + 1)
          );
        });
      }
      return categoryOptions;
    },
    close () {
      this.$refs.form.reset();
      this.$refs.form.resetValidation();
      this.$emit('close');
    },
    async save () {
      const result = await this.$refs.form.validate();
      const isValid = typeof result === 'object' ? result.valid : result;
      if (!isValid) {
        return;
      }
      this.loading = true;
      const formData = { ...this.selectedCategory };

      if (formData.parent === -1) {
        formData.parent = null;
      }

      const response = await this.saveCategory(formData);
      if (response.isAxiosError) {
        const rootStore = useRootStore();
        rootStore.SET_SNACKBAR(response.message);
      }

      this.loading = false;
      this.close();
    }
  }
};
</script>

<style scoped></style>
