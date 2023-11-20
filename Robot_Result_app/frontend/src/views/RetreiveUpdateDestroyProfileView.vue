<template>
  <section class="bg-seasalt" style="min-height: 100vh; padding-top: 5%;" >
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col col-lg-6 mb-4 mb-lg-0">
          <div class="card mb-3">
            <div class="row g-0">
              
              <!-- Avatar & Details Section -->
              <div class="col-md-4 bg-ucla-blue text-center text-seasalt">
                
                <!-- Avatar -->
                <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" class="img-fluid my-5" style="width: 80px;" />
                
                <h5><b>{{ user.username }}</b></h5>
                <br>
                <button class="btn btn-light mb-5" v-if="!editMode" @click="startEdit">Edit Profile</button>
              
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
                      <button type="submit" class="btn btn-primary me-2">Save</button> 
                      <!-- TODO: MAKE BUTTON UCLA BLUE COLOUR -->
                      <button @click="cancelEdit" class="btn btn-secondary bg-ucla-blue">Cancel</button>
                    </form>
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
      editableUser: {},
      editMode: false,
    };
  },
  async created() {
    try {
      const username = await axios.get("/auth/users/me/");
      console.log(username);
      const response = await axios.get('/api/v1/users/' + username.data.username +'/');
      this.user = response.data;
      this.editableUser = { ...this.user };  // Clone user data for editing
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  },
  methods: {
    startEdit() {
      this.editMode = true;
    },
    async updateProfile() {
      try {
        const username = await axios.get("/auth/users/me/");
        console.log(username);
        const response = await axios.put('/api/v1/users/' + username.data.username + "/", this.editableUser);
        this.user = response.data;
        this.editMode = false;
      } catch (error) {
        console.error("Error updating user profile:", error);
      }
    },
    cancelEdit() {
      this.editableUser = { ...this.user };  // Revert changes
      this.editMode = false;
    },
  }
};
</script>

