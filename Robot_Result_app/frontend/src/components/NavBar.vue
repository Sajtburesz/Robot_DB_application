<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-alice-blue">
    <!-- Container wrapper -->
    <div class="container-fluid">
      <!-- Toggle button -->
      <button class="navbar-toggler btn btn-link ms-2" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <font-awesome-icon icon="fa-solid fa-bars" />
      </button>

      <!-- Collapsible wrapper -->
      <div class="collapse navbar-collapse justify-content-center" id="navbarSupportedContent">
        <!-- Navbar brand -->
        <router-link class="navbar-brand mt-lg-o" :to="{ name: 'home' }">
          <img src="/static/images/Robot-framework-logo.png" height="40"
            alt="Robot Framework Logo" loading="lazy" />
        </router-link>
        <!-- Left links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item me-2">
            <router-link class="nav-link fw-bold" :to="{ name: 'ListTestRunsView' }">Test Runs</router-link>
          </li>
          <li class="nav-item me-2">
            <router-link class="nav-link fw-bold" :to="{ name: 'CreateTeamView' }">Team</router-link>
          </li>
          <li class="nav-item me-2">
            <router-link class="nav-link fw-bold shadow p-2 mb-1 bg-body rounded upload-navlink upload-navlink-animation" :to="{ name: 'CreateTestRunView' }">Upload</router-link>
          </li>
          <li class="nav-item me-2" v-if="isAdmin">
            <router-link class="nav-link fw-bold" :to="{ name: 'ManageAttributesView' }">Admin</router-link>
          </li>
        </ul>
        <!-- Left links -->
        <!-- Right elements -->
        <div class="d-flex align-items-center">
          <!-- Avatar -->
          <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdownMenuLink" type="button"
            data-bs-toggle="dropdown" aria-expanded="false">
            <img v-if="getAvatar" :src="`/static/avatars/${getAvatar}`" class="rounded-circle" height="50"
              alt="Portrait of a Woman" loading="lazy" />
          </a>
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuLink">
            <li>
              <router-link class="dropdown-item" :to="{ name: 'RetreiveUpdateDestroyeProfileView' }">My profile</router-link>
            </li>
            <li>
              <a class="dropdown-item" href="/accounts/logout/">Logout</a>
            </li>
          </ul>
        </div>
        <!-- Right elements -->
      </div>
      <!-- Collapsible wrapper -->

    </div>
    <!-- Container wrapper -->
  </nav>
  <!-- Navbar -->
</template>

<script>
import { axios } from "@/common/api.service.js";

export default {
  name: "NavBarComponent",
  created() {
    this.fetchAvatar(); // Fetch avatar when component is created
  },
  computed: {
    isAdmin() {
      this.$store.dispatch('fetchAdminStatus');
      return this.$store.state.isAdmin;
    },
    getAvatar() {
      return this.$store.state.avatar;
    },
  },
  methods:{
    async fetchAvatar(){
      try{
        const user = await axios.get('/auth/users/me/');
        const avatar = await axios.get(`/api/v1/users/${user.data.username}/`);
        this.$store.dispatch('setAvatar',avatar.data.avatar);
      }catch(error){
        this.$toast.error("Something went wrong when fetching avatar.");
      }
    }
  }
};
</script>

<style>

.upload-navlink-animation {
  transition: background-color 0.3s ease, color 0.3s ease;
}

.upload-navlink:hover{
  background-color: #3a6f8fff !important; 
  color: #f7f7f7ff !important;
}


@media (max-width: 399px) {
  .navbar-expand-lg .navbar-toggler {
    display: block;
  }

  .navbar-expand-lg .navbar-collapse {
    display: none;
  }
  .navbar-expand-lg {
    flex-wrap: wrap;
  }

  .navbar-expand-lg .navbar-collapse {
    flex-basis: 100%;
    justify-content: center;
  }

  .navbar-expand-lg .d-flex {
    margin-top: 0.5rem; /* Adjust this as needed */
    justify-content: flex-end;
    width: 100%;
  }
}

@media (min-width: 400px) {
  .navbar-expand-lg .navbar-nav .nav-item {
    display: flex;
  }

  .navbar-expand-lg .navbar-nav {
    flex-direction: row;
  }
    .navbar-expand-lg .navbar-collapse {
    justify-content: flex-start;
  }

  .navbar-expand-lg .d-flex {
    justify-content: flex-end;
  }
  .navbar-expand-lg .navbar-toggler {
    display: none;
  }

  .navbar-expand-lg .navbar-collapse {
    display: flex;
  }
}

</style>