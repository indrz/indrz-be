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
      v-model:selected="selected"
      v-model:active="active"
      :items="poiData"
      item-value="id"
      class="poi no-checkbox"
      density="compact"
      style="overflow: auto; width: auto;"
      select-strategy="classic"
      selectable
    >
      <template v-slot:title="{ item }">
        <span style="white-space: normal" @click="onTreeClick(getTreeItem(item))">
          {{ getItemLabel(item) }}
        </span>
      </template>

      <template v-slot:prepend="{ item }">
        <div @click="onTreeClick(getTreeItem(item))">
          <img
            v-if="getTreeItem(item).icon && isTreeItemActive(item)"
            :src="getTreeItem(item).icon"
            style="height:25px;"
          >
          <img
            v-else-if="getTreeItem(item).icon"
            :src="setInactiveName(getTreeItem(item).icon)"
            style="height:25px;"
          >
        </div>
      </template>
    </v-treeview>
  </div>
</template>

<script>
import _ from 'lodash';
import { usePoiStore } from '~/stores/poi';
import bus from '~/util/bus';

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
      selected: [],
      active: [],
      loading: true,
      currentPoi: null
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
    activeIdSet () {
      return new Set(
        (Array.isArray(this.active) ? this.active : [])
          .map(Number)
          .filter(Number.isFinite)
      );
    }
  },

  watch: {
    selected: {
      deep: true,
      handler (newSelected, oldSelected) {
        const next = Array.isArray(newSelected) ? newSelected.map(v => Number(v)).filter(Number.isFinite) : [];
        const prev = Array.isArray(oldSelected) ? oldSelected.map(v => Number(v)).filter(Number.isFinite) : [];

        // Single-select mode: keep only the last selected id.
        if (this.multi === false && next.length > 1) {
          const last = next[next.length - 1];
          this.selected = [last];
          this.active = [last];
          return;
        }

        const removedIds = _.difference(prev, next);
        const newIds = _.difference(next, prev);
        const oldIds = _.intersection(next, prev);

        const toNode = (id) => {
          const found = this.findNode(id);
          return found?.data || found || null;
        };

        bus.emit('poiLoad', {
          newItems: newIds.map(toNode).filter(Boolean),
          oldItems: oldIds.map(toNode).filter(Boolean),
          removedItems: removedIds.map(toNode).filter(Boolean)
        });
      }
    }
  },

  mounted () {
    this.loadDataToPoiTree();
  },

  methods: {
    getTreeItem (item) {
      return item && item.raw ? item.raw : item;
    },
    isTreeItemActive (item) {
      const id = Number(this.getTreeItem(item)?.id);
      return Number.isFinite(id) && this.activeIdSet.has(id);
    },
    getItemLabel (item) {
      const data = this.getTreeItem(item)
      const locale = this.currentLocale || 'en'
      return (
        data?.[`name_${locale}`] ||
        data?.name_en ||
        data?.name_de ||
        data?.name ||
        data?.title ||
        data?.label ||
        data?.text ||
        ''
      )
    },
    async loadPOI () {
      const poiStore = usePoiStore();
      await poiStore.LOAD_POI();
    },

    async loadDataToPoiTree () {
      try {
        await this.loadPOI();
        if (Array.isArray(this.initialPoiCatId) && this.initialPoiCatId.length) {
          // Capture the value now since the parent may reset it to null before the timeout fires
          const catIds = [...this.initialPoiCatId];
          setTimeout(() => {
            catIds.forEach(catId => this.loadInitialPOICategory(catId));
          }, 1000)
        } else if (this.initialPoiId) {
          // Capture the value now since the parent may reset it to null before the timeout fires
          const poiId = this.initialPoiId;
          setTimeout(() => {
            this.$emit('loadSinglePoi', poiId);
          }, 500);
        }
      } catch (e) {
        console.error('Failed to load POI tree:', e);
      } finally {
        this.loading = false;
      }
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
      const node = foundData?.data || foundData;
      const nodeId = Number(node?.id);
      if (!Number.isFinite(nodeId)) return;

      // Open ancestors (best-effort): v-treeview will generally reflect active selections even if closed.
      // We keep behavior consistent by activating/selecting the category and its children.
      const idsToSelect = [nodeId];
      if (Array.isArray(node?.children)) {
        node.children.forEach((child) => {
          const childId = Number(child?.id);
          if (Number.isFinite(childId)) idsToSelect.push(childId);
        });
      }

      const merged = _.uniq([...(Array.isArray(this.selected) ? this.selected : []), ...idsToSelect]);
      this.selected = merged;
      this.active = _.uniq([...(Array.isArray(this.active) ? this.active : []), nodeId]);

      // Ensure the same side effects as a user click (e.g. emitting selectPoiCategory)
      this.onTreeClick(foundData, true);
    },

    onTreeClick (node, forceSelect = false) {
      const rawNode = node?.data ? node.data : node;
      const handler = rawNode?.children ? this.onTreeParentNodeClick : this.onLeafNodeClick;
      handler(rawNode, forceSelect);
    },

    onLeafNodeClick (node, forceSelect = false) {
      const nodeId = Number(node?.id);
      if (!Number.isFinite(nodeId)) return;

      const selectedNow = Array.isArray(this.selected) ? this.selected.map(Number) : [];
      const shouldAdd = forceSelect ? true : !selectedNow.includes(nodeId);

      if (!this.multi) {
        this.removeAllSelections();
      }

      this.selected = shouldAdd
        ? _.uniq([...selectedNow, nodeId])
        : selectedNow.filter(id => id !== nodeId);

      const activeNow = Array.isArray(this.active) ? this.active.map(Number) : [];
      this.active = shouldAdd
        ? _.uniq([...activeNow, nodeId])
        : activeNow.filter(id => id !== nodeId);

      this.currentPoi = shouldAdd ? (node.children || [node]) : [];
      this.$emit('selectPoiCategory', shouldAdd ? this.currentPoi[0] : null);
    },

    onTreeParentNodeClick (node, forceSelect = false) {
      const nodeId = Number(node?.id);
      if (!Number.isFinite(nodeId)) return;

      const children = Array.isArray(node?.children) ? node.children : [];
      const childIds = children
        .map((c) => Number(c?.id))
        .filter(Number.isFinite);

      if (!childIds.length) return;

      const selectedNow = Array.isArray(this.selected) ? this.selected.map(Number) : [];
      const activeNow = Array.isArray(this.active) ? this.active.map(Number) : [];

      // Parent click behavior:
      // - If any child is unselected -> select all children
      // - If all children are selected -> deselect all children
      const allChildrenSelected = childIds.every(id => selectedNow.includes(id));
      const shouldAdd = forceSelect ? true : !allChildrenSelected;

      // Toggle parent selection highlight too (useful since checkboxes are hidden).
      if (shouldAdd) {
        this.selected = _.uniq([...selectedNow, nodeId]);
      } else {
        this.selected = selectedNow.filter(id => id !== nodeId);
      }

      // Selecting a parent selects/deselects its direct children.
      children.forEach((childNode) => this.onLeafNodeClick(childNode, shouldAdd));

      // Keep parent active state in sync.
      this.active = shouldAdd
        ? _.uniq([...activeNow, nodeId])
        : activeNow.filter(id => id !== nodeId);
    },

    onLocationClick (location) {
      this.$emit('locationClick', location.centroid);
    },

    removeAllSelections () {
      this.selected = [];
      this.active = [];
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
