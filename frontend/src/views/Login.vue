<template>
  <div>
    <v-container style="margin-top: 150px">
      <v-row>
        <v-col class="col-lg-4 col-md-4 col-sm-5 mr-auto ml-auto">
          <v-card class="py-5 px-5" elevation="5">
            <div class="text-center">
              <span style="font-size: 25px">Login</span>
            </div>

            <!-- spinner -->
            <div v-if="spinner" class="text-center mt-5">
              <v-progress-circular
                :size="50"
                :width="5"
                color="grey darken-4"
                indeterminate
              >
              </v-progress-circular>
            </div>
            <!-- end spinner -->

            <!-- error text -->
            <div
              v-if="showError"
              id="error-text"
              class="red darken-3 text-center py-3 my-3"
            >
              <span style="font-size: 16px" id="text" class="white--text">{{
                errorText
              }}</span>
            </div>
            <!-- end error text -->

            <form v-if="showForm" @submit.prevent="login()">
              <v-text-field
                id="username"
                label="Username"
                v-model="username"
                required
              >
              </v-text-field>
              <v-text-field
                id="password"
                type="password"
                v-model="password"
                label="Password"
                required
              >
              </v-text-field>
              <v-btn type="submit" class="grey darken-4 white--text col-12"
                >Login</v-btn
              >
            </form>

            <div class="text-center mt-5">
              <small
                @click="$router.push({ name: 'Register' })"
                id="create-new-account"
                >create new account</small
              >
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require("axios");
import store from "../store/index";

export default {
  name: "Login",
  data() {
    return {
      username: null,
      password: null,

      spinner: false,
      showForm: true,
      showError: false,
      errorText: null,
    };
  },
  created() {
    this.$store.commit("changeShowLogin", false);
  },
  beforeRouteLeave: (to, from, next) => {
    store.commit("changeShowLogin", true);
    next();
  },
  methods: {
    displayError(text) {
      this.spinner = false;
      this.showForm = true;
      this.showError = true;
      this.errorText = text;
    },
    login() {
      this.showForm = false;
      this.spinner = true;
      this.showError = false;

      setTimeout(() => {
        axios
          .post("http://localhost:8000/api/user/token/", {
            username: this.username,
            password: this.password
          })
          .then((response) => {
            this.$store.commit("getUserInfo", response.data)
            var url = this.$store.state.currentUrl
            this.$store.commit("deleteCurrentUrl")
            this.$router.push(`${url}`)
          })
          .catch(() => {
            this.displayError("Username or password is incorrect")
          });
      }, 1000);
    },
  },
};
</script>

<style scoped>
#create-new-account {
  cursor: pointer;
}
#create-new-account:hover {
  color: rgb(72, 72, 255);
}
</style>