<template>
  <div id="video">
    <v-container>
      <v-row>
        <v-col cols="12" class="col-lg-9 col-md-9 col-sm-12">
          <video autoplay controls buffered width="100%">
            <source :src="video.videoFile" type="video/mp4" />
          </video>
          <h1>{{ video.title }}</h1>
          <div class="d-flex">
            <h4>{{ video.views }} views - {{ video.date }}</h4>
            <div class="ml-auto">
              <div class="d-flex">
                <v-btn
                  v-if="liked"
                  class="text-capitalize grey darken-4 mr-2 white--text"
                  text
                  @click="likeVideo(video.id)"
                >
                  liked {{ video.likes }}
                </v-btn>
                <v-btn
                  v-else
                  class="text-capitalize grey mr-2"
                  text
                  @click="likeVideo(video.id)"
                >
                  likes {{ video.likes }}
                </v-btn>

                <v-btn
                  v-if="disliked"
                  class="text-capitalize grey darken-4 mr-2 white--text"
                  text
                  @click="dislikeVideo(video.id)"
                >
                  disliked {{ video.dislikes }}
                </v-btn>
                <v-btn
                  v-else
                  class="text-capitalize grey ml-2"
                  text
                  @click="dislikeVideo(video.id)"
                >
                  dislikes {{ video.dislikes }}
                </v-btn>
              </div>
            </div>
          </div>
          <h2>{{ video.uploaderName }}</h2>
          <hr class="mt-5" />
          <!-- comments -->
          <div class="mt-5">
            <h3>Comments</h3>
            <div class="d-flex">
              <v-text-field
                label="Write your comment"
                v-model="comment"
                autocomplete="off"
                @click="clickWhenNotLogged()"
              >
              </v-text-field>
              <v-btn
                v-if="$store.state.userInfo.access != null"
                class="grey mt-3 text-capitalize"
                @click="sendComment()"
                >Send</v-btn
              >
            </div>

            <div>
              <div
                class="grey lighten-2 my-3 py-3 px-5"
                v-for="(comment, index) in comments"
                :key="comment.id"
              >
                <div v-if="edit == comment.id" class="d-flex">
                  <v-text-field v-model="commentForEdit"></v-text-field>
                  <v-btn
                    class="ml-auto mt-3"
                    @click="editComment(comment.id, index)"
                    >edit</v-btn
                  >
                </div>
                <div v-else>
                  <h3>{{ comment.username }}</h3>
                  <span>{{ comment.content }}</span>
                  <div class="mt-2 d-flex">
                    <small class="mt-5">{{ comment.date }}</small>
                    <i
                      v-if="comment.liked"
                      style="color: cyan"
                      class="fas fa-thumbs-up mt-5 ml-5"
                      @click="likeComment(comment.id, index)"
                    ></i>
                    <i
                      v-else
                      class="fas fa-thumbs-up mt-5 ml-5"
                      @click="likeComment(comment.id, index)"
                    ></i>
                    <small class="ml-2 mt-5">{{ comment.likes }}</small>
                    <i
                      v-if="comment.userId == $store.state.userInfo.id"
                      style="cursor: pointer"
                      class="fas fa-trash-alt ml-auto mt-5"
                      @click="deleteComment(comment.id, index)"
                    ></i>
                    <i
                      v-if="comment.userId == $store.state.userInfo.id"
                      style="cursor: pointer"
                      class="fas fa-edit ml-2 mt-5"
                      @click="showEdit(comment.id, comment.content)"
                    ></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </v-col>
        <v-col cols="12" class="col-lg-3 col-md-3 col-sm-8 ml-auto mr-auto">
          <v-card
            flat
            v-for="video in videos"
            :key="video.id"
            class="card-video grey lighten-1 pb-3 my-3"
            @click="
              viewVideo(video.id, video.complex, video.slug, video.tag_ids)
            "
          >
            <img :src="video.thumbnail" width="100%" height="200px" alt="" />
            <h4 class="px-2 py-2">{{ video.title }}</h4>
            <small class="ml-2 mr-2"
              >{{ video.views }} views | {{ video.uploaderName }}</small
            >
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "VideoDetail",
  data() {
    return {
      video: null,
      videos: [],

      liked: false,
      disliked: false,

      comment: null,
      edit: null,
      commentForEdit: null,
      comments: [],

      notificationSocket: null,
    };
  },
  created() {
    this.query(this.$route.params.id);

    if (this.$store.state.userInfo.access != null) {
      this.checkLiked(this.$route.params.id);
    }

    setTimeout(() => this.videoViewCount(this.$route.params.id), 500);

    this.notificationSocket = new WebSocket(
      "ws://localhost:8000/ws/notification/notificationWebSocket/"
    )
    this.notificationSocket.onclose = function() {
      console.log('web socket closed')
    }
  },
  methods: {
    getVideoDetail: function (id) {
      axios.get(`http://localhost:8000/${id}/video/`).then((response) => {
        this.video = response.data["video"];
      });
    },
    async query(id) {
      await this.relatedVideos(id);
      await this.getComments();
      this.getVideoDetail(id);
    },
    videoViewCount: function (id) {
      axios.post(`http://localhost:8000/view-count/${id}/`).then((response) => {
        this.video.views = response.data["views"];
      });
    },
    relatedVideos: function (id) {
      axios
        .get(`http://localhost:8000/get-related-videos/${id}/`)
        .then((response) => {
          this.videos = response.data["relatedVideos"];
        });
    },
    checkLiked: function (videoId) {
      var userId = this.$store.state.userInfo.id;

      axios
        .get(
          `http://localhost:8000/check-user-liked-or-disliked/${videoId}/${userId}/`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.userInfo.access}`,
            },
          }
        )
        .then((response) => {
          if (response.data["liked"]) this.liked = true;
          else if (response.data["disliked"]) this.disliked = true;
        });
    },
    likeVideo: function (videoId) {
      if (this.$store.state.userInfo.access == null) {
        this.$store.commit("getCurrentUrl", this.$route.path);
        this.$router.push({ name: "Login" });
      } else {
        var userId = this.$store.state.userInfo.id;

        axios
          .post(
            `http://localhost:8000/like-video/${videoId}/${userId}/`,
            {},
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.userInfo.access}`,
              },
            }
          )
          .then((response) => {
            this.video.likes = response.data["likes"];
            this.video.dislikes = response.data["dislikes"];

            if (response.data["liked"]) {
              this.liked = true;
              this.disliked = false;
              // send notification socket
              if (this.$store.state.userInfo.id != this.video.uploaderId) {
                  this.notificationSocket.send(JSON.stringify({
                    'sender_name': this.$store.state.userInfo.username,
                    'user_id': this.video.uploaderId,
                    'content': `${this.$store.state.userInfo.username} liked your video`,
                    'url': this.$route.path
                  }))
              }
            } else this.liked = false;

            if (response.data["disliked"]) {
              this.disliked = true;
              this.liked = false;
            } else {
              this.disliked = false;
            }

            
          });
      }
    },
    dislikeVideo: function (videoId) {
      if (this.$store.state.userInfo.access == null) {
        this.$store.commit("getCurrentUrl", this.$route.path);
        this.$router.push({ name: "Login" });
      } else {
        var userId = this.$store.state.userInfo.id;

        axios
          .post(
            `http://localhost:8000/dislike-video/${videoId}/${userId}/`,
            {},
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.userInfo.access}`,
              },
            }
          )
          .then((response) => {
            this.video.likes = response.data["likes"];
            this.video.dislikes = response.data["dislikes"];

            if (response.data["liked"]) {
              this.liked = true;
              this.disliked = false;
            } else this.liked = false;

            if (response.data["disliked"]) {
              this.disliked = true;
              this.liked = false;
            } else {
              this.disliked = false;
            }
          });
      }
    },
    getComments: function () {
      var videoId = this.$route.params.id;

      if (this.$store.state.userInfo.access == null) {
        axios
          .get(`http://localhost:8000/get-comments-unauthenticated/${videoId}/`)
          .then((response) => {
            this.comments = response.data["comments"];
          });
      } else {
        var userId = this.$store.state.userInfo.id;
        axios
          .get(
            `http://localhost:8000/get-comments-authenticated/${videoId}/${userId}/`
          )
          .then((response) => {
            this.comments = response.data["comments"];
          });
      }
    },
    sendComment: function () {
      if (this.$store.state.userInfo.access == null) {
        this.$store.commit("getCurrentUrl", this.$route.path);
        this.$router.push({ name: "Login" });
      } else if (this.comment == null) return;
      else {
        var videoId = this.$route.params.id;
        var userId = this.$store.state.userInfo.id;

        axios
          .post(
            `http://localhost:8000/send-comment/${videoId}/${userId}/`,
            {
              content: this.comment,
            },
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.userInfo.access}`,
              },
            }
          )
          .then((response) => {
            this.comments.unshift(response.data["comment"]);
            this.comment = null;

            // send notification socket
            if (this.$store.state.userInfo.id != this.video.uploaderId) {
                this.notificationSocket.send(JSON.stringify({
                  'sender_name': this.$store.state.userInfo.username,
                  'user_id': this.video.uploaderId,
                  'content': `${this.$store.state.userInfo.username} commented on your video`,
                  'url': this.$route.path
                }))
            }
          });
      }
    },
    clickWhenNotLogged() {
      if (this.$store.state.userInfo.access == null) {
        this.$store.commit("getCurrentUrl", this.$route.path);
        this.$router.push({ name: "Login" });
      } else return;
    },
    likeComment: function (id, index) {
      this.clickWhenNotLogged();

      var userId = this.$store.state.userInfo.id;
      axios
        .post(
          `http://localhost:8000/like-comment/${id}/${userId}/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.userInfo.access}`,
            },
          }
        )
        .then((response) => {
          this.comments[index].liked = response.data["liked"];
          this.comments[index].likes = response.data["likes"];
          
          if (this.comments[index].liked) {
            // send notification socket
            if (this.$store.state.userInfo.id != this.comments[index].userId) {
                this.notificationSocket.send(JSON.stringify({
                  'sender_name': this.$store.state.userInfo.username,
                  'user_id': this.comments[index].userId,
                  'content': `${this.$store.state.userInfo.username} liked your comment`,
                  'url': this.$route.path
                }))
            }
          }
        });
    },
    viewVideo: function (id, complex, slug, tag_ids) {
      if (this.$store.state.userInfo.access != null) {
        this.addUserViewedVideo(tag_ids);
        this.addUserViewedVideos(id);
      }
      this.$router.push({ params: { complexId: complex, id: id, slug: slug } });
      window.location.reload();
    },
    // add user's viewed video tags
    addUserViewedVideo: function (tag_ids) {
      var userId = this.$store.state.userInfo.id;
      var userAccess = this.$store.state.userInfo.access;
      axios.post(
        `http://localhost:8000/add-user-viewed-video/${userId}/`,
        {
          tag_ids: tag_ids,
        },
        {
          headers: {
            Authorization: `Bearer ${userAccess}`,
          },
        }
      );
    },
    // add user's viewed videos
    addUserViewedVideos: function (videoId) {
      var userId = this.$store.state.userInfo.id;
      var userAccess = this.$store.state.userInfo.access;
      axios.post(
        `http://localhost:8000/add-user-viewed-videos/${userId}/${videoId}/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${userAccess}`,
          },
        }
      );
    },
    deleteComment(id, index) {
      var userId = this.$store.state.userInfo.id;
      axios
        .post(
          `http://localhost:8000/delete-comment/${id}/${userId}/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.userInfo.access}`,
            },
          }
        )
        .then((response) => {
          if (response.data["success"]) {
            this.comments.splice(index, 1);
          }
        });
    },
    showEdit(id, content) {
      this.edit = id;
      this.commentForEdit = content;
    },
    editComment(id, index) {
      var userId = this.$store.state.userInfo.id;
      axios
        .post(
          `http://localhost:8000/edit-comment/${id}/${userId}/`,
          {
            content: this.commentForEdit,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.userInfo.access}`,
            },
          }
        )
        .then((response) => {
          this.comments[index].content = response.data["content"];
          this.edit = null;
        });
    },
  },
};
</script>

<style scoped>
.fa-thumbs-up {
  cursor: pointer;
}
.card-video {
  cursor: pointer;
}
.card-video:hover {
  color: rgb(255, 255, 255);
}
</style>