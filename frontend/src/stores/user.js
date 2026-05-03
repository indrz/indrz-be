import { defineStore } from 'pinia'
import { useRouter } from '#app'
import { isNil } from 'lodash'
import UserService from '@/service/user'
import LocalStorageService from '@/service/localStorage'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),

  getters: {
    isUserSignedIn: (state) => !isNil(state.user),
    userEmail: (state) => (state.user ? state.user.username : '')
  },

  actions: {
    SET_USER(user) {
      this.user = user
      if (user) {
        LocalStorageService.setToken(this.user)
      } else {
        LocalStorageService.removeToken()
      }
    },

    async SIGN_IN(payload) {
      const userResponse = await UserService.signIn(payload)
      if (userResponse && userResponse.data) {
        this.SET_USER(userResponse.data)
      }
    },

    async SIGN_OUT() {
      const router = useRouter()
      this.SET_USER(null)
      await router.push('/admin/login')
    }
  }
})
