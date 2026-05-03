/* eslint-disable */

<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" class="d-flex justify-center">
        <span class="v-card__title">Welcome to the INDRZ Admin</span>
      </v-col>
    </v-row>
    <br>
    <span class="v-card__text">Please login</span>

    <v-form
      ref="loginForm"
      v-model="valid"
      @submit.prevent="onSignIn"
      lazy-validation
    >
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              key="login-username"
              v-model="username"
              :rules="[formRules.required]"
              name="username"
              label="User Name"
              prepend-icon="mdi-account"
              required
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              key="login-password"
              v-model="password"
              :rules="[formRules.required]"
              name="password"
              label="Password"
              prepend-icon="mdi-lock"
              type="password"
              required
            />
          </v-col>
        </v-row>
        <v-row v-if="noUser" class="justify-center">
          <v-col cols="12" class="text-subtitle-2 text-error text-center">
            User name or password is not valid!
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn :disabled="!valid" type="submit" block color="primary">
              Login
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
    <div class="mt-20" />
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-btn @click="onSignInWithSAML" block variant="plain" color="primary">
            SSO Login
            <v-icon end>
              mdi-cloud
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup>
import { useUserStore } from '~/stores/user'

definePageMeta({
  layout: 'admin'
})

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const loginForm = ref(null)

const username = ref('')
const password = ref('')
const valid = ref(true)
const noUser = ref(false)
const samlLogin = ref(false)
const formRules = {
  required: value => !!value || 'This is a required field.'
}

onBeforeMount(async () => {
  const sessionId = /SESS\w*=([^;]+)/i.test(document.cookie) ? RegExp.$1 : false
  if (sessionId) {
    window.location.href = '/saml/login/'
  }
})

onMounted(() => {
  // User store hydration from sessionStorage is handled by auth.global middleware.
  // If already signed in, redirect away from login page.
  if (!samlLogin.value && userStore.isUserSignedIn) {
    router.push(route.query.redirect || '/admin')
  }
})

async function onSignIn () {
  const result = await loginForm.value.validate()
  const isValid = typeof result === 'object' ? result.valid : result
  if (!isValid) {
    return
  }
  try {
    await userStore.SIGN_IN({
      username: username.value,
      password: password.value
    })
    if (userStore.isUserSignedIn) {
      router.push(route.query.redirect || '/admin')
      noUser.value = false
      return
    }
    noUser.value = true
  } catch (error) {
    console.log(error.message)
  }
}

function onSignInWithSAML () {
  window.location.href = '/saml/login/'
}
</script>

<style scoped>

</style>
