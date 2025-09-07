<template>
  <div>
    <v-card>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="shelfListData"
        :server-items-length="total"
        :single-select="singleSelect"
        :loading="loading"
        :height="height"
        :no-data-text="noDataText"
        @click:row="onShelfDataClick"
        item-key="id"
        dense
        class="elevation-1"
        loading-text="Loading... Please wait"
        items-per-page="-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Shelf Data</v-toolbar-title>
            <v-spacer />
            <v-btn
              :disabled="!selectedShelf || shelfDataAddEditDialog"
              @click="addShelfData"
              outlined
            >
              <v-icon left>
                mdi-plus
              </v-icon>
              Shelf Data
            </v-btn>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            @click="editShelfData(item)"
            small
            class="mr-1"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            @click="showConfirmDeleteShelfData = true"
            small
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
      <add-edit-shelf-data
        :title="shelfDataFormTitle"
        :dialog="shelfDataAddEditDialog"
        :current-shelf-data="shelfDataEditedItem"
        @close="shelfDataAddEditDialogClose"
      />
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
import { mapState, mapActions } from 'vuex';
import ConfirmDialog from '@/components/ConfirmDialog';
import AddEditShelfData from '@/components/admin/shelves/AddEditShelfData';

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
          text: 'External Id',
          align: 'left',
          sortable: false,
          value: 'external_id',
          width: 90
        },
        {
          text: 'System From',
          align: 'right',
          sortable: true,
          value: 'system_from'
        },
        {
          text: 'System To',
          align: 'right',
          sortable: true,
          value: 'system_to'
        },
        {
          text: 'Shelf Side',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'side'
        },
        {
          text: 'Measure From',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'measure_from'
        },
        {
          text: 'Measure To',
          align: 'right',
          filterable: false,
          sortable: false,
          value: 'measure_to'
        },
        { text: '', value: 'actions', sortable: false }
      ],
      shelfDataEditedIndex: -1,
      shelfDataEditedItem: {},
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
    ...mapState({
      shelfListData: function (state) {
        const { data, total } = state.shelf.shelfData;

        this.total = total;

        return data;
      },
      noDataText: (state) => {
        if (state.shelf.selectedShelf) {
          return 'No shelf data found';
        }
        return 'No book shelf selected';
      },
      selectedShelf: state => state.shelf.selectedShelf,
      selectedShelfData: state => state.shelf.selectedShelfData
    }),
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
    ...mapActions({
      loadShelfList: 'shelf/LOAD_BOOKSHELF_LIST',
      deleteShelfData: 'shelf/DELETE_SHELF_DATA',
      setSelectedShelfData: 'shelf/SET_SELECTED_SHELF_DATA'
    }),
    onShelfDataClick (data) {
      this.setSelectedShelfData(data);
    },
    onShelfClick (shelf) {
      this.setSelectedShelf(shelf);
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

    async confirmDeleteShelfData () {
      this.loading = true;

      await this.deleteShelfData(this.selectedShelfData);

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
