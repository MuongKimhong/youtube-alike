<template>
  <div>
    <v-container style="margin-top: 150px">
      <v-row>
        <v-col class="col-lg-4 col-md-5 col-sm-6 mr-auto ml-auto">
          <v-card class="py-5 px-5" elevation="5">
            <div class="text-center">
              <span style="font-size: 25px">Register</span>
            </div>

            <!-- spinner -->
            <div v-if="spinner" class="text-center mt-5">
                <v-progress-circular :size="50" :width="5" color="grey darken-4" indeterminate>
                </v-progress-circular>
            </div>
            <!-- end spinner -->

            <!-- error text -->
            <div v-if="showError" id="error-text" class="red darken-3 text-center py-3 my-3">
                <span style="font-size: 16px" id="text" class="white--text">{{ errorText }}</span>
            </div>
            <!-- end error text -->

            <form v-if="showForm" @submit.prevent="register()">
              <v-text-field id="username" label="Username" v-model="username" required>
              </v-text-field>
              <v-text-field id="password1" type="password" label="Password" v-model="password1" required>
              </v-text-field>
              <v-text-field id="password2" type="password" label="Confirm password" v-model="password2" required>
              </v-text-field>
              <v-btn type="submit" class="grey darken-4 white--text col-12">Register</v-btn>

              <div class="text-center mt-5">
                <small @click="$router.push({ name: 'Login' })" id="login-account">login with existing account</small>
            </div>
            </form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require('axios')
import store from '../store/index'

export default {
  name: "Register",
  data() {
    return {
      username: null,
      password1: null,
      password2: null,

      spinner: false,
      showForm: true,
      showError: false,
      errorText: null
    };
  },
  created() {
    this.$store.commit('changeShowLogin', false)
  },
  beforeRouteLeave: (to, from, next) => {
      store.commit('changeShowLogin', true)
      next()
  },
  methods: {
      displayError(text) {
            this.spinner = false
            this.showForm = true
            this.showError = true
            this.errorText = text
      },
      register() {
          this.showForm = false
          this.spinner = true
          this.showError = false

          if (this.password1 != this.password2) {
            this.displayError("Two password didn't match")
            return;
          }
          setTimeout(() => {
              axios.post('http://localhost:8000/create-account/', {
                  username: this.username,
                  password: this.password1
              })
              .then((response) => {
                  if (response.data.success) this.$router.push({ name: 'Login' })
              })
              .catch((error) => {
                  var text = error.response.data['usernameTaken']
                  this.displayError(text)
              })
          }, 1000)
      }
  }
};
</script>

<style scoped>
#login-account {
    cursor: pointer
}
#login-account:hover {
    color: rgb(72, 72, 255)
}
</style>