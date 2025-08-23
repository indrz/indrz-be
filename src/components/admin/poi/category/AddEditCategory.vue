<template>
  <v-dialog :value="dialog" persistent scrollable max-width="500px">
    <v-card>
      <v-toolbar dense flat>
        <div class="headline">
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
                  item-text="name"
                  item-value="id"
                  label="Icon"
                  clearable
                >
                  <template v-slot:selection="{ item }">
                    <v-avatar left>
                      <v-img
                        :src="item.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="avatar left icon"
                      />
                    </v-avatar>
                    {{ item.name }}
                  </template>
                  <template v-slot:item="{ item }">
                    <v-list-item-icon style="margin-right: 16px">
                      <v-img
                        :src="item.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="item icon"
                      />
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title v-text="item.name" />
                    </v-list-item-content>
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
                  item-text="text"
                  item-value="value"
                  label="Parent"
                  clearable
                >
                  <template v-slot:selection="{ item }">
                    <v-avatar left>
                      <v-img
                        :src="item.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="avatar icon"
                      />
                    </v-avatar>
                    {{ item.text }}
                  </template>
                  <template v-slot:item="{ item }">
                    <v-list-item-icon style="margin-right: 16px">
                      <v-img
                        :src="item.icon"
                        contain
                        max-height="24"
                        max-width="24"
                        alt="avatar icon"
                      />
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title v-text="item.text" />
                    </v-list-item-content>
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
                    <label class="v-label theme--light">Activated</label>
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
        <v-btn :disabled="loading" color="blue darken-1" text @click="close">
          Cancel
        </v-btn>
        <v-btn
          :disabled="loading || !valid"
          :loading="loading"
          color="blue darken-1"
          text
          @click="save"
        >
          <v-icon left>
            mdi-content-save
          </v-icon>
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex';

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
    ...mapState({
      poiData: state => state.poi.poiData,
      poiIcons: state => state.poi.poiIcons
    }),
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
    ...mapActions({
      loadPOIIcons: 'poi/LOAD_POI_ICONS',
      getCatgory: 'poi/GET_POI_CATGORY',
      saveCategory: 'poi/SAVE_POI_CATEGORY'
    }),
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
      if (!this.$refs.form.validate()) {
        return;
      }
      this.loading = true;
      const formData = { ...this.selectedCategory };

      if (formData.parent === -1) {
        formData.parent = null;
      }

      const response = await this.saveCategory(formData);
      if (response.isAxiosError) {
        this.$store.commit('SET_SNACKBAR', response.message);
      }

      this.loading = false;
      this.close();
    }
  }
};
</script>

<style scoped></style>
