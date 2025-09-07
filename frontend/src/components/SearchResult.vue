<template>
  <div id="search-result-list" class="list-group">
    <div v-if="!searchResult.length">
      <span>{{ no_results_found }}</span>
    </div>
    <template v-for="(result, i) in searchResult">
      <span :key="i" v-html="result.html" />
    </template>
  </div>
</template>

<script>
export default {
  name: 'SearchResult',
  props: {
    searchResult: {
      type: Array,
      default: function () {
        return [];
      }
    }
  },
  data () {
    return {
      no_results_found: this.$t('no_result_found')
    };
  },
  methods: {
  }
};
</script>
<style>
  a.list-group-item {
    color: #555 !important;
    text-decoration: none;
    font-size: 14px;
    color: #000 !important;
  }
  a.list-group-item:hover {
    background-color: #f3f3f3;
  }
  .badge {
    display: inline-block;
    min-width: 10px;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 700;
    line-height: 1;
    color: #fff;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    background-color: #777;
    border-radius: 10px;
  }
  .list-group-item:first-child {
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }
  a.list-group-item {
    color: #555;
  }
  .list-group-item {
    display: block;
    padding: 5px 1px !important;
    background-color: transparent;
    border: transparent;
    margin: 0;
  }
  .list-group-item {
    position: relative;
    display: block;
    padding: 10px 15px;
    margin-bottom: -1px;
    background-color: #fff;
    border: 1px solid #ddd;
  }
</style>
