import api from '~/util/api';

export const state = () => ({
  floors: []
});

export const mutations = {
  SET_FLOORS (state, floors) {
    state.floors = floors;
  }
};

export const actions = {
  async LOAD_FLOORS ({ commit }) {
    const response = await api.request({
      endPoint: 'floor/'
    }, {
      baseApiUrl: process.env.BASE_API_URL,
      token: process.env.TOKEN
    });
    commit('SET_FLOORS', response?.data?.results || []);
  }
};

export const getters = {
  floors: state => () => {
    return state.floors;
  },
  firstFloor: state => () => {
    return state.floors && state.floors.length ? state.floors[0].id : null;
  },
  getFloorName: state => (id) => {
    let name = '';
    const floor = state.floors.find(floor => floor.id === id);

    if (floor) {
      name = floor.short_name;
    }
    return name || id;
  }
};
