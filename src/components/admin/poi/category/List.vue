<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-toolbar flat dens>
            <v-spacer />
            <v-btn aria-label="Add Category" icon small color="indigo" @click="addCategory">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
            <v-btn
              :disabled="!hasActiveCategory"
              icon
              small
              color="green"
              @click="editCategory"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              :disabled="!hasActiveCategory"
              aria-label="Delete Category"
              icon
              small
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
              :active.sync="currentCategory"
              :multiple-active="false"
              :items="poiData"
              transition
              activatable
              hoverable
              return-object
              item-key="id"
              class="poi no-checkbox"
              dense
              style="overflow: auto; width: auto;"
            >
              <template slot="label" slot-scope="{ item }">
                <span style="white-space: normal">
                  {{ item["name_" + $i18n.locale] }}
                </span>
              </template>
              <template v-slot:prepend="{ item }">
                <div>
                  <img v-if="item.icon" :src="item.icon" style="height:25px;">
                  <img
                    v-else
                    src="/media/poi_icons/other_pin_grey.png"
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
import { mapActions, mapState, mapGetters } from 'vuex';
import AddEditCategory from './AddEditCategory';
import PointsOfInterest from '@/components/poi/PointsOfInterest';
import ConfirmDialog from '@/components/ConfirmDialog';

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
    ...mapState({
      poiData: state => state.poi.poiData
    }),
    ...mapGetters({
      findNode: 'poi/findNode'
    }),
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
    ...mapActions({
      loadPOI: 'poi/LOAD_POI',
      deleteCatgory: 'poi/DELETE_POI_CATGORY'
    }),
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
