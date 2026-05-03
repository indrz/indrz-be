import { useUserStore } from '~/stores/user'
import LocalStorageService from '~/service/localStorage'

export default defineNuxtRouteMiddleware((to) => {
  const userStore = useUserStore()

  // Hydrate user store from sessionStorage if not already set
  if (!userStore.user) {
    const tokenData = LocalStorageService.getTokenData()
    if (tokenData && tokenData.token) {
      userStore.SET_USER(tokenData)
    }
  }

  const publicPages = ['/', '/de', '/en', '/admin/login']
  const isAdminRoute = to.path.startsWith('/admin')

  if (publicPages.includes(to.path)) {
    // If user is already signed in and visits login page, redirect to admin dashboard
    if (isAdminRoute && userStore.user) {
      return navigateTo('/admin')
    }
    return
  }

  // Protect admin routes — redirect to login if not authenticated
  if (isAdminRoute && !userStore.user) {
    return navigateTo(`/admin/login?redirect=${to.path}`)
  }
})
