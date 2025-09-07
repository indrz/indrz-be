import { isNil } from 'lodash';
import UserService from '@/service/user';
import LocalStorageService from '@/service/localStorage';

export const state = () => ({
  user: null
});

export const mutations = {
  SET_USER (state, user) {
    state.user = user;
    if (user) {
      LocalStorageService.setToken(state.user);
    } else {
      LocalStorageService.removeToken();
    }
  }
};

export const actions = {
  async SIGN_IN ({ commit }, payload) {
    const userResponse = await UserService.signIn(payload);
    if (userResponse && userResponse.data) {
      commit('SET_USER', userResponse.data);
    }
  },

  SIGN_OUT ({ commit }) {
    commit('SET_USER', null);
    this.$router.push('/admin/login');
  }
};

export const getters = {
  isUserSignedIn (state) {
    return !isNil(state.user);
  },
  userEmail (state) {
    return state.user ? state.user.username : ''
  }
};
