<template>
  <v-app>
    <v-app-bar app class="grey darken-4">
      <div class="d-flex align-center" @click="$router.push({ name: 'Home' })">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>
      <div class="d-flex align-center col-6">
        <v-autocomplete
          dark
          class="mt-5"
          :items="searchAutoCompleteResults"
          @change="searchResultClick($event)"
          label="Search Videos"
          autocomplete="off"
          @keyup="searchAutoComplete"
        >
        </v-autocomplete>
        <v-btn class="px-2" @click="searchButton()">Search</v-btn>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        v-if="
          $store.state.userInfo.access == null && $store.state.showLogin == true
        "
        text
        @click="loginClick()"
      >
        <span class="mr-2 white--text">Login</span>
      </v-btn>

      <v-menu offset-y v-if="$store.state.userInfo.access != null">
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" text v-on="on" @click="hasNotification = false">
            <v-badge v-if="hasNotification" color="error" overlap>
              <span class="mr-2 white--text">Notifications</span>
            </v-badge>
            <span v-else class="mr-2 white--text">Notifications</span>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="notification in notifications"
            :key="notification.id" class="notification-content"
            @click="goToVideoInNotification(notification.url)"
          >
            <span style="cursor: pointer">{{ notification.content }}</span>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-menu offset-y v-if="$store.state.userInfo.access != null">
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" text v-on="on">
            <span class="mr-2 white--text">{{
              $store.state.userInfo.username
            }}</span>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          <v-list-item
            id="upload"
            @click="
              $router.push({
                name: 'UploadVideo',
                params: { id: $store.state.userInfo.id },
              })
            "
          >
            <v-list-item-title>Upload video</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn v-if="$store.state.userInfo.access != null" text @click="logout()">
        <span class="mr-2 white--text">Logout</span>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "App",

  data: () => ({
    searchText: "",
    showResult: false,
    text: null,
    searchAutoCompleteResults: [],
    hasNotification: false,
    notifications: [],

    notificationWebSocket: null,
  }),
  created: function () {
    var self = this
    if (this.$store.state.userInfo.access != null) {
      this.queryNotification();

      this.notificationWebSocket = new WebSocket(
        "ws://localhost:8000/ws/notification/notificationWebSocket/"
      );
      this.notificationWebSocket.onmessage = function (event) {
        
        self.notifications.unshift(JSON.parse(event.data)['message'])
        if (parseInt(JSON.parse(event.data)['message']['user_id']) === parseInt(self.$store.state.userInfo.id)) {
          self.hasNotification = true
        }
      };
      this.notificationWebSocket.onclose = function () {
        console.log("web socket closed");
      };
    }
  },
  methods: {
    loginClick: function () {
      this.$store.commit("getCurrentUrl", this.$route.path);
      this.$router.push({ name: "Login" });
    },
    logout: function () {
      this.$store.commit("deleteUserInfo");
      window.location.reload();
    },
    fireSearchAutoCompleteRequest: function (text) {
      axios
        .get("http://localhost:8000/search-autocomplete/", {
          params: {
            searchText: text,
          },
        })
        .then((response) => {
          this.searchAutoCompleteResults = response.data["results"];
        });
    },
    searchAutoComplete: async function (event) {
      if (event.keyCode === 13) {
        this.searchResultClick(event.target.value);
      } else {
        await this.fireSearchAutoCompleteRequest(event.target.value);
        this.text = event.target.value;
      }
    },
    searchResultClick: function (event) {
      this.$router.push({ name: "SearchResult", query: { search: event } });
      window.location.reload();
    },
    searchButton: function () {
      this.searchResultClick(this.text);
    },
    queryNotification: function () {
      var userId = this.$store.state.userInfo.id;

      axios
        .get(`http://localhost:8000/get-notifications/${userId}/`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.userInfo.access}`,
          },
        })
        .then((response) => {
          this.notifications = response.data["notifications"];
        });
    },
    goToVideoInNotification: function (path) {
      this.$router.push({ path: path })
      window.location.reload()
    }
  },
};
</script>

<style scoped>
#upload {
  cursor: pointer;
}
#upload:hover {
  background-color: rgb(226, 226, 226);
}
.notification-content:hover {
  cursor: pointer;
  background-color: rgb(221, 221, 221)
}
</style>