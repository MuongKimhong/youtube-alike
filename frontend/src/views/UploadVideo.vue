<template>
  <div id="upload-video" style="margin-top: 20px">
    <v-container>
      <v-app-bar class="grey" dense style="border-radius: 8px">
        <template>
          <v-tabs v-model="tab" centered slider-color="white">
            <v-tab class="text-capitalize white--text" id="my-videos"
              >My videos</v-tab
            >
            <v-tab class="text-capitalize white--text">Upload</v-tab>
          </v-tabs>
        </template>
      </v-app-bar>
      <v-tabs-items v-model="tab">
        <!-- my videos tab -->
        <v-tab-item>
          <v-card flat>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  class="col-lg-2 col-md-3 col-sm-3"
                  v-for="(video, index) in userVideos"
                  :key="video.id"
                >
                  <v-card
                    flat
                    class="grey lighten-1 card-video pb-2"
                    @click="viewVideo(video.id, video.complex, video.slug)"
                  >
                    <img
                      :src="video.thumbnail"
                      width="100%"
                      height="200px"
                      alt=""
                    />
                    <h4 class="px-2 py-1">{{ video.title }}</h4>
                    <div class="d-flex mt-2">
                      <small class="ml-2 mr-2">{{ video.views }} views</small>
                    </div>
                  </v-card>
                  <v-btn class="col-12 red darken-2" @click="deleteVideo(video.id, index)">
                    <i class="fas fa-trash-alt white--text"></i>
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-tab-item>

        <!-- upload video tab -->
        <v-tab-item>
          <v-card flat>
            <!-- spinner -->
            <div v-if="spinner" class="text-center" style="margin-top: 50px">
              <v-progress-circular
                style="margin-top: 120px"
                :size="70"
                :width="7"
                color="grey"
                indeterminate
              >
              </v-progress-circular>
              <div
                class="text-center d-flex align-center col-lg-5 col-md-5 ml-auto mr-auto"
                style="margin-top: 30px"
              >
                <v-progress-linear
                  color="grey"
                  max="100"
                  v-model="uploadPercentage"
                ></v-progress-linear>
              </div>

              <h4 class="text-center">{{ percentageText }}</h4>
              <h5 class="text-center">
                Please don't leave this page while uploading
              </h5>
            </div>
            <!-- end spinner -->

            <div v-else>
              <div
                class="text-center d-flex align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-text-field
                  v-model="video.title"
                  required
                  type="text"
                  label="Video title"
                ></v-text-field>
              </div>
              <div
                class="text-center align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-file-input
                  show-size
                  required
                  label="Video"
                  @change="handleVideoFileUpload($event)"
                  accept="video/*"
                ></v-file-input>
              </div>
              <div
                class="text-center align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-file-input
                  show-size
                  required
                  label="Thumbnail image"
                  @change="handleThumbnailFileUpload($event)"
                  accept="image/*"
                ></v-file-input>
              </div>
              <div
                class="text-center align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-text-field
                  label="Enter video tags"
                  v-model="tag"
                  type="text"
                  @keyup="addVideoTags"
                >
                </v-text-field>
              </div>
              <div
                class="text-center align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-select
                  v-model="video.tags"
                  :items="video.tags"
                  attach
                  chips
                  label="tags"
                  multiple
                  required="true"
                >
                </v-select>
              </div>
              <div
                class="text-center align-center col-lg-5 col-md-5 ml-auto mr-auto"
              >
                <v-textarea
                  v-model="video.description"
                  label="Video description"
                ></v-textarea>
              </div>
              <div class="ml-auto mr-auto d-flex col-lg-5 col-md-5">
                <v-btn
                  type="button"
                  class="text-lowercase white--text col-12 grey"
                  @click="uploadVideo()"
                >
                  upload
                </v-btn>
              </div>
            </div>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "UploadVideo",
  data() {
    return {
      tab: null,
      tag: null,
      spinner: false,
      uploadingText: null,
      uploadPercentage: 0,
      percentageText: null,

      video: {
        title: null,
        videoFile: null,
        thumbnail: null,
        description: "",
        tags: [],
      },

      url: "/img/download_Rszepdk.744d63bb.jpeg",

      userVideos: [],
    };
  },
  created() {
    this.getAllUserVideos();
  },
  methods: {
    uploadVideo: function () {
      this.spinner = true;
      var formData = new FormData();
      var userId = this.$store.state.userInfo.id;
      var userAccess = this.$store.state.userInfo.access;
      formData.append("videoFile", this.video.videoFile);
      formData.append("thumbnail", this.video.thumbnail);
      formData.append("title", this.video.title);
      formData.append("description", this.video.description);
      formData.append("tags", this.video.tags);

      axios
        .post(`http://localhost:8000/${userId}/upload-video/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${userAccess}`,
          },
          onUploadProgress: function (progressEvent) {
            this.uploadPercentage = parseInt(
              Math.round((progressEvent.loaded / progressEvent.total) * 100)
            );
            this.percentageText = String(this.uploadPercentage) + " %";
            if (this.uploadPercentage > 90)
              this.percentageText = "finishing ..";
          }.bind(this),
        })
        .then((response) => {
          this.userVideos.unshift(response.data["video"]);
          setTimeout(() => {
            document.getElementById("my-videos").click();
            for (var key in this.video) {
              if (String(key) == "description") this.video[key] = "";
              else if (String(key) == "tags") this.video[key] = [];
              else this.video[key] = null;
            }
            this.spinner = false;
          }, 1000);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleVideoFileUpload(files) {
      this.video.videoFile = files;
    },
    handleThumbnailFileUpload(files) {
      this.video.thumbnail = files;
    },
    getAllUserVideos: function () {
      axios
        .get(
          `http://localhost:8000/${this.$store.state.userInfo.id}/get-all-user-videos/`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.userInfo.access}`,
            },
          }
        )
        .then((response) => {
          this.userVideos = response.data["videos"];
        });
    },
    viewVideo: function (id, complex, slug) {
      this.$router.push({
        name: "VideoDetail",
        params: { complexId: complex, id: id, slug: slug },
      });
    },
    addVideoTags: function (e) {
      if (e.keyCode === 13) {
        if (this.tag != null) {
          this.video.tags.push(String(this.tag));
          this.tag = null;
        }
      } else return;
    },
    deleteVideo: function(id, index) {
      var userId = this.$store.state.userInfo.id
      axios.post(`http://localhost:8000/delete-video/${id}/${userId}/`, {},
      {
        headers: {
          Authorization: `Bearer ${this.$store.state.userInfo.access}`,
        },
      })
      .then((response) => {
        if (response.data['success']) {
          this.userVideos.splice(index, 1)
        }
      })
    }
  },
};
</script>

<style scoped>
.card-video {
  cursor: pointer;
}
.card-video:hover {
  color: rgb(255, 255, 255);
}
</style>