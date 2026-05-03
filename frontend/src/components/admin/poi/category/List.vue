<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-toolbar elevation="0" density="compact">
            <v-spacer />
            <v-btn aria-label="Add Category" icon size="small" color="indigo" @click="addCategory">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
            <v-btn
              :disabled="!hasActiveCategory"
              icon
              size="small"
              color="green"
              @click="editCategory"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              :disabled="!hasActiveCategory"
              aria-label="Delete Category"
              icon
              size="small"
              color="red"
              @click="showConfirmDelete = true"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <div class="text-center">
              <v-progress-circular
                v-if="loading"
                indeterminate
                color="primary"
              />
            </div>
            <v-treeview
              v-if="!loading"
              ref="poi"
              v-model:active="currentCategory"
              :items="poiData"
              activatable
              hoverable
              item-value="id"
              class="poi no-checkbox"
              density="compact"
              style="overflow: auto; width: auto;"
            >
              <template #title="{ item }">
                <span style="white-space: normal">
                  {{ getItemLabel(item) }}
                </span>
              </template>
              <template v-slot:prepend="{ item }">
                <div>
                  <img v-if="getTreeItem(item).icon" :src="getTreeItem(item).icon" style="height:25px;">
                  <img
                    v-else
                    src="/images/other_pin_grey.png"
                    style="height:25px;"
                  >
                </div>
              </template>
            </v-treeview>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <add-edit-category
      :title="addEditDialogTitle"
      :dialog="categoryAddEditDialog"
      :props-category="selectedCategory"
      @close="addEditCategoryClose"
    />
    <confirm-dialog
      :show="showConfirmDelete"
      :busy="loading"
      @cancelClick="showConfirmDelete = false"
      @confirmClick="onConfirmDeleteCategory"
    />
  </v-container>
</template>

<script>
import AddEditCategory from './AddEditCategory';
import PointsOfInterest from '@/components/poi/PointsOfInterest';
import ConfirmDialog from '@/components/ConfirmDialog';
import { usePoiStore } from '~/stores/poi';

export default {
  name: 'PoiCategoryList',
  components: {
    AddEditCategory,
    PointsOfInterest,
    ConfirmDialog
  },
  data () {
    return {
      currentCategory: [],
      selectedCategory: {},
      categoryAddEditDialog: false,
      showConfirmDelete: false,
      addEditDialogTitle: '',
      defaultOptions: {
        enabled: true
      },
      loading: true
    };
  },
  computed: {
    currentLocale () {
      const raw = this.$i18n?.locale
      return raw && typeof raw === 'object' && 'value' in raw ? raw.value : raw
    },
    poiData () {
      const poiStore = usePoiStore();
      return poiStore.poiData;
    },
    findNode () {
      const poiStore = usePoiStore();
      return poiStore.findNode;
    },
    treeComp () {
      return this.$refs.poi;
    },
    hasActiveCategory () {
      return this.currentCategory.length;
    }
  },

  watch: {
    categoryAddEditDialog (val) {
      val || this.addEditCategoryClose();
    }
  },

  mounted () {
    this.loadDataToPoiTree();
  },

  methods: {
    getTreeItem (item) {
      return item && item.raw ? item.raw : item;
    },
    getItemLabel (item) {
      const data = this.getTreeItem(item)
      const locale = this.currentLocale || 'en'
      return data?.[`name_${locale}`] || data?.name_en || data?.name_de || data?.name || ''
    },
    async loadPOI () {
      const poiStore = usePoiStore();
      await poiStore.LOAD_POI();
    },
    async deleteCatgory (id) {
      const poiStore = usePoiStore();
      await poiStore.DELETE_POI_CATGORY({}, id);
    },
    async loadDataToPoiTree () {
      await this.loadPOI();
      this.loading = false;
    },
    addCategory () {
      this.addEditDialogTitle = 'Add Category';
      const parent =
        this.currentCategory && this.currentCategory.length
          ? this.currentCategory[0].id
          : -1;
      this.selectedCategory = { ...this.defaultOptions, parent };
      this.categoryAddEditDialog = true;
    },
    editCategory () {
      this.addEditDialogTitle = 'Edit Category';
      this.selectedCategory = Object.assign(
        { ...this.defaultOptions },
        {
          ...(this.currentCategory?.length ? this.currentCategory[0] : {})
        }
      );
      this.categoryAddEditDialog = true;
    },
    addEditCategoryClose () {
      this.categoryAddEditDialog = false;
    },
    async onConfirmDeleteCategory () {
      this.loading = true;

      await this.deleteCatgory(this.currentCategory[0].id);

      this.showConfirmDelete = false;
      this.loading = false;
    }
  }
};
</script>
