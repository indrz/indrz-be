/* eslint-disable */

<template>
  <v-container xs12>
    <v-row
      align="center"
      justify="center"
    >
      <span class="v-card__title">Welcome to the INDRZ Admin</span>
    </v-row>
    <br>
    <span class="v-card__text">Please login</span>

    <template>
      <v-form
        ref="loginForm"
        v-model="valid"
        @submit.prevent="onSignIn"
        lazy-validation
      >
        <v-container>
          <v-layout row wrap>
            <v-flex xs12 sm6>
              <v-text-field
                key="login-username"
                v-model="username"
                :rules="[formRules.required]"
                name="username"
                label="User Name"
                prepend-icon="mdi-account"
                required
              />
            </v-flex>

            <v-flex xs12 sm6>
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
            </v-flex>
          </v-layout>
          <v-layout v-if="noUser" row wrap class="subheader-2 justify-center error--text">
            User name or password is not valid!
          </v-layout>
          <v-layout row wrap>
            <v-btn :disabled="!valid" type="submit" block color="primary">
              Login
            </v-btn>
          </v-layout>
        </v-container>
      </v-form>
      <div class="mt-20" />
      <v-container>
        <v-layout row wrap>
          <v-btn @click="onSignInWithSAML" block color="plain">
            SSO Login
            <v-icon
              right
              dark
            >
              mdi-cloud
            </v-icon>
          </v-btn>
        </v-layout>
      </v-container>
    </template>
  </v-container>
</template>

<script>
import axios from 'axios';
import LocalStorageService from '../../service/localStorage';
export default {
  name: 'Login',
  layout: 'admin',
  data () {
    return {
      username: '',
      password: '',
      valid: true,
      noUser: false,
      saml_login: false,
      formRules: {
        required: value => !!value || 'This is a required field.'
      }
    };
  },
  // Replace "http://127.0.0.1:8000"
  async beforeMount () {
    const sessionId = /SESS\w*=([^;]+)/i.test(document.cookie) ? RegExp.$1 : false;
    if (sessionId) {
      this.saml_login = true
      const data = { 'token': sessionId }
      await axios.post('/session_user/', data)
        .then((response) => {
          sessionStorage.setItem('indrz-frontend', JSON.stringify(response.data));
          document.cookie.split(';').forEach(function (c) { document.cookie = c.replace(/^ +/, '').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/'); });
        });
      axios.post('/session_user_logout/', data)
      console.log('1')
      const tokenData = LocalStorageService.getTokenData();
      if (tokenData && tokenData.token) {
        this.$store.commit('user/SET_USER', tokenData);
        this.$router.push(this.$route.query.redirect || '/admin');
      }
      this.saml_login = false
    }
  },

  mounted () {
    if (!this.saml_login) {
      console.log('n')
      const tokenData = LocalStorageService.getTokenData();
      if (tokenData && tokenData.token) {
        this.$store.commit('user/SET_USER', tokenData);
        this.$router.push(this.$route.query.redirect || '/admin');
      }
    }
  },

  methods: {
    async onSignIn () {
      if (!this.$refs.loginForm.validate()) {
        return;
      }
      try {
        await this
          .$store
          .dispatch('user/SIGN_IN', {
            username: this.username,
            password: this.password
          });
        if (this.$store.getters['user/isUserSignedIn']) {
          this.$router.push(this.$route.query.redirect || '/admin');
          this.noUser = false;
          return;
        }
        this.noUser = true;
      } catch (error) {
        console.log(error.message);
      }
    },
    // Replace "http://127.0.0.1:8000"
    onSignInWithSAML () {
      const linkLs = '/saml/login/'
      window.location.href = linkLs
    }
  }
};
</script>

<style scoped>

</style>
