<template>
  <div>
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
      v-model="tree"
      :multiple-active="multi"
      :items="poiData"
      selected-color="indigo"
      selectable
      return-object
      item-key="id"
      class="poi no-checkbox"
      dense
      style="overflow: auto; width: auto;"
    >
      <template v-slot:label="{ item }">
        <span style="white-space: normal" @click="onTreeClick(item)">
          {{ item['name_' + $i18n.locale] }}
        </span>
      </template>
      <template v-slot:prepend="{ item, active }">
        <div @click="onTreeClick(item)">
          <img v-if="active" :src="item.icon" style="height:25px;">
          <img v-else :src="setInactiveName(item.icon)" style="height:25px;">
        </div>
      </template>
    </v-treeview>
  </div>
</template>

<script>
import _ from 'lodash';
import { mapActions, mapState, mapGetters } from 'vuex';

export default {
  name: 'PointsOfInterest',
  props: {
    initialPoiCatId: {
      type: Array,
      default: function () {
        return [];
      }
    },
    initialPoiId: {
      type: String,
      default: function () {
        return null;
      }
    },
    multi: {
      type: Boolean,
      default: function () {
        return true;
      }
    }
  },
  data () {
    return {
      files: {
        html: 'mdi-language-html5',
        js: 'mdi-nodejs',
        json: 'mdi-json',
        md: 'mdi-markdown',
        pdf: 'mdi-file-pdf',
        png: 'mdi-file-image',
        txt: 'mdi-file-document-outline',
        xls: 'mdi-file-excel'
      },
      tree: [],
      openedItems: [],
      forceReloadNode: false,
      loading: true,
      currentPoi: null
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
    }
  },

  watch: {
    tree (newSelections, oldSelections) {
      let removedItems = [];
      let newItems = [];
      let oldItems = [];

      if (this.multi === false) {
        removedItems = oldSelections;
        newItems = this.currentPoi;
        newSelections = [newSelections[newSelections.length - 1]];
      } else {
        if (oldSelections.length > newSelections.length) {
          removedItems = _.differenceBy(oldSelections, newSelections, 'id');
        }
        if (newSelections.length > oldSelections.length) {
          newItems = _.differenceBy(newSelections, oldSelections, 'id');
        }
        oldItems = _.intersectionBy(newSelections, oldSelections, 'id');
      }

      if (
        this.forceReloadNode &&
        newSelections.length === oldSelections.length &&
        newSelections[0].id === oldSelections[0].id) {
        newItems = newSelections;
        removedItems = newSelections;
        oldItems = [];
        this.forceReloadNode = false;
      }
      this.$root.$emit('poiLoad', {
        newItems,
        oldItems,
        removedItems
      });
    }
  },

  mounted () {
    this.loadDataToPoiTree();
  },

  methods: {
    ...mapActions({
      loadPOI: 'poi/LOAD_POI'
    }),

    async loadDataToPoiTree () {
      await this.loadPOI();
      if (this.initialPoiCatId) {
        setTimeout(() => {
          this.initialPoiCatId.forEach(catId => this.loadInitialPOICategory(catId));
        }, 1000)
      } else if (this.initialPoiId) {
        setTimeout(() => {
          this.$emit('loadSinglePoi', this.initialPoiId);
        }, 500);
      }
      this.loading = false;
    },
    setInactiveName (name) {
      const splitName = name.split('/');
      const oldName = splitName.pop();
      const newName = 'Inactive_' + oldName;
      splitName.push(newName)
      return splitName.join('/')
    },
    loadInitialPOICategory (catId) {
      const foundData = this.findNode(catId);

      if (!foundData) {
        this.loading = false;
        return;
      }
      this.tree = [foundData.data];
      const treeComp = this.treeComp;

      if (foundData && foundData.roots) {
        foundData.roots.reverse().forEach((node) => {
          treeComp.updateOpen(node, true);
        });
      }

      treeComp.updateOpen(catId, true);

      if (foundData?.data?.children) {
        foundData.data.children.forEach((child) => {
          treeComp.updateActive(child.id, true);
          treeComp.updateSelected(child.id, true);
        });
      }

      treeComp.updateActive(catId, true);
      treeComp.updateSelected(catId, true);
      this.onTreeClick(foundData, true)
    },

    onTreeClick (node, forceSelect = false) {
      const treeComp = this.$refs.poi;
      const handler = node.children ? this.onTreeParentNodeClick : this.onLeafNodeClick;

      handler(node, treeComp, forceSelect);
    },

    onLeafNodeClick (node, treeComp, forceSelect = false) {
      node = node?.data ? node.data : node;
      const shouldAdd = (!forceSelect ? !treeComp.selectedCache.has(node.id) : forceSelect);

      if (!this.multi) {
        this.removeAllSelections(treeComp);
      }

      treeComp.updateSelected(node.id, shouldAdd);
      treeComp.updateActive(node.id, shouldAdd);

      this.currentPoi = shouldAdd ? (node.children || [node]) : [];

      this.$emit('selectPoiCategory', shouldAdd ? this.currentPoi[0] : null);
      treeComp.emitSelected();
    },

    onTreeParentNodeClick (node, treeComp) {
      if (!treeComp.nodes[node.id].parent) {
        this.expandCollapseNode(node.id, treeComp);
        return;
      }

      if (!treeComp.nodes[node.id].isOpen) {
        this.expandCollapseNode(node.id, treeComp);
      }
      const shouldAdd = !treeComp.activeCache.has(node.id);

      node.children.forEach(childNode => this.onLeafNodeClick(childNode, treeComp, shouldAdd));

      treeComp.updateActive(node.id, (this.multi === false ? true : shouldAdd));

      treeComp.emitActive();
    },

    expandCollapseNode (nodeId, treeComp) {
      const isOpened = treeComp.nodes[nodeId].isOpen;
      treeComp.updateOpen(nodeId, !isOpened);
      treeComp.emitOpen();
    },

    onLocationClick (location) {
      this.$emit('locationClick', location.centroid);
    },

    removeAllSelections (treeComp) {
      treeComp.selectedCache.forEach((nodeId) => {
        treeComp.updateSelected(nodeId, false);
      });
      treeComp.activeCache.forEach((nodeId) => {
        treeComp.updateActive(nodeId, false);
      });
    }
  }
};
</script>

<style>
.poi {
  font-size: 0.875rem;
}
.no-checkbox .v-treeview-node__checkbox {
  display: none !important;
}
</style>
