<template>
  <div class="home">
    <v-container>
      <v-row>
        <v-col cols=12 class="col-lg-3 col-md-4 col-sm-6 mt-4" v-for="video in videos" :key="video.id">
          <v-card flat class="grey lighten-1 card-video pb-3" @click="viewVideo(video.id, video.complex, video.slug, video.tag_ids)">
            <img :src="video.thumbnail" width="100%" height="200px" alt="">
            <h4 class="px-2 py-2">{{ video.title }}</h4>
            <small class="ml-2 mr-2">{{ video.views }} views | {{ video.uploaderName }}</small>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  name: 'Home',
  data() {
    return {
      videos: []
    }
  },
  created() {
    if(this.$store.state.userInfo.access != null) this.getRandomVideosBasedOnUser()
    else this.getRandomVideos()
  },
  methods: {
    getRandomVideos: function () {
      axios.get('http://localhost:8000/random-videos/')
      .then((response) => {
        this.videos = response.data['videos']
      })
    },
    getRandomVideosBasedOnUser: function () {
      var userId = this.$store.state.userInfo.id
      var userAccess = this.$store.state.userInfo.access
      axios.get(`http://localhost:8000/random-videos-based-on-users/${userId}/`,
      {
        headers: {
            Authorization: `Bearer ${userAccess}`
          }
      })
      .then((response) => {
        this.videos = response.data['videos']
      })
    },
    viewVideo: function (id, complex, slug, tag_ids) {
      if (this.$store.state.userInfo.access != null) {
        this.addUserViewedVideo(tag_ids)
        this.addUserViewedVideos(id)
      }
      this.$router.push({ name: 'VideoDetail', params: { complexId: complex, id: id, slug: slug}})
    },
    // add user's viewed video tags
    addUserViewedVideo: function (tag_ids) {
      var userId = this.$store.state.userInfo.id
      var userAccess = this.$store.state.userInfo.access
      axios.post(`http://localhost:8000/add-user-viewed-video/${userId}/`, {
        tag_ids: tag_ids
      },
      {
        headers: {
            Authorization: `Bearer ${userAccess}`
          }
      })
    },
    // add user's viewed videos
    addUserViewedVideos: function (videoId) {
      var userId = this.$store.state.userInfo.id
      var userAccess = this.$store.state.userInfo.access
      axios.post(`http://localhost:8000/add-user-viewed-videos/${userId}/${videoId}/`, {},
      {
        headers: {
            Authorization: `Bearer ${userAccess}`
          }
      })
    }
  }
}
</script>


<style scoped>
.card-video {
  cursor: pointer
}
.card-video:hover {
  color: rgb(255, 255, 255)
}
</style>