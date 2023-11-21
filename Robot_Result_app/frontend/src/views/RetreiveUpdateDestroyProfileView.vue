<template>
  <section class="bg-seasalt" style="min-height: 100vh; padding-top: 5%;">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col col-lg-6 mb-4 mb-lg-0">
          <div class="card mb-3">
            <div class="row g-0">

              <!-- Avatar & Details Section -->
              <div class="col-md-4 bg-ucla-blue text-center text-seasalt">

                <!-- User's Current Avatar -->
                <img v-if="user.avatar" :src="`/static/avatars/${user.avatar}`" alt="Avatar"
                  class="img-fluid rounded-circle my-5 hover-zoom-icon" style="width: 80px; cursor: pointer;"
                  data-bs-toggle="modal" data-bs-target="#avatarModal" loading="lazy" />
                <h5><b>{{ user.username }}</b></h5>
                <br>
                <button class="btn btn-light mb-2" v-if="!editMode" @click="startEdit">Edit Profile</button>
                <button class="btn btn-light mb-5" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change
                  Password</button>
              </div>

              <!-- Avatar Selection Modal -->
              <div class="modal fade" id="avatarModal" tabindex="-1" aria-labelledby="avatarModalLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="avatarModalLabel">Select Avatar</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <div class="d-flex justify-content-around flex-wrap">
                        <img v-for="avatar in avatars" :key="avatar" :src="`/static/avatars/${avatar}`" alt="Avatar"
                          class="img-fluid rounded-circle m-2 avatar-option hover-zoom-icon" @click="updateAvatar(avatar)"
                          data-bs-dismiss="modal" aria-label="Close" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Change Password Modal -->
              <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="changePasswordModalLabel">Change Password</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <form @submit.prevent="changePassword">
                        <input type="text" name="username" :value="user.username" class="form-control" autocomplete="username" hidden readonly>
                        <div class="mb-3">
                          <label class="form-label">Old Password:</label>
                          <input type="password" class="form-control" v-model="passwords.oldPassword"
                            autocomplete="current-password" required>
                        </div>
                        <div class="mb-3">
                          <label class="form-label">New Password:</label>
                          <input type="password" class="form-control" v-model="passwords.newPassword"
                            autocomplete="new-password" required>
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Confirm New Password:</label>
                          <input type="password" class="form-control" v-model="passwords.confirmPassword"
                            autocomplete="new-password" required>
                        </div>
                        <button type="submit" class="btn bg-ucla-blue clickable-item text-seasalt" data-bs-dismiss="modal" aria-label="Close">Change Password</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Information Section -->
              <div class="col-md-8">
                <div class="card-body p-4">

                  <!-- When Not in Edit Mode -->
                  <div v-if="!editMode">
                    <h6 class="text-jet fw-bold">Information</h6>
                    <hr class="mt-0 mb-4">
                    <div class="row pt-1">
                      <div class="col-6 mb-3">
                        <h6 class="text-jet fw-bold">Email</h6>
                        <p class="text-muted">{{ user.email }}</p>
                      </div>
                      <div class="col-6 mb-3">
                        <h6 class="text-jet fw-bold">Name</h6>
                        <p class="text-muted">{{ user.first_name }} {{ user.last_name }}</p>
                      </div>
                    </div>
                    <h6 class="text-jet fw-bold">Description</h6>
                    <hr class="mt-0 mb-4">
                    <p class="text-jet">{{ user.description }}</p>
                  </div>

                  <!-- When in Edit Mode -->
                  <div v-else>
                    <form @submit.prevent="updateProfile">
                      <div class="mb-3">
                        <label class="form-label text-jet fw-bold">First Name:</label>
                        <input class="form-control" v-model="editableUser.first_name" />
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-jet fw-bold">Last Name:</label>
                        <input class="form-control" v-model="editableUser.last_name" />
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-jet fw-bold">Email:</label>
                        <input type="email" class="form-control" v-model="editableUser.email" />
                      </div>
                      <div class="mb-3">
                        <label class="form-label text-jet fw-bold">Description:</label>
                        <textarea class="form-control" v-model="editableUser.description"></textarea>
                      </div>
                      <button type="submit" class="btn bg-ucla-blue clickable-item text-seasalt me-2">Save</button>
                      <button @click="cancelEdit" class="btn btn-secondary bg-ucla-blue">Cancel</button>
                      <button class="btn btn-link hover-zoom-icon" data-bs-toggle="modal"
                        data-bs-target="#userDeleteModal">
                        <font-awesome-icon icon="fa-solid fa-trash" style="color: red;" size="2xl" />
                      </button>
                    </form>
                  </div>
                  <!-- User Delete Confirmation Modal -->
                  <div class="modal" tabindex="-1" role="dialog" aria-hidden="true" id="userDeleteModal">
                    <div class="modal-dialog" role="document">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title">Delete Account</h5>
                          <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button>
                        </div>
                        <div class="modal-body">
                          <p>Are you sure about deleting account?</p>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                          <button type="button" class="btn btn-danger" @click="deleteUser()"
                            data-bs-dismiss="modal">Yes</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { axios } from "@/common/api.service.js";


export default {
  data() {
    return {
      user: {},
      avatars: [],
      showAvatarSelection: false,
      editableUser: {},
      editMode: false,
      deleteModal: false,
      passwords: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  async created() {
    this.fetchUserData();
    this.fetchAvatar();
  },
  methods: {
    startEdit() {
      this.editMode = true;
    },
    async fetchUserData() {
      try {
        const username = await axios.get("/auth/users/me/");
        const response = await axios.get('/api/v1/users/' + username.data.username + '/');
        this.user = response.data;
        this.editableUser = { ...this.user };
        this.$store.dispatch('setAvatar', response.data.avatar);
      } catch (error) {
        this.$toast.error("Error fetching user data.");
      }
    },
    async updateProfile() {
      try {
        const username = await axios.get("/auth/users/me/");
        const response = await axios.put('/api/v1/users/' + username.data.username + "/", this.editableUser);
        this.user = response.data;
        this.editMode = false;
      } catch (error) {
        this.$toast.error("Error updating user profile.");
      }
    },
    async fetchAvatar() {
      try {
        const avatar = await axios.get(`/api/v1/avatar/change/`);
        this.avatars = avatar.data.avatars;
      } catch (error) {
        this.$toast.error("Something happened during fetching available avatars.");
      }
    },
    async updateAvatar(avatar) {
      try {
        await axios.post(`/api/v1/avatar/change/`, { avatar: avatar });
        this.fetchUserData();
      } catch (error) {
        this.$toast.error("Something happened during updateing avatars.");
      }
    },
    cancelEdit() {
      this.editableUser = { ...this.user };  // Revert changes
      this.editMode = false;
    },
    async deleteUser() {
      try {
        const username = await axios.get("/auth/users/me/");
        await axios.delete(`/api/v1/users/${username.data.username}/`);
        window.location.href = '/accounts/login/';
      } catch (error) {
        this.$toast.error("Something happened during user deletion.");
      }
    },
    async changePassword() {
      if (this.passwords.newPassword !== this.passwords.confirmPassword) {
        this.$toast.error("New passwords do not match.");
        return;
      }

      try {
        await axios.post('/api/v1/change-password/', {
          old_password: this.passwords.oldPassword,
          new_password: this.passwords.newPassword
        });
        this.$toast.success("Password changed successfully.");
      } catch (error) {
        this.$toast.error("Failed to change password.");
      }
    }
  }
};
</script>

<style scoped>
.hover-zoom-icon {
  transition: transform 0.3s ease;
}

.hover-zoom-icon:hover {
  transform: scale(1.1);
}

.avatar-option {
  width: 60px;
  cursor: pointer;
  transition: transform 0.3s ease;
}
</style>