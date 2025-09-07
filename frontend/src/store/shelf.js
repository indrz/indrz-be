import api from '@/util/api';

const bookShelfEndpoint = `bookway/bookshelf/`;
const shelfDataEndpoint = `/shelfdata/`;

const initialShelves = {
  data: [],
  total: 0
};
const initialShelfData = {
  data: [],
  total: 0
};

export const state = () => ({
  shelves: initialShelves,
  shelfData: initialShelfData,
  selectedShelf: null,
  selectedShelfData: null,
  lastShelfQuery: null
});

export const mutations = {
  setShelves (state, { data = [], total = 0 }) {
    state.shelves = { data, total };
  },
  setSelectedShelf (state, shelf) {
    state.selectedShelf = shelf;
  },
  setShelfData (state, shelfData) {
    state.shelfData = shelfData;
  },
  setSelectedShelfData (state, shelfData) {
    state.selectedShelfData = shelfData;
  },
  setLastShelfQuery (state, query) {
    state.lastShelfQuery = query;
  }
};

export const actions = {
  async LOAD_BOOKSHELF_LIST ({ commit }, query) {
    const urlWithParams = api.getURLParamsFromPayLoad(query);

    const { data } = await api.request({
      endPoint: `${bookShelfEndpoint}${urlWithParams}`
    });

    const shelfListData = {
      data: data.results.features,
      total: data.count
    };
    commit('setLastShelfQuery', query);
    commit('setShelves', shelfListData);
    commit('setShelfData', initialShelfData);
    commit('setSelectedShelf', null);
  },

  async SET_SELECTED_SHELF ({ commit }, shelf) {
    commit('setSelectedShelf', shelf);

    if (!shelf) {
      commit('setShelfData', initialShelfData);
      return;
    }
    const shelfData = await api.request({
      endPoint: `${bookShelfEndpoint}${shelf.id}${shelfDataEndpoint}`
    });

    commit('setShelfData', shelfData);
  },
  SET_SELECTED_SHELF_DATA ({ commit }, shelfData) {
    commit('setSelectedShelfData', shelfData);
  },

  async SAVE_SHELF ({ state, commit, dispatch }, data) {
    let apiRequest = api.postRequest;
    let endPoint = bookShelfEndpoint;

    if (data.id) {
      apiRequest = api.putRequest;
      endPoint = `${bookShelfEndpoint}${data.id}/`
    }

    const response = await apiRequest({
      data: data,
      endPoint
    });

    await dispatch('LOAD_BOOKSHELF_LIST', state.lastShelfQuery);

    return response.data;
  },

  async DELETE_SHELF ({ state, commit, dispatch }, data) {
    const response = await api.postRequest({
      endPoint: `${bookShelfEndpoint}${data.id}/`,
      method: 'DELETE',
      data: {}
    });

    await dispatch('LOAD_BOOKSHELF_LIST', state.lastShelfQuery);

    return response.data;
  },

  async SAVE_SHELF_DATA ({ state, commit, dispatch }, data) {
    let apiRequest = api.postRequest;
    let endPoint = shelfDataEndpoint;

    if (data.id) {
      apiRequest = api.putRequest;
      endPoint = `${shelfDataEndpoint}${data.id}/`
    }

    const response = await apiRequest({
      data: data,
      endPoint: `bookway${endPoint}`
    });

    await dispatch('SET_SELECTED_SHELF', state.selectedShelf);

    return response.data;
  },

  async DELETE_SHELF_DATA ({ state, commit, dispatch }, data) {
    const response = await api.postRequest({
      endPoint: `bookway${shelfDataEndpoint}${data.id}/`,
      method: 'DELETE',
      data: {}
    });

    await dispatch('SET_SELECTED_SHELF', state.selectedShelf);

    return response.data;
  }
};

export const getters = {};
