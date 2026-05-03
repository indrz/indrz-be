<template>
  <div>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="shelfListData"
        :loading="loading"
        :height="height"
        :no-data-text="noDataText"
        @click:row="onShelfDataClick"
        density="compact"
        class="elevation-1"
        loading-text="Loading... Please wait"
        :items-per-page="-1"
      >
        <template v-slot:top>
          <v-toolbar elevation="0">
            <v-toolbar-title>Shelf Data</v-toolbar-title>
            <v-spacer />
            <v-btn
              :disabled="!selectedShelf || shelfDataAddEditDialog"
              @click="addShelfData"
              variant="outlined"
            >
              <v-icon start>
                mdi-plus
              </v-icon>
              Shelf Data
            </v-btn>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            @click.stop="editShelfData(item)"
            size="small"
            class="mr-1"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            @click.stop="deleteShelfDataItem(item)"
            size="small"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
      <v-dialog v-model="shelfDataAddEditDialog" max-width="500px">
        <v-card>
          <v-card-title>{{ shelfDataFormTitle }}</v-card-title>
          <add-edit-shelf-data
            ref="shelfDataForm"
            :title="shelfDataFormTitle"
            :dialog="shelfDataAddEditDialog"
            :current-shelf-data="shelfDataEditedItem"
            @close="shelfDataAddEditDialogClose"
          />
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="shelfDataAddEditDialogClose">Cancel</v-btn>
            <v-btn color="primary" variant="elevated" @click="$refs.shelfDataForm.save()">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <confirm-dialog
        :show="showConfirmDeleteShelfData"
        :message="deleteShelfDataConfirmMessage"
        :busy="loading"
        @cancelClick="showConfirmDeleteShelfData = false"
        @confirmClick="confirmDeleteShelfData"
      />
    </v-card>
  </div>
</template>

<script>
import ConfirmDialog from '@/components/ConfirmDialog';
import AddEditShelfData from '@/components/admin/shelves/AddEditShelfData';
import { useShelfStore } from '~/stores/shelf';

export default {
  name: 'ShelfDataList',
  components: { ConfirmDialog, AddEditShelfData },
  props: {
    height: {
      type: Number,
      default: 600
    }
  },
  data () {
    return {
      loading: false,
      singleSelect: false,
      shelfDataAddEditDialog: false,
      showConfirmDeleteShelfData: false,
      selected: [],
      pagination: {},
      headers: [
        {
          title: 'External Id',
          align: 'left',
          sortable: false,
          key: 'external_id',
          width: 90
        },
        {
          title: 'System From',
          align: 'right',
          sortable: true,
          key: 'system_from'
        },
        {
          title: 'System To',
          align: 'right',
          sortable: true,
          key: 'system_to'
        },
        {
          title: 'Shelf Side',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'side'
        },
        {
          title: 'Measure From',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'measure_from'
        },
        {
          title: 'Measure To',
          align: 'right',
          filterable: false,
          sortable: false,
          key: 'measure_to'
        },
        { title: '', key: 'actions', sortable: false }
      ],
      shelfDataEditedIndex: -1,
      shelfDataEditedItem: {},
      shelfDataToDelete: null,
      defaultItem: {
        bookshelf_id: null,
        external_id: null,
        id: null,
        measure_from: null,
        measure_to: null,
        section_child: null,
        section_id: null,
        section_main: null,
        side: 'L',
        system_from: null,
        system_to: null
      },
      deleteShelfDataConfirmMessage: 'Are you sure to delete this shelf data?'
    };
  },
  computed: {
    shelfListData () {
      const shelfStore = useShelfStore();
      const { data = [], total = 0 } = shelfStore.shelfData || {};

      this.total = total;

      return data;
    },
    noDataText () {
      const shelfStore = useShelfStore();
      if (shelfStore.selectedShelf) {
        return 'No shelf data found';
      }
      return 'No book shelf selected';
    },
    selectedShelf () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelf;
    },
    selectedShelfData () {
      const shelfStore = useShelfStore();
      return shelfStore.selectedShelfData;
    },
    shelfDataFormTitle () {
      return this.shelfDataEditedIndex === -1 ? 'New Shelf Data' : 'Edit Shelf Data';
    }
  },
  watch: {
    shelfDataAddEditDialog (val) {
      val || this.shelfDataAddEditDialogClose();
    }
  },
  methods: {
    loadShelfList (query) {
      const shelfStore = useShelfStore();
      return shelfStore.LOAD_BOOKSHELF_LIST(query);
    },
    deleteShelfData (shelfData) {
      const shelfStore = useShelfStore();
      return shelfStore.DELETE_SHELF_DATA(shelfData);
    },
    setSelectedShelfData (shelfData) {
      const shelfStore = useShelfStore();
      return shelfStore.SET_SELECTED_SHELF_DATA(shelfData);
    },
    onShelfDataClick (event, row) {
      this.setSelectedShelfData(row?.item ?? event);
    },
    addShelfData () {
      const { id: bookshelf } = this.selectedShelf;

      this.shelfDataEditedItem = Object.assign({
        bookshelf
      });

      this.shelfDataAddEditDialog = true;
    },

    editShelfData (shelfData) {
      this.shelfDataEditedIndex = this.shelfListData.indexOf(shelfData);
      this.shelfDataEditedItem = Object.assign({}, shelfData);
      this.shelfDataAddEditDialog = true;
    },

    deleteShelfDataItem (shelfData) {
      this.shelfDataToDelete = shelfData;
      this.showConfirmDeleteShelfData = true;
    },

    async confirmDeleteShelfData () {
      this.loading = true;

      await this.deleteShelfData(this.shelfDataToDelete);

      this.shelfDataToDelete = null;
      this.showConfirmDeleteShelfData = false;
      this.loading = false;
    },

    shelfDataAddEditDialogClose () {
      this.shelfDataAddEditDialog = false;
    }
  }
};
</script>

<style scoped>

</style>=
